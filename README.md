# articles-EORScreen

Field-grouped screen of historical enhanced-oil-recovery families, with split-conformal sets, compared with the recommended numeric limits in Taber, Martin, and Seright (1997).

**Not a submission.** The TechScience ENERGY special issue with deadline 1 February 2027 is about next-generation power systems. The fit note is [docs/JOURNAL_FIT.md](docs/JOURNAL_FIT.md). No manuscript is uploaded. A patent attorney has not reviewed a submission because there is none.

## Data

36 field or project rows, one row per field group, from Mendeley Data [10.17632/8wfntyb7v4.1](https://doi.org/10.17632/8wfntyb7v4.1), CC BY 4.0. Hezekiah-Braye, O. and Aniedi, E.E. The label is the family that was implemented: Chemical, Gas, or Thermal. Licence notes and the sources that were rejected are in [data/DATA_LICENSE.md](data/DATA_LICENSE.md).

## What the run does

Projects are stratified by family and split into six folds. A field group is entirely in train, calibration, or test. An L2 multinomial logistic regression is fit on the training projects of each fold. The nonconformity score is one minus the probability of a candidate family. The 90 percent split-conformal set uses the finite-sample rank `ceil((n_cal+1)*0.9)`.

The comparison rule applies only the 1997 recommended limits for API gravity, viscosity, permeability, depth, and temperature. Oil saturation, composition, formation type, and net thickness are not in the file, so they are not applied. A pass on that subset is not a full screening decision.

Every count in [research/results.json](research/results.json) is written by `research/run_study.py`.

```bash
pip install -e ".[dev]"
ruff check src tests research
python -m pytest -q
python research/run_study.py
```
