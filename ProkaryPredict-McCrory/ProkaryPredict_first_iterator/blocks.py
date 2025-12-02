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

# Mapping reaction products → functional categories
PRODUCT_KEYWORDS = {
    "core_metabolism": ["glucose", "pyruvate", "acetyl-CoA", "ATP", "NADH"],
    "energy_systems": ["ATP", "ADP", "protons", "NADPH", "oxygen"],
    "biosynthesis": ["amino acid", "nucleotide", "lipid", "fatty acid"],
    "regulation": ["transcription factor", "regulator"],
    "transport": ["membrane", "imported", "exported", "pump", "channel"]
}


def categorize_feature_by_products(record):
    """
    Categorize a gene/feature based on:
      1) Reaction products
      2) SBML auto_categories (if present)
      3) Fallback: other_functions
    """
    # Look at reactions and their products
    reactions = record.get("reactions_detail", [])  # detailed reaction objects or dicts
    text = ""
    for r in reactions:
        # assume r has a 'products' field, list of product names
        products = r.get("products", [])
        text += " " + " ".join([p.lower() for p in products])

    # 1) Check products against keywords
    for cat, keys in PRODUCT_KEYWORDS.items():
        for k in keys:
            if k.lower() in text:
                return cat

    # 2) Fallback to auto_categories if available
    auto_cats = record.get("auto_categories")
    if auto_cats:
        for category in CATEGORY_PRIORITY:
            keywords = auto_cats.get(category, set())
            for k in keywords:
                if k.lower() in text:
                    return category

    # 3) Fallback default
    return "other_functions"


def assign_color(category):
    return DEFAULT_COLORS.get(category, DEFAULT_COLORS["other_functions"])


def features_to_blocks(features):
    """
    Convert feature list into blocks with start/end coordinates and color.
    Categorization is now based on reaction products.
    """
    blocks = []
    have_coords = all("start" in f and "end" in f for f in features)

    if have_coords:
        for f in features:
            cat = categorize_feature_by_products(f)
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
            cat = categorize_feature_by_products(f)
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
