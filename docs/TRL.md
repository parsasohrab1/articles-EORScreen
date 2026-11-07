# Technology readiness

**Level: TRL 4.** TRL 5 is not claimed.

The screen runs offline on published field and project rows. The numbers are deposited central values, including ranges and censored viscosities. There is no operator trial and no second field campaign.

| Level | Status | Evidence |
|---|---|---|
| TRL 1–3 | done | Field-group split, L2 multinomial logistic regression, split-conformal sets, and the 1997 numeric limits are in `src/eorscreen`. |
| TRL 4 | reached | One offline run on the public table. Counts are in `research/results.json`. |
| TRL 5 | not reached | No use by an operator, and the deposit does not include the case-level source table. |
| TRL 6+ | not reached | No deployment. |

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

The nominal coverage is the reference level of the sets. The pooled fraction is the description of these six folds.
