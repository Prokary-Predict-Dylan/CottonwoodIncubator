# blocks.py (refined for evidence-driven classification)
from collections import defaultdict

# Color system
DEFAULT_COLORS = {
    "core_metabolism": "#bed5d6",
    "energy_systems": "#c1d6be",
    "biosynthesis": "#a38280",
    "regulation": "#af5a53",
    "transport": "#eaceca",
    "other_functions": "#c38a71",
    "unassigned": "#cccccc",
    "non_coding": "#ffffff"
}

# Reaction → category mapping (expand with real pathways)
REACTION_TO_CATEGORY = {
    "glycolysis": "core_metabolism",
    "tca": "core_metabolism",
    "photosynthesis": "energy_systems",
    "respiration": "energy_systems",
    "lipid biosynthesis": "biosynthesis",
    "amino acid biosynthesis": "biosynthesis",
    "transcription": "regulation",
    "transport": "transport"
}

def categorize_feature(f):
    """
    Assign a functional category to a gene/feature.
    Non-coding genes get 'non_coding'.
    Protein-coding genes are categorized by:
      1. Reactions it catalyzes
      2. GO terms (if present)
      3. Domain/motif hints
      4. Fallback to 'other_functions'
    """
    # Non-coding genes
    if f.get("type") in ("tRNA", "rRNA", "ncRNA"):
        return "non_coding"

    categories = set()

    # 1) Reaction-based classification
    for r in f.get("reactions", []):
        r_lower = r.lower()
        for key, cat in REACTION_TO_CATEGORY.items():
            if key in r_lower:
                categories.add(cat)

    # 2) GO-term based (optional)
    for go_term in f.get("go_terms", []):
        go_lower = go_term.lower()
        if "transport" in go_lower:
            categories.add("transport")
        elif "regulator" in go_lower or "kinase" in go_lower:
            categories.add("regulation")
        elif "metabolism" in go_lower or "biosynthesis" in go_lower:
            categories.add("core_metabolism")
    
    # 3) Domain hints (optional)
    for domain in f.get("domains", []):
        dom_lower = domain.lower()
        if "transporter" in dom_lower:
            categories.add("transport")
        elif "synthase" in dom_lower or "synthetase" in dom_lower:
            categories.add("biosynthesis")
        elif "kinase" in dom_lower:
            categories.add("regulation")

    # 4) Fallback
    if not categories:
        categories.add("other_functions")

    return sorted(categories)[0]  # pick one for color mapping

def assign_color(category):
    return DEFAULT_COLORS.get(category, DEFAULT_COLORS["unassigned"])

def features_to_blocks(features):
    """
    Convert a list of gene/feature dictionaries to block dicts for plotting.
    Handles features with or without start/end coordinates.
    """
    blocks = []
    have_coords = all("start" in f and "end" in f for f in features)

    if have_coords:
        for f in features:
            cat = categorize_feature(f)
            blocks.append({
                "id": f.get("id"),
                "label": f.get("name") or f.get("id"),
                "category": cat,
                "start": f.get("start"),
                "end": f.get("end"),
                "length": f.get("length") or (f.get("end") - f.get("start")),
                "color": assign_color(cat),
                "shape": "rect",
                "metadata": f
            })
    else:
        pos = 0
        for f in features:
            length = f.get("length", 100)
            cat = categorize_feature(f)
            blocks.append({
                "id": f.get("id"),
                "label": f.get("name") or f.get("id"),
                "category": cat,
                "start": pos,
                "end": pos + length,
                "length": length,
                "color": assign_color(cat),
                "shape": "rect",
                "metadata": f
            })
            pos += length + int(length * 0.1)

    return blocks
