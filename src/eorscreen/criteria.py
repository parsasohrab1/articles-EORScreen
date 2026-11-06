"""Recommended numeric limits from Taber, Martin, and Seright (1997), Table 3.

The bound is the recommended limit, not the mean of projects then underway.
Oil saturation, composition, formation type, and net thickness are omitted:
the public file does not contain them. A pass is only a pass on the limits below.

Source of the bounds: Taber, J.J., Martin, F.D., Seright, R.S., 1997. EOR screening
criteria revisited—Part 1. SPE Reservoir Engineering 12 (3), 189–198. SPE-35385.
The same recommended bounds are reproduced in Scientific Reports table 1 of
doi:10.1038/s41598-025-21696-x (CC BY 4.0).
"""

from __future__ import annotations

FAMILY_ORDER = ("Chemical", "Gas", "Thermal")

# (feature, operator, limit). Every gate must hold.
METHODS: dict[str, tuple[str, tuple[tuple[str, str, float], ...]]] = {
    "nitrogen_flue": ("Gas", (("api", ">", 35), ("mu_cp", "<", 0.4), ("depth_ft", ">", 6000))),
    "hydrocarbon_miscible": (
        "Gas",
        (("api", ">", 23), ("mu_cp", "<", 3), ("depth_ft", ">", 4000)),
    ),
    "co2_miscible": ("Gas", (("api", ">", 22), ("mu_cp", "<", 10), ("depth_ft", ">", 2500))),
    "immiscible_gas": ("Gas", (("api", ">", 12), ("mu_cp", "<", 600), ("depth_ft", ">", 1800))),
    "micellar_asp_alkaline": (
        "Chemical",
        (
            ("api", ">", 20),
            ("mu_cp", "<", 35),
            ("k_md", ">", 10),
            ("depth_ft", "<", 9000),
            ("temp_f", "<", 200),
        ),
    ),
    "polymer": (
        "Chemical",
        (
            ("api", ">", 15),
            ("mu_cp", ">", 10),
            ("mu_cp", "<", 150),
            ("k_md", ">", 10),
            ("depth_ft", "<", 9000),
            ("temp_f", "<", 200),
        ),
    ),
    "combustion": (
        "Thermal",
        (
            ("api", ">", 10),
            ("mu_cp", "<", 5000),
            ("k_md", ">", 50),
            ("depth_ft", "<", 11500),
            ("temp_f", ">", 100),
        ),
    ),
    "steam": (
        "Thermal",
        (("api", ">", 8), ("mu_cp", "<", 200_000), ("k_md", ">", 200), ("depth_ft", "<", 4500)),
    ),
}

OMITTED = (
    "oil_saturation",
    "composition",
    "formation_type",
    "net_thickness",
)


def _holds(value: float, op: str, limit: float) -> bool:
    if op == ">":
        return value > limit
    if op == "<":
        return value < limit
    raise ValueError(op)


def methods_passing(features: dict[str, float]) -> list[str]:
    passed = []
    for name, (_family, gates) in METHODS.items():
        if all(_holds(features[key], op, limit) for key, op, limit in gates):
            passed.append(name)
    return sorted(passed)


def families_passing(features: dict[str, float]) -> list[str]:
    hit = {METHODS[name][0] for name in methods_passing(features)}
    return [family for family in FAMILY_ORDER if family in hit]
