"""Project holdout. A field group is never split across train, calibration, and test."""

from __future__ import annotations

N_FOLDS = 6


def field_groups(rows: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = {}
    for row in rows:
        grouped.setdefault(row["field_group"], []).append(row)
    groups = []
    for name, members in grouped.items():
        families = {member["family"] for member in members}
        if len(families) != 1:
            raise ValueError(f"{name} has more than one EOR family")
        groups.append(
            {
                "field_group": name,
                "family": families.pop(),
                "members": sorted(members, key=lambda row: row["case_id"]),
            }
        )
    return sorted(groups, key=lambda group: group["field_group"])


def assign_folds(groups: list[dict], n_folds: int = N_FOLDS) -> dict[str, int]:
    by_family: dict[str, list[dict]] = {}
    for group in groups:
        by_family.setdefault(group["family"], []).append(group)
    fold_of: dict[str, int] = {}
    for family in sorted(by_family):
        ordered = sorted(by_family[family], key=lambda group: group["field_group"])
        for index, group in enumerate(ordered):
            fold_of[group["field_group"]] = index % n_folds
    return fold_of


def roles_for_fold(
    groups: list[dict], fold_of: dict[str, int], test_fold: int
) -> tuple[list[dict], list[dict], list[dict]]:
    """Within each family in the complement, every third project (index 2, 5, ...) is calibration."""
    test = [group for group in groups if fold_of[group["field_group"]] == test_fold]
    complement = [group for group in groups if fold_of[group["field_group"]] != test_fold]
    by_family: dict[str, list[dict]] = {}
    for group in complement:
        by_family.setdefault(group["family"], []).append(group)
    train: list[dict] = []
    calibration: list[dict] = []
    for family in sorted(by_family):
        ordered = sorted(by_family[family], key=lambda group: group["field_group"])
        for index, group in enumerate(ordered):
            if index % 3 == 2:
                calibration.append(group)
            else:
                train.append(group)
    return train, calibration, test
