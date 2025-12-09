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
# File Handling
# -----------------------------------------------------------
if uploaded is not None:
    fn = uploaded.name.lower()
    content = uploaded.read()
    feature_list = []

    try:
        # ------------------------------
        # GenBank
        # ------------------------------
        if fn.endswith((".gb", ".gbk", ".genbank")):
            feature_list = parse_genbank(io.BytesIO(content))
            st.success(f"Parsed GenBank: {len(feature_list)} features found")

        # ------------------------------
        # FASTA
        # ------------------------------
        elif fn.endswith((".fa", ".fasta")):
            feature_list = parse_fasta(io.BytesIO(content))
            st.success(f"Parsed FASTA: {len(feature_list)} sequences")

        # ------------------------------
        # SBML
        # ------------------------------
        elif fn.endswith((".xml", ".sbml")) or b"<sbml" in content[:200].lower():
            sbml_res = parse_sbml(io.BytesIO(content))

            # Store COBRA model in session for PDF export
            st.session_state['model'] = sbml_res["cobra_model"]  # ensure parse_sbml returns COBRA model

            # Build feature list for blocks
            for idx, g in enumerate(sbml_res["genes"]):
                feature_list.append({
                    "id": g["id"],
                    "name": g["name"],
                    "product": g.get("product", ""),  
                    "auto_categories": sbml_res["auto_categories"],  
                    "start": idx * 200,
                    "end": idx * 200 + 100,
                    "length": 100,
                    "source": "sbml",
                })
            st.success(f"Parsed SBML: {len(feature_list)} genes (mapped to blocks)")

        # ------------------------------
        # Unknown file → heuristics
        # ------------------------------
        else:
            st.warning("Unknown extension; attempting heuristics...")
            try:
                feature_list = parse_genbank(io.BytesIO(content))
                st.success(f"Parsed GenBank heuristically: {len(feature_list)} features found")
            except Exception:
                try:
                    feature_list = parse_fasta(io.BytesIO(content))
                    st.success(f"Parsed FASTA heuristically: {len(feature_list)} sequences")
                except Exception:
                    st.error("Could not parse file. Upload a valid GenBank, FASTA, or SBML file.")
                    feature_list = []

    except Exception as e:
        st.error(f"Parsing error: {e}")
        feature_list = []

    # -----------------------------------------------------------
    # Block Conversion
    # -----------------------------------------------------------
    blocks = features_to_blocks(feature_list)

    # -----------------------------------------------------------
    # Category Filter
    # -----------------------------------------------------------
    categories = sorted(set(b["category"] for b in blocks))
    sel_cats = st.sidebar.multiselect(
        "Show categories", options=categories, default=categories
    )
    filtered_blocks = [b for b in blocks if b["category"] in sel_cats]

    # -----------------------------------------------------------
    # Visualization
    # -----------------------------------------------------------
    st.subheader("Block visualization")
    fig = blocks_to_figure(filtered_blocks)
    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------------------------------------
    # JSON Export
    # -----------------------------------------------------------
    with st.expander("Block data (JSON)"):
        st.json(filtered_blocks)

st.subheader("Block workspace (visual code)")

# Generate blocks XML
blockly_xml_blocks = ""
previous_block_id = None
for i, gene in enumerate(filtered_blocks):
    block_id = f"gene_{i}"
    block_xml = f'<block type="gene_block" id="{block_id}">'
    block_xml += f'<field name="GENE">{gene["label"]}</field>'
    if previous_block_id:
        block_xml += f'<next><block type="gene_block" id="{block_id}_next"></block></next>'
    block_xml += "</block>"
    blockly_xml_blocks += block_xml
    previous_block_id = block_id

blockly_html = f"""
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <script src="https://unpkg.com/blockly/blockly.min.js"></script>
    <style>
        html, body {{ height: 100%; margin: 0; }}
        #blocklyDiv {{ height: 480px; width: 100%; }}
    </style>
  </head>
  <body>
    <div id="blocklyDiv"></div>
    <xml id="toolbox" style="display:none">
      <category name="Genome">
        <block type="gene_block"></block>
      </category>
    </xml>
    <script>
      // Define custom gene block
      Blockly.Blocks['gene_block'] = {{
        init: function() {{
          this.appendDummyInput()
              .appendField(new Blockly.FieldTextInput("Gene"), "GENE");
          this.setPreviousStatement(true, null);
          this.setNextStatement(true, null);
          this.setColour(160);
          this.setTooltip("");
          this.setHelpUrl("");
        }}
      }};

      var workspace = Blockly.inject('blocklyDiv', {{ toolbox: document.getElementById('toolbox') }});
      var xmlText = '<xml>{blockly_xml_blocks}</xml>';
      var xml = Blockly.Xml.textToDom(xmlText);
      Blockly.Xml.domToWorkspace(xml, workspace);
      Blockly.Xml.domToWorkspace(Blockly.Xml.textToDom(xmlText), workspace);
      Blockly.utils.toolbox.flyoutCategoryCallback = function(){{}};
    </script>
  </body>
</html>
"""
st.components.v1.html(blockly_html, height=520, scrolling=True)

# -----------------------------------------------------------
# PDF Export — Gene → Reaction mapping
# -----------------------------------------------------------
if st.session_state.get("export_request") and 'model' in st.session_state:
    model = st.session_state['model']
    pdf_bytes = export_gene_reaction_pdf(
        model,
        metadata={"source_file": uploaded.name}
    )

    b64 = base64.b64encode(pdf_bytes).decode()
    fname = f"{export_name}.pdf"

    href = (
        f'<a href="data:application/pdf;base64,{b64}" '
        f'download="{fname}">Download PDF report</a>'
    )
    st.markdown(href, unsafe_allow_html=True)
    st.session_state["export_request"] = None
