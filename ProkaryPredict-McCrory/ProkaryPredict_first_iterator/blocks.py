# blocks.py (updated)
from collections import defaultdict

# Color system (reuse or expand)
DEFAULT_COLORS = {
    "core_metabolism": "#bed5d6",
    "energy_systems": "#c1d6be",
    "biosynthesis": "#a38280",
    "regulation": "#af5a53",
    "transport": "#eaceca",
    "other_functions": "#c38a71",
    "unassigned": "#cccccc"
}

# Mapping reactions → functional categories (replace with real pathways if available)
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

def assign_categories_from_reactions(reactions):
    """Given a list of reaction names/IDs, return a set of functional categories."""
    cats = set()
    for r in reactions:
        r_lower = r.lower()
        for key, cat in REACTION_TO_CATEGORY.items():
            if key in r_lower:
                cats.add(cat)
    return cats if cats else {"unassigned"}

def assign_color(categories):
    """Pick a color for a gene with one or more categories."""
    # If multiple categories, pick the first alphabetically (or implement blending)
    primary = sorted(categories)[0]
    return DEFAULT_COLORS.get(primary, DEFAULT_COLORS["unassigned"])

def features_to_blocks(features):
    blocks = []
    have_coords = all("start" in f and "end" in f for f in features)
    
    if have_coords:
        for f in features:
            reactions = f.get("reactions", [])
            cats = assign_categories_from_reactions(reactions)
            blocks.append({
                "id": f.get("id"),
                "label": f.get("name") or f.get("id"),
                "categories": list(cats),
                "category": sorted(cats)[0],  # pick one for color mapping
                "start": f.get("start"),
                "end": f.get("end"),
                "length": f.get("length") or (f.get("end") - f.get("start")),
                "color": assign_color(cats),
                "shape": "rect",
                "metadata": f
            })
    else:
        pos = 0
        for f in features:
            length = f.get("length", 100)
            reactions = f.get("reactions", [])
            cats = assign_categories_from_reactions(reactions)
            blocks.append({
                "id": f.get("id"),
                "label": f.get("name") or f.get("id"),
                "categories": list(cats),
                "category": sorted(cats)[0],
                "start": pos,
                "end": pos + length,
                "length": length,
                "color": assign_color(cats),
                "shape": "rect",
                "metadata": f
            })
            pos += length + int(length * 0.1)
            
    return blocks
