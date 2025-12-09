# blocks.py (EC-based gene categorization)
from collections import defaultdict
import re

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

# EC class → functional category mapping
EC_CATEGORY_MAP = {
    "1": "core_metabolism",     # Oxidoreductases
    "2": "biosynthesis",        # Transferases
    "3": "core_metabolism",     # Hydrolases
    "4": "core_metabolism",     # Lyases
    "5": "core_metabolism",     # Isomerases
    "6": "biosynthesis",        # Ligases
    "7": "transport"            # Translocases
}

EC_REGEX = re.compile(r"(\d+)\.\d+\.\d+\.\d+")  # Extracts the EC class number


def extract_ec_numbers(f):
    """
    Extract EC numbers from a feature record.
    Handles:
        - qualifiers: {"EC_number": ["1.1.1.1"]}
        - direct field: f["ec_number"]
        - product text containing "(EC 1.1.1.1)"
    Returns a list of EC numbers.
    """
    ecs = set()

    # 1) Qualifiers from GenBank or SBML
    q = f.get("qualifiers", {})
    if "EC_number" in q:
        for ec in q["EC_number"]:
            ecs.add(ec)

    # 2) Direct field
    if "ec_number" in f and f["ec_number"]:
        ecs.add(f["ec_number"])

    # 3) Product string
    prod = f.get("product", "")
    matches = EC_REGEX.findall(prod)
    for m in matches:
        ecs.add(m)

    return list(ecs)


def categorize_feature(f):
    """
    Assign category using:
      1) Non-coding type
      2) EC-based classification (most accurate)
      3) Subsystem fallback
      4) Product-name fallback
      5) If nothing: other_functions
    """
    # 1) Non-coding check
    if f.get("type") in ("tRNA", "rRNA", "ncRNA"):
        return "non_coding"

    # 2) EC-number based categorization
    ecs = extract_ec_numbers(f)
    for ec in ecs:
        ec_class = ec.split(".")[0]
        if ec_class in EC_CATEGORY_MAP:
            return EC_CATEGORY_MAP[ec_class]

    # 3) Subsystem fallback (SBML models often include this)
    subsystem = f.get("subsystem", "").lower()
    if "transport" in subsystem:
        return "transport"
    if "biosynth" in subsystem:
        return "biosynthesis"
    if "metabolism" in subsystem or "cycle" in subsystem:
        return "core_metabolism"
    if "regulation" in subsystem:
        return "regulation"

    # 4) Name / product fallback
    text = f.get("product", "").lower() + " " + f.get("name", "").lower()

    if any(k in text for k in ["transporter", "permease", "channel", "pump"]):
        return "transport"
    if any(k in text for k in ["synthase", "synthetase", "ligase"]):
        return "biosynthesis"
    if any(k in text for k in ["dehydrogenase", "isomerase", "kinase", "oxidase"]):
        return "core_metabolism"
    if any(k in text for k in ["regulator", "repressor", "activator"]):
        return "regulation"

    # 5) Fallback
    return "other_functions"


def assign_color(category):
    return DEFAULT_COLORS.get(category, DEFAULT_COLORS["unassigned"])


def features_to_blocks(features):
    """
    Convert parsed gene features into drawable blocks.
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
