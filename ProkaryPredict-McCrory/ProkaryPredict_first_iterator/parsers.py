# parsers.py
from Bio import SeqIO
import io
import cobra

def parse_fasta(handle):
    records = list(SeqIO.parse(handle, "fasta"))
    results = []
    for r in records:
        results.append({
            "id": r.id,
            "name": getattr(r, "name", r.id),
            "description": r.description,
            "sequence": str(r.seq),
            "length": len(r.seq),
            "source": "fasta"
        })
    return results

def parse_genbank(handle):
    records = list(SeqIO.parse(handle, "genbank"))
    results = []
    for r in records:
        for feat in r.features:
            if feat.type in ("gene", "CDS", "rRNA", "tRNA"):
                gene_name = None
                qualifiers = feat.qualifiers
                if "gene" in qualifiers:
                    gene_name = qualifiers.get("gene")[0]
                elif "locus_tag" in qualifiers:
                    gene_name = qualifiers.get("locus_tag")[0]
                prod = qualifiers.get("product", [""])[0]
                seq_len = int(len(feat.location))
                results.append({
                    "id": qualifiers.get("locus_tag", [f"{r.id}_{len(results)}"])[0],
                    "name": gene_name or qualifiers.get("locus_tag", ["unknown"])[0],
                    "product": prod,
                    "start": int(feat.location.start),
                    "end": int(feat.location.end),
                    "length": seq_len,
                    "type": feat.type,
                    "source": "genbank",
                    "qualifiers": qualifiers
                })
    return results

def parse_sbml(file_like):
    try:
        model = cobra.io.read_sbml_model(file_like)
    except Exception:
        file_like.seek(0)
        model = cobra.io.read_sbml_model(io.StringIO(file_like.read().decode("utf-8")))
    genes = [{"id": g.id, "name": g.name or g.id, "notes": g.notes, "reactions":[r.id for r in g.reactions], "source":"sbml"} for g in model.genes]
    reactions = [{"id": r.id, "name": r.name or r.id, "bounds":(r.lower_bound, r.upper_bound), "genes":[g.id for g in r.genes], "source":"sbml"} for r in model.reactions]
    return {"genes": genes, "reactions": reactions}