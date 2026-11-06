# Data licence

## Used

| Item | Record |
|---|---|
| File | `EOR_36Case_Processed_Analytical_Dataset_v1.csv` |
| SHA-256 | `d2c1b1171d6e04f04b79d5240d6829a1abb25db8318021009efc77a463104dc9` |
| Title | Processed Field-Experience Dataset for Explainable Machine-Learning EOR-Family Screening |
| DOI | [10.17632/8wfntyb7v4.1](https://doi.org/10.17632/8wfntyb7v4.1) |
| Authors | Oritom Hezekiah-Braye; Edet Emmanuel Aniedi |
| Licence | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| Retrieved | 6 November 2026, from the Mendeley Data public file URL |

The file is the deposited CSV, including its byte-order mark. This repository does not change any value.

Each row is one field or project, with central porosity, permeability, depth, temperature, API gravity, and oil viscosity, plus the EOR family that was implemented (Chemical, Gas, or Thermal). Rows can be marked as a range or as a censored value. Those flags are counted in `research/results.json`. The authors' case-level source table is not in the deposit, so this repository does not re-check each number against the original papers. The label is the process that was implemented, not a claim that it was the best process.

## Not used

| Source | Why it was not used |
|---|---|
| USGS data release [10.5066/P9AG37KI](https://doi.org/10.5066/P9AG37KI), CC0 | Reservoir-level CO2-EOR recovery results for 3,524 reservoirs. Names and reservoir descriptions from the Nehring database are withheld, so the file has no porosity, permeability, or viscosity to put next to a screening table. |
| Zenodo [10.5281/zenodo.20617349](https://doi.org/10.5281/zenodo.20617349), CC BY 4.0 | The CSV named for Alvarado and Manrique, SPE-143326, uses names such as Field-180, pairs formations with the wrong basins, and has spud dates after 2010. It is not that paper's field table. |
| Oil & Gas Journal EOR survey | The survey is not an open dataset. |
| polymer-flooding.com field-case PDF | The page does not state a licence. |
| Alberta Innovative Energy Technologies Program reports, Open Government Licence | Individual project PDFs are public. They are not one machine-readable table of many projects with both reservoir properties and an outcome. Numbers from those PDFs were not typed into a new table. |
