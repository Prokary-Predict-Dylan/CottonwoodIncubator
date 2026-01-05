from Bio import SeqIO
import io
import cobra
import re
from collections import Counter

# -------------------------
# FASTA PARSER
# -------------------------
def parse_fasta(file_like):
    """
    Robust FASTA parser for Streamlit:
    - Accepts text-mode file or UploadedFile (converted to text).
    """
    records = list(SeqIO.parse(file_like, "fasta"))
    results = []
    for r in records:
        results.append({
            "id": r.id,
            "name": r.name or r.id,
            "description": r.description,
            "sequence": str(r.seq),
            "length": len(r.seq),
            "source": "fasta"
        })
    return results

# -------------------------
# GENBANK PARSER
# -------------------------
def parse_genbank(file_like):
    """
    Robust GenBank parser for Streamlit.
    """
    records = list(SeqIO.parse(file_like, "genbank"))
    results = []
    for r in records:
        for feat in r.features:
            if feat.type in ("gene", "CDS", "rRNA", "tRNA"):
                q = feat.qualifiers or {}
                results.append({
                    "id": q.get("locus_tag", ["unknown"])[0],
                    "name": q.get("gene", [None])[0] or q.get("locus_tag", ["unknown"])[0],
                    "product": q.get("product", [""])[0],
                    "start": int(feat.location.start) if feat.location else None,
                    "end": int(feat.location.end) if feat.location else None,
                    "length": int(len(feat.location)) if feat.location else 0,
                    "type": feat.type,
                    "qualifiers": q,
                    "source": "genbank"
                })
    return results

# -------------------------
# SBML PARSER
# -------------------------
def autogenerate_categories_from_model(model):
    categories = {
        "energy_systems": set(),
        "core_metabolism": set(),
        "biosynthesis": set(),
        "transport": set(),
        "regulation": set()
    }
    heuristics = {
        "energy_systems": ["photosystem", "psa", "psb", "ndh", "cytochrome", "oxidase", "electron", "respir", "atp", "ferro"],
        "core_metabolism": ["glycolysis", "tca", "krebs", "gdh", "gap", "pyk"],
        "biosynthesis": ["synthase", "synthetase", "ribose", "fatty", "amino", "mur"],
        "transport": ["transporter", "export", "import", "abc", "symport", "antiport"],
        "regulation": ["regulator", "sensor", "two-component", "sigma", "tf"],
    }

    token_counts = Counter()
    for r in model.reactions:
        text = " ".join([r.id or "", r.name or "", getattr(r, "subsystem", "") or ""]).lower()
        for cat, keys in heuristics.items():
            if any(k in text for k in keys):
                categories[cat].update(keys)
        for t in re.findall(r"[a-zA-Z0-9_]+", text):
            token_counts[t] += 1
    return categories

def parse_sbml(file_like):
    try:
        model = cobra.io.read_sbml_model(file_like)
    except Exception:
        file_like.seek(0)
        content_bytes = file_like.read()
        model = cobra.io.read_sbml_model(io.StringIO(content_bytes.decode("utf-8", errors="ignore")))

    auto_cats = autogenerate_categories_from_model(model)

    genes = []
    for g in model.genes:
        reaction_text = "; ".join([r.name or r.id for r in g.reactions]).lower()
        genes.append({
            "id": g.id,
            "name": g.name or g.id,
            "product": reaction_text,
            "auto_categories": auto_cats,
            "reactions": [r.id for r in g.reactions],
            "source": "sbml"
        })

    reactions = [
        {
            "id": r.id,
            "name": r.name or r.id,
            "bounds": (r.lower_bound, r.upper_bound),
            "genes": [g.id for g in r.genes],
            "source": "sbml"
        }
        for r in model.reactions
    ]

    return {"cobra_model": model, "genes": genes, "reactions": reactions, "auto_categories": auto_cats}
