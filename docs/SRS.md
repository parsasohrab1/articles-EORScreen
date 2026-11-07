# Software requirements — EORScreen

Laboratory scope: reproduce one field-grouped screen on the deposited CSV and write the measured counts.

| ID | Requirement | Satisfied by |
|---|---|---|
| FR-01 | Stop if the CSV bytes differ from the pinned SHA-256. | `load_rows` |
| FR-02 | Record CC BY 4.0 and the sources that were not used. | `data/DATA_LICENSE.md` |
| FR-03 | Treat the field group as the split unit. A group is not divided across roles. | `field_groups`, `roles_for_fold` |
| FR-04 | Fit L2 multinomial logistic regression on training groups only, with standardization fit on those groups. | `study.run` |
| FR-05 | Build the 90 percent split-conformal set with rank `ceil((n_cal+1)*(1-alpha))`. | `conformal_threshold` |
| FR-06 | Score the 1997 recommended numeric limits on API gravity, viscosity, permeability, depth, and temperature. | `families_passing` |
| FR-07 | Write `research/results.json` and regenerate the marked blocks, the abstract, and `article/manuscript.txt` from that object. | `research/run_study.py` |

The software does not impute a missing reservoir property and does not replace a censored viscosity.
