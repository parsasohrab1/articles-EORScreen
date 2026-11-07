# Abstract draft

**Title:** Field-grouped sets for historical enhanced-oil-recovery families

**Target:** ENERGY special issue, Recent Advances in Sustainable and Intelligent Petroleum Engineering, deadline 1 February 2027. Not uploaded. See `docs/JOURNAL_FIT.md`.

<!-- results:start -->
This note screens historical enhanced-oil-recovery families on one public table of field and project rows. The table is the processed dataset deposited by Hezekiah-Braye and Aniedi, Mendeley Data 10.17632/8wfntyb7v4.1, under CC BY 4.0. Each row is one field group. The label is the family that was implemented: chemical, gas, or thermal. The table does not say that this family was optimal. Range flags and censored viscosities are kept. The case-level source list is not in the deposit.

Field groups are stratified by family into six folds. A group stays in one of train, calibration, and test. An L2 multinomial logistic regression is fit on the training groups. Features are porosity, log10 permeability, depth, temperature, API gravity, and log10 oil viscosity. The score of a candidate family is one minus its probability. The set keeps every family at or below the split-conformal rank ceil((n_cal+1)*0.90), the finite-sample rule for nominal coverage 0.90. On this file that rank is the largest calibration score. Coverage pooled over folds describes this run and is not a second guarantee.

The comparison uses the 1997 recommended limits for API gravity, viscosity, permeability, depth, and temperature. Oil saturation, composition, formation type, and net thickness are absent, so they are not applied. A pass on the available limits is not a full screen and not a recovery design.

There are 36 rows and 36 field groups, 23 range flags, and 3 censored values. The set contains the historical family on 33/36 (0.9167). Mean set size 1.8333. Empty sets 0. The point family matches on 26/36 (0.7222). The 1997 limits contain the historical family on 27/36 (0.7500) and return it alone on 10/36 (0.2778). Chemical: conformal 8/11, point 2/11, rule contains 6/11, rule alone 0/11. Gas: conformal 12/12, point 12/12, rule contains 11/12, rule alone 1/12. Thermal: conformal 13/13, point 12/13, rule contains 10/13, rule alone 9/13.

The chemical point guess is the weak row: it rarely names chemical, while gas and thermal point guesses match most held-out projects in those groups. The 1997 polymer viscosity window is narrow beside heavy-oil polymer rows in the table. The set is wider than the point guess and still misses some chemical projects. This text has not been uploaded. Upload waits until a patent attorney confirms that it discloses no claimed method.
<!-- results:end -->

**Keywords:** enhanced oil recovery; split conformal; field holdout; screening criteria
