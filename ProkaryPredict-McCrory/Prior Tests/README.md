# ProkaryPredict

**ProkaryPredict** is a Python-based metabolic engineering tool designed
to simulate gene knockouts and cross-species replacements in prokaryotic
genomes using genome-scale metabolic models (GEMs). It aims to be both
**research-grade** and **user-friendly**, making predictive metabolic
engineering accessible to researchers and students alike.

------------------------------------------------------------------------

## Features

-   **Genome-Scale Modeling**: Load and analyze GEMs in SBML format.
-   **Gene Knockout Simulation**: Predict growth rate changes after
    single-gene deletions.
-   **Gene-Reaction Mapping**: Automatically link genes to metabolic
    reactions.
-   **Data Handling**: Easily extract gene and reaction data into CSVs
    for downstream analysis.
-   **Extensible Design**: Support for multiple prokaryotic organisms,
    starting with *Synechocystis sp. PCC 6803*.

------------------------------------------------------------------------

## Project Structure

    prokarypredict/
      data/         # Input files: GEMs, genome FASTAs
      notebooks/    # Jupyter notebooks for analysis
      scripts/      # Python scripts for automation
      results/      # Output CSVs, analysis results
      README.md     # Project documentation (this file)

------------------------------------------------------------------------

## Requirements

-   Python 3.9+
-   [COBRApy](https://github.com/opencobra/cobrapy) for GEM handling
-   [Biopython](https://biopython.org/) for sequence parsing
-   pandas for data management
-   Jupyter Notebook for interactive workflows

Install dependencies:

``` bash
pip install cobra biopython pandas jupyterlab
```

------------------------------------------------------------------------

## Usage

### 1. Load a GEM

``` python
import cobra
model = cobra.io.read_sbml_model("data/iSynCJ816.xml")
```

### 2. Gene-Reaction Mapping

``` python
gene_rxn_map = {gene.id: [rxn.id for rxn in gene.reactions] for gene in model.genes}
```

### 3. Knock Out a Gene

``` python
with model:
    gene = model.genes.get_by_id("gene_id_here")
    gene.knock_out()
    solution = model.optimize()
    print("Growth rate after knockout:", solution.objective_value)
```

## Roadmap

-   Expand to additional organisms (*E. coli*, *B. subtilis*)
-   Implement cross-species gene replacement simulation
-   Add GUI or "block-code" editing interface for non-programmers
-   Connect to public GEM repositories for automated model imports

------------------------------------------------------------------------

## License

MIT License (modify as needed).

------------------------------------------------------------------------

## Citation

If you use this tool in your research, please cite appropriately (to be
added later).
