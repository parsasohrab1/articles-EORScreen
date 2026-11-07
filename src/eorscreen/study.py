"""Run the field-grouped screen and the criteria-table comparison."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

import numpy as np

from eorscreen.criteria import FAMILY_ORDER, OMITTED, families_passing, methods_passing
from eorscreen.model import (
    ALPHA,
    FEATURE_NAMES,
    L2,
    conformal_threshold,
    design,
    fit_softmax,
    labels,
    predict_proba,
    prediction_set,
    standardize,
)
from eorscreen.split import N_FOLDS, assign_folds, field_groups, roles_for_fold

DATA_DOI = "10.17632/8wfntyb7v4.1"
DATA_LICENSE = "CC BY 4.0"
DATA_SHA256 = "d2c1b1171d6e04f04b79d5240d6829a1abb25db8318021009efc77a463104dc9"

NOTE = (
    "Each field group is held out in one fold. Within the complement, every third "
    "project inside a family is the calibration set and the rest fit an L2 multinomial "
    "logistic regression. The 90 percent split-conformal rule uses rank "
    "ceil((n_cal+1)*0.9). At the calibration sizes in this file that rank is the "
    "largest calibration score, so a set contains every family whose score is no larger "
    "than that value. Pooled coverage describes these folds; it is not a second guarantee. "
    "The historical family is the process that was implemented, not a proof that it was "
    "the best process. The criteria rule applies only the 1997 recommended numeric limits "
    "for variables present in the file."
)


def load_rows(path: Path) -> list[dict]:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != DATA_SHA256:
        raise ValueError(f"unexpected file hash {digest}")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        raw_rows = list(csv.DictReader(handle))
    rows = []
    for raw in raw_rows:
        row = {
            "case_id": raw["Case_ID"],
            "field": raw["Field"],
            "field_group": raw["Field_Group"],
            "family": raw["EOR_Family"],
            "historical_method": raw["Historical_EOR_Method"],
            "phi_pct": float(raw["Phi_Central"]),
            "k_md": float(raw["K_Central_mD"]),
            "depth_ft": float(raw["Depth_Central_ft"]),
            "temp_f": float(raw["Temp_Central_F"]),
            "api": float(raw["API_Central"]),
            "mu_cp": float(raw["Mu_Central_cP"]),
            "range_flag": raw["Range_Flag"] == "YES",
            "censor_flag": raw["Censor_Flag"] == "YES",
            "deposited_log10_k": float(raw["log10_K_Central"]),
            "deposited_log10_mu": float(raw["log10_Mu_Central"]),
        }
        if row["family"] not in FAMILY_ORDER:
            raise ValueError(row["case_id"])
        rows.append(row)
    return rows


def _features(member: dict) -> dict[str, float]:
    return {
        "api": member["api"],
        "mu_cp": member["mu_cp"],
        "k_md": member["k_md"],
        "depth_ft": member["depth_ft"],
        "temp_f": member["temp_f"],
    }


def _freeze(value):
    if isinstance(value, dict):
        return {key: _freeze(value[key]) for key in value}
    if isinstance(value, (list, tuple)):
        return [_freeze(item) for item in value]
    if isinstance(value, (np.floating, float)):
        number = float(value)
        if not np.isfinite(number):
            return None
        return round(number, 10)
    if isinstance(value, (np.integer, int)) and not isinstance(value, bool):
        return int(value)
    if isinstance(value, (np.bool_, bool)):
        return bool(value)
    if isinstance(value, str):
        return value
    raise TypeError(type(value))


def run(path: Path) -> dict:
    rows = load_rows(path)
    groups = field_groups(rows)
    if any(len(group["members"]) != 1 for group in groups):
        raise ValueError("this file is required to have one row per field group")
    fold_of = assign_folds(groups)
    class_names = FAMILY_ORDER
    projects = []
    folds = []
    for test_fold in range(N_FOLDS):
        train, calibration, test = roles_for_fold(groups, fold_of, test_fold)
        present = {group["family"] for group in train}
        if present != set(class_names):
            raise ValueError(f"fold {test_fold} train set misses a family")
        x_train, (x_cal, x_test) = _scale(train, calibration, test)
        y_train = labels(train, class_names)
        y_cal = labels(calibration, class_names)
        weights, bias = fit_softmax(x_train, y_train, len(class_names))
        cal_proba = predict_proba(x_cal, weights, bias)
        cal_scores = 1.0 - cal_proba[np.arange(len(calibration)), y_cal]
        threshold = conformal_threshold(cal_scores, ALPHA)
        test_proba = predict_proba(x_test, weights, bias)
        folds.append(
            {
                "test_fold": test_fold,
                "n_train": len(train),
                "n_calibration": len(calibration),
                "n_test": len(test),
                "threshold": None if threshold == np.inf else threshold,
                "threshold_is_maximum_calibration_score": bool(
                    np.isfinite(threshold) and threshold == float(np.max(cal_scores))
                ),
            }
        )
        order = np.argsort([group["field_group"] for group in test])
        for position in order:
            group = test[int(position)]
            member = group["members"][0]
            probabilities = test_proba[int(position)]
            point = class_names[int(np.argmax(probabilities))]
            chosen = prediction_set(probabilities, class_names, threshold)
            rule_methods = methods_passing(_features(member))
            rule_families = families_passing(_features(member))
            projects.append(
                {
                    "case_id": member["case_id"],
                    "field_group": group["field_group"],
                    "historical_family": group["family"],
                    "historical_method": member["historical_method"],
                    "test_fold": test_fold,
                    "censor_flag": member["censor_flag"],
                    "range_flag": member["range_flag"],
                    "probability": {
                        name: float(probabilities[index]) for index, name in enumerate(class_names)
                    },
                    "point_family": point,
                    "conformal_set": chosen,
                    "set_contains_historical": group["family"] in chosen,
                    "point_matches_historical": point == group["family"],
                    "rule_methods": rule_methods,
                    "rule_families": rule_families,
                    "rule_contains_historical": group["family"] in rule_families,
                    "rule_exact": rule_families == [group["family"]],
                }
            )
    projects.sort(key=lambda project: project["case_id"])
    return _freeze(_summary(rows, projects, folds))


def _scale(train, calibration, test):
    x_train = design(train)
    x_cal = design(calibration)
    x_test = design(test)
    x_train, (x_cal, x_test) = standardize(x_train, [x_cal, x_test])
    return x_train, (x_cal, x_test)


def _rate(projects: list[dict], key: str) -> dict:
    return {"count": sum(1 for project in projects if project[key]), "n": len(projects)}


def _summary(rows: list[dict], projects: list[dict], folds: list[dict]) -> dict:
    by_family = {}
    for family in FAMILY_ORDER:
        subset = [project for project in projects if project["historical_family"] == family]
        by_family[family] = {
            "n": len(subset),
            "conformal_contains": sum(1 for project in subset if project["set_contains_historical"]),
            "point_matches": sum(1 for project in subset if project["point_matches_historical"]),
            "rule_contains": sum(1 for project in subset if project["rule_contains_historical"]),
            "rule_exact": sum(1 for project in subset if project["rule_exact"]),
        }
    sizes = [len(project["conformal_set"]) for project in projects]
    return {
        "data": {
            "doi": DATA_DOI,
            "license": DATA_LICENSE,
            "sha256": DATA_SHA256,
            "n_rows": len(rows),
            "n_field_groups": len({row["field_group"] for row in rows}),
            "n_range_flag": sum(1 for row in rows if row["range_flag"]),
            "n_censor_flag": sum(1 for row in rows if row["censor_flag"]),
            "label": "historically implemented EOR family",
        },
        "procedure": {
            "split": "field group, stratified by family, six folds",
            "model": "L2 multinomial logistic regression",
            "l2": L2,
            "features": list(FEATURE_NAMES),
            "nominal_coverage": 1 - ALPHA,
            "nonconformity": "1 - probability of the candidate family",
            "criteria": "Taber, Martin, Seright 1997 recommended numeric limits",
            "criteria_omitted": list(OMITTED),
            "note": NOTE,
        },
        "folds": folds,
        "test": {
            "n": len(projects),
            "conformal_contains_historical": _rate(projects, "set_contains_historical"),
            "point_matches_historical": _rate(projects, "point_matches_historical"),
            "rule_contains_historical": _rate(projects, "rule_contains_historical"),
            "rule_exact": _rate(projects, "rule_exact"),
            "mean_set_size": float(np.mean(sizes)),
            "n_empty_sets": sum(1 for size in sizes if size == 0),
            "by_family": by_family,
        },
        "projects": projects,
        "submission": {
            "call": (
                "TechScience ENERGY, Recent Advances in Sustainable and "
                "Intelligent Petroleum Engineering"
            ),
            "deadline": "2027-02-01",
            "decision": "do_not_upload",
            "manuscript_uploaded": False,
            "patent_counsel_review": "not_requested",
            "out_of_scope_call": "TechScience ENERGY, Next-Generation Power Systems",
        },
    }
