# articles-EORScreen

Field-grouped screen of historical enhanced-oil-recovery families, with split-conformal sets, compared with the recommended numeric limits in Taber, Martin, and Seright (1997).

**Maturity: TRL 4.** The screen has been run on the public 36-project table. There is no operator trial. See [docs/TRL.md](docs/TRL.md) and [docs/ACHIEVEMENTS.md](docs/ACHIEVEMENTS.md).

**Not uploaded.** The target call is the TechScience ENERGY special issue on sustainable and intelligent petroleum engineering, deadline 1 February 2027. The power-systems issue with the same deadline is a different call. The fit note is [docs/JOURNAL_FIT.md](docs/JOURNAL_FIT.md). The manuscript text is [article/manuscript.txt](article/manuscript.txt). Upload waits for a patent attorney. Nothing has been uploaded.

## Data

One row per field group, from Mendeley Data [10.17632/8wfntyb7v4.1](https://doi.org/10.17632/8wfntyb7v4.1), CC BY 4.0. Hezekiah-Braye, O. and Aniedi, E.E. The label is the family that was implemented: Chemical, Gas, or Thermal. Licence notes are in [data/DATA_LICENSE.md](data/DATA_LICENSE.md).

## What the run does

Projects are stratified by family and split into six folds. A field group is entirely in train, calibration, or test. An L2 multinomial logistic regression is fit on the training projects of each fold. The nonconformity score is one minus the probability of a candidate family. The 90 percent split-conformal set uses the finite-sample rank `ceil((n_cal+1)*0.9)`.

The comparison rule applies only the 1997 recommended limits for API gravity, viscosity, permeability, depth, and temperature. Oil saturation, composition, formation type, and net thickness are not in the file, so they are not applied.

## Measured result

<!-- results:start -->
Field groups 36. Rows 36. Range flags 23. Censored values 3.
Nominal coverage 0.9000.
Conformal set contains the historical family on 33/36 (0.9167). Mean set size 1.8333. Empty sets 0.
Point family matches the historical family on 26/36 (0.7222).
The 1997 limits contain the historical family on 27/36 (0.7500) and return that family alone on 10/36 (0.2778).
Chemical: conformal 8/11, point 2/11, rule contains 6/11, rule alone 0/11.
Gas: conformal 12/12, point 12/12, rule contains 11/12, rule alone 1/12.
Thermal: conformal 13/13, point 12/13, rule contains 10/13, rule alone 9/13.
<!-- results:end -->

Every count above and in [research/results.json](research/results.json) is written by `research/run_study.py`.

Docs: [BRS](docs/BRS.md) · [SRS](docs/SRS.md) · [TRL](docs/TRL.md) · [achievements](docs/ACHIEVEMENTS.md) · [submission sheet](docs/SUBMISSION.md)

```bash
pip install -e ".[dev]"
ruff check src tests research
python -m pytest -q
python research/run_study.py
```
