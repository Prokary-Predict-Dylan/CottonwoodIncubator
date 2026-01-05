import streamlit as st
import io
import time
import base64

from parsers import parse_fasta, parse_genbank, parse_sbml
from blocks import features_to_blocks
from viz import blocks_to_figure
from export_pdf import export_gene_reaction_pdf

# -------------------------
# Page setup
# -------------------------
st.set_page_config(page_title="ProkaryPredict — First Iterator", layout="wide")
st.title("ProkaryPredict — First Iterator")

if "export_request" not in st.session_state:
    st.session_state["export_request"] = None

# -------------------------
# Sidebar
# -------------------------
with st.sidebar:
    st.header("Upload genome/model")
    uploaded_file = st.file_uploader(
        "Upload GenBank (.gb/.gbk), FASTA (.fa/.fasta), or SBML (.xml/.sbml)",
        accept_multiple_files=False
    )

    st.markdown("---")
    st.header("Export")
    export_name = st.text_input("PDF filename (without extension)", value="prokarypredict_report")
    if st.button("Export PDF"):
        st.session_state["export_request"] = time.time()

st.info("Upload a GenBank, FASTA, or SBML file. Features will be parsed and displayed as blocks.")

# -------------------------
# Helper: convert to text-mode handle
# -------------------------
def get_text_handle(file_obj):
    """Convert Streamlit UploadedFile (or bytes) into proper text-mode handle for Biopython."""
    file_obj.seek(0)
    content_bytes = file_obj.read()
    return io.TextIOWrapper(io.BytesIO(content_bytes), encoding="utf-8", errors="ignore")

# -------------------------
# File handling
# -------------------------
feature_list = []
model_obj = None

if uploaded_file is not None:
    fn = uploaded_file.name.lower()
    try:
        if fn.endswith((".gb", ".gbk", ".genbank")):
            handle = get_text_handle(uploaded_file)
            feature_list = parse_genbank(handle)
            st.success(f"Parsed GenBank: {len(feature_list)} features found")

        elif fn.endswith((".fa", ".fasta")):
            handle = get_text_handle(uploaded_file)
            feature_list = parse_fasta(handle)
            st.success(f"Parsed FASTA: {len(feature_list)} sequences")

        elif fn.endswith((".xml", ".sbml")):
            sbml_res = parse_sbml(io.BytesIO(uploaded_file.getvalue()))
            model_obj = sbml_res["cobra_model"]
            st.session_state["model"] = model_obj

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

        else:
            st.error("Unsupported file type. Upload FASTA, GenBank, or SBML.")

    except Exception as e:
        st.error(f"File parsing failed: {e}")

# -------------------------
# Convert features → blocks
# -------------------------
if feature_list:
    blocks = features_to_blocks(feature_list)

    # Sidebar category filter
    categories = sorted(set(b["category"] for b in blocks))
    sel_cats = st.sidebar.multiselect("Show categories", options=categories, default=categories)
    filtered_blocks = [b for b in blocks if b["category"] in sel_cats]

    # Visualization
    st.subheader("Block visualization")
    fig = blocks_to_figure(filtered_blocks)
    st.plotly_chart(fig, use_container_width=True)

    # JSON export
    with st.expander("Block data (JSON)"):
        st.json(filtered_blocks)

# -------------------------
# PDF export
# -------------------------
if st.session_state.get("export_request") and model_obj is not None:
    try:
        pdf_bytes = export_gene_reaction_pdf(
            model_obj,
            metadata={
                "source_file": uploaded_file.name if uploaded_file else "unknown",
                "exported_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        )
        b64 = base64.b64encode(pdf_bytes).decode()
        fname = f"{export_name}.pdf"
        href = f'<a href="data:application/pdf;base64,{b64}" download="{fname}">Download PDF report</a>'
        st.markdown(href, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"PDF export failed: {e}")

    st.session_state["export_request"] = None
