# app.py
import streamlit as st
import json
from parsers import parse_fasta, parse_genbank, parse_sbml
from blocks import features_to_blocks
from viz import blocks_to_figure
from export_pdf import export_gene_reaction_pdf
import io
import base64
import time

st.set_page_config(page_title="ProkaryPredict First Iterator", layout="wide")
st.title("ProkaryPredict — (First Iterator)")

# Ensure export_request exists
if "export_request" not in st.session_state:
    st.session_state["export_request"] = None

# -----------------------------------------------------------
# Sidebar
# -----------------------------------------------------------
with st.sidebar:
    st.header("Upload files")
    uploaded = st.file_uploader(
        "Upload GenBank (.gb/.gbk) / FASTA / SBML (.xml/.sbml)",
        accept_multiple_files=False
    )
    st.markdown("---")
    st.header("Export")
    export_name = st.text_input("PDF filename (without ext)", value="prokarypredict_report")

    if st.button("Export PDF"):
        st.session_state["export_request"] = time.time()

st.info("Upload a GenBank, FASTA, or SBML file. Parsed features will be converted to blocks and displayed.")

# -----------------------------------------------------------
# File Handling — FASTA, GenBank, SBML
# -----------------------------------------------------------
if uploaded is not None:
    fn = uploaded.name.lower()
    feature_list = []

    # ------------------------------
    # Helper: convert uploaded file to proper text-mode handle
    # ------------------------------
    def get_text_handle(file_obj):
        """
        Converts Streamlit UploadedFile (or bytes) to a text-mode file for Biopython.
        """
        import io
        file_obj.seek(0)
        content_bytes = file_obj.read()
        return io.TextIOWrapper(io.BytesIO(content_bytes), encoding="utf-8", errors="ignore")

    # ------------------------------
    # GenBank
    # ------------------------------
    if fn.endswith((".gb", ".gbk", ".genbank")):
        try:
            handle = get_text_handle(uploaded)
            feature_list = parse_genbank(handle)
            st.success(f"Parsed GenBank: {len(feature_list)} features found")
        except Exception as e:
            st.error(f"GenBank parsing failed: {e}")

    # ------------------------------
    # FASTA
    # ------------------------------
    elif fn.endswith((".fa", ".fasta")):
        try:
            handle = get_text_handle(uploaded)
            feature_list = parse_fasta(handle)
            st.success(f"Parsed FASTA: {len(feature_list)} sequences")
        except Exception as e:
            st.error(f"FASTA parsing failed: {e}")

    # ------------------------------
    # SBML
    # ------------------------------
    elif fn.endswith((".xml", ".sbml")):
        try:
            sbml_res = parse_sbml(io.BytesIO(uploaded.getvalue()))
            st.session_state["model"] = sbml_res["cobra_model"]

            for idx, g in enumerate(sbml_res["genes"]):
                feature_list.append({
                    "id": g["id"],
                    "name": g.get("name") or g["id"],
                    "product": g.get("product", ""),
                    "auto_categories": sbml_res.get("auto_categories", {}),
                    "start": idx * 200,
                    "end": idx * 200 + 100,
                    "length": 100,
                    "source": "sbml",
                    "reactions": g.get("reactions", [])
                })

            st.success(f"Parsed SBML: {len(feature_list)} genes")
        except Exception as e:
            st.error(f"SBML parsing failed: {e}")

    else:
        st.error("Unsupported file type. Upload FASTA, GenBank, or SBML.")

    # ------------------------------
    # If parsing succeeded, continue with blocks
    # ------------------------------
    if feature_list:
        blocks = features_to_blocks(feature_list)

        # Sidebar category filter
        categories = sorted(set(b["category"] for b in blocks))
        sel_cats = st.sidebar.multiselect(
            "Show categories", options=categories, default=categories
        )
        filtered_blocks = [b for b in blocks if b["category"] in sel_cats]

        # Block visualization
        st.subheader("Block visualization")
        fig = blocks_to_figure(filtered_blocks)
        st.plotly_chart(fig, use_container_width=True)

        # JSON export
        with st.expander("Block data (JSON)"):
            st.json(filtered_blocks)


# -----------------------------------------------------------
# PDF Export — Gene → Reaction mapping
# -----------------------------------------------------------
if st.session_state.get("export_request") and 'model' in st.session_state:
    model = st.session_state['model']
    try:
        pdf_bytes = export_gene_reaction_pdf(
            model,
            metadata={"source_file": uploaded.name if uploaded is not None else "unknown",
                      "exported_at": time.strftime("%Y-%m-%d %H:%M:%S")}
        )

        b64 = base64.b64encode(pdf_bytes).decode()
        fname = f"{export_name}.pdf"

        href = (
            f'<a href="data:application/pdf;base64,{b64}" '
            f'download="{fname}">Download PDF report</a>'
        )
        st.markdown(href, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"PDF export failed: {e}")

    # Reset request flag so subsequent clicks are new
    st.session_state["export_request"] = None
