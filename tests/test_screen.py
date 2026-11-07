import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pytest

from eorscreen.criteria import families_passing, methods_passing
from eorscreen.model import conformal_threshold, fit_softmax, predict_proba
from eorscreen.report import abstract_text, manuscript_text, measured_block
from eorscreen.split import assign_folds, field_groups, roles_for_fold
from eorscreen.study import DATA_SHA256, load_rows, run

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "EOR_36Case_Processed_Analytical_Dataset_v1.csv"


def test_deposited_file_hash_is_unchanged():
    assert hashlib.sha256(DATA.read_bytes()).hexdigest() == DATA_SHA256


def test_one_row_per_field_and_logarithms_match():
    rows = load_rows(DATA)
    assert len(rows) == len({row["field_group"] for row in rows})
    assert {row["family"] for row in rows} == {"Chemical", "Gas", "Thermal"}
    for row in rows:
        assert math.log10(row["k_md"]) == pytest.approx(row["deposited_log10_k"], rel=1e-9, abs=1e-9)
        assert math.log10(row["mu_cp"]) == pytest.approx(row["deposited_log10_mu"], rel=1e-9, abs=1e-9)


def test_field_group_is_not_split_across_roles():
    rows = [
        {"case_id": "a1", "field_group": "A", "family": "Gas"},
        {"case_id": "a2", "field_group": "A", "family": "Gas"},
        {"case_id": "b1", "field_group": "B", "family": "Gas"},
        {"case_id": "c1", "field_group": "C", "family": "Chemical"},
        {"case_id": "d1", "field_group": "D", "family": "Thermal"},
    ]
    groups = field_groups(rows)
    assert len(groups) == 4
    fold_of = assign_folds(groups, n_folds=2)
    assert fold_of["A"] == fold_of["A"]
    for test_fold in (0, 1):
        train, calibration, test = roles_for_fold(groups, fold_of, test_fold)
        names = []
        for bucket in (train, calibration, test):
            bucket_names = [group["field_group"] for group in bucket]
            assert len(bucket_names) == len(set(bucket_names))
            names.extend(bucket_names)
        assert sorted(names) == ["A", "B", "C", "D"]


def test_criteria_limits_on_constructed_reservoirs():
    light = {"api": 36, "mu_cp": 1.5, "k_md": 100, "depth_ft": 5000, "temp_f": 150}
    assert "co2_miscible" in methods_passing(light)
    assert "steam" not in methods_passing(light)
    assert families_passing(light) == ["Chemical", "Gas", "Thermal"]
    heavy = {"api": 13, "mu_cp": 2000, "k_md": 2000, "depth_ft": 1000, "temp_f": 90}
    assert families_passing(heavy) == ["Thermal"]
    assert methods_passing(heavy) == ["steam"]


def test_conformal_rank_matches_the_finite_sample_rule():
    scores = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    assert conformal_threshold(scores, 0.10) == 1.0
    assert conformal_threshold(np.array([0.2, 0.4, 0.6, 0.8]), 0.10) == math.inf


def test_softmax_separates_a_linear_problem():
    features = np.array(
        [
            [0.0, 0.0],
            [0.1, -0.1],
            [-0.2, 0.1],
            [3.0, 3.0],
            [3.2, 2.8],
            [2.7, 3.1],
            [-3.0, 3.0],
            [-2.8, 3.2],
            [-3.1, 2.9],
        ]
    )
    target = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2])
    weights, bias = fit_softmax(features, target, 3)
    predicted = predict_proba(features, weights, bias).argmax(axis=1)
    assert np.array_equal(predicted, target)


def test_results_file_is_the_script_output():
    fresh = run(DATA)
    saved = json.loads((ROOT / "research" / "results.json").read_text(encoding="utf-8"))
    assert fresh == saved
    assert fresh["test"]["n"] == len(fresh["projects"])
    families = [row["EOR_Family"] for row in csv.DictReader(DATA.open(encoding="utf-8-sig"))]
    assert [fresh["test"]["by_family"][name]["n"] for name in ("Chemical", "Gas", "Thermal")] == [
        families.count("Chemical"),
        families.count("Gas"),
        families.count("Thermal"),
    ]
    for project in fresh["projects"]:
        total = sum(project["probability"].values())
        assert total == pytest.approx(1.0, abs=1e-8)
        assert project["set_contains_historical"] == (
            project["historical_family"] in project["conformal_set"]
        )


def test_article_text_is_the_script_output_and_the_abstract_length_fits():
    fresh = run(DATA)
    block = measured_block(fresh)
    for relative in (
        "README.md",
        "docs/JOURNAL_FIT.md",
        "docs/TRL.md",
        "docs/ACHIEVEMENTS.md",
    ):
        assert block in (ROOT / relative).read_text(encoding="utf-8")
    abstract = abstract_text(fresh)
    words = abstract.split()
    assert 200 <= len(words) <= 400
    assert abstract in (ROOT / "article" / "abstract.md").read_text(encoding="utf-8")
    assert (ROOT / "article" / "manuscript.txt").read_text(encoding="utf-8") == manuscript_text(
        fresh
    )
