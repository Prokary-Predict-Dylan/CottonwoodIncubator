# Color system
DEFAULT_COLORS = {
    "core_metabolism": "#bed5d6",
    "energy_systems": "#c1d6be",
    "biosynthesis": "#a38280",
    "regulation": "#af5a53",
    "transport": "#eaceca",
    "other_functions": "#c38a71"
}

# Category priority (for SBML auto_categories)
CATEGORY_PRIORITY = [
    "regulation",
    "transport",
    "biosynthesis",
    "core_metabolism",
    "energy_systems",
    "other_functions"
]

# Mapping reactions → functional categories
REACTION_KEYWORDS = {
    "core_metabolism": ["glycolysis", "tca cycle", "calvin cycle"],
    "energy_systems": ["photosynthesis", "respiration", "atp synthase"],
    "biosynthesis": ["amino acid", "nucleotide", "lipid"],
    "regulation": ["transcription factor", "tf"],
    "transport": ["membrane transporter", "transporter", "channel", "pump"]
}

def categorize_feature(record):
    """
    Categorize a gene/feature based on:
      1) SBML auto_categories if present
      2) Reactions it catalyzes (REACTION_KEYWORDS mapping)
      3) Fallback: other_functions
    """
    prod = (record.get("product") or "").lower()
    name = (record.get("name") or "").lower()
    text = f"{prod} {name}"

    # 1) SBML auto_categories
    auto_cats = record.get("auto_categories")
    if auto_cats:
        for category in CATEGORY_PRIORITY:
            keywords = auto_cats.get(category, set())
            for k in keywords:
                if k.lower() in text:
                    return category

    # 2) Map reactions → categories
    reactions = record.get("reactions", [])
    for r in reactions:
        rname = r.lower()
        for cat, keys in REACTION_KEYWORDS.items():
            for k in keys:
                if k in rname:
                    return cat

    # 3) Fallback
    return "other_functions"

def assign_color(category):
    return DEFAULT_COLORS.get(category, DEFAULT_COLORS["other_functions"])

def features_to_blocks(features):
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
