# Business requirements — EORScreen

Scope of this release: an offline, reproducible screen of historical enhanced-oil-recovery families on one public project table, with split-conformal sets and a comparison to the 1997 recommended numeric limits. The target discussion venue is the ENERGY special issue on sustainable and intelligent petroleum engineering (deadline 2027-02-01). This document is not a submission.

| ID | Requirement | Evidence |
|---|---|---|
| BR-01 | Use a public project table whose licence has been read and recorded. | `data/DATA_LICENSE.md` |
| BR-02 | Keep each field group inside one of train, calibration, and test. | `src/eorscreen/split.py` |
| BR-03 | Publish set coverage, set size, the point guess, and the 1997 comparison from the script. | `research/results.json` and the generated blocks |
| BR-04 | Apply only published limits, and only for variables present in the file. | `src/eorscreen/criteria.py` |
| BR-05 | Do not disclose methods covered by filed claims in the manuscript. | `docs/JOURNAL_FIT.md`, `docs/SUBMISSION.md` |

Out of scope: a chemical formulation, a gas or steam operating procedure, a reservoir simulation, and an operator trial.
