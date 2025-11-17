DEFAULT_COLORS = {
    "core_metabolism": "#bed5d6",
    "energy_systems": "#c1d6be",
    "biosynthesis": "#a38280",
    "regulation": "#af5a53",
    "transport": "#eaceca",
    "other_functions": "#c38a71"
}

def categorize_feature(record):
    prod = (record.get("product") or "").lower()
    name = (record.get("name") or "").lower()

    # Core Metabolism
    if any(k in prod for k in ["dehydrogenase", "kinase", "synthetase", "reductase", "metabolic"]):
        return "core_metabolism"

    # Energy Systems
    if any(k in prod + name for k in ["atp synthase", "electron transport", "glycolysis", "respiration", "oxidase", "hydrogenase"]):
        return "energy_systems"

    # Biosynthesis
    if any(k in prod + name for k in ["ribosomal", "capsid", "flagellin", "polyketide", "amino acid"]):
        return "biosynthesis"

    # Regulation
    if any(k in name for k in ["regulator", "transcription", "sigma", "tf", "repressor", "activator"]):
        return "regulation"

    # Transport
    if any(k in prod + name for k in ["transporter", "channel", "pump"]):
        return "transport"

    # Other functions
    return "other_functions"

def assign_color(category):
    return DEFAULT_COLORS.get(category, DEFAULT_COLORS["other_functions"])

def features_to_blocks(features):
    blocks = []
    # Determine if features have coordinates
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
        # sequential layout if no coordinates
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
            pos += length + int(length * 0.1)  # small gap between blocks
    return blocks
