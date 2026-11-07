"""Article and achievement text. Every count is taken from the study payload."""

from __future__ import annotations

from pathlib import Path

START = "<!-- results:start -->"
END = "<!-- results:end -->"
FAMILIES = ("Chemical", "Gas", "Thermal")


def _ratio(count: int, n: int) -> str:
    return f"{count}/{n} ({count / n:.4f})"


def measured_block(payload: dict) -> str:
    data = payload["data"]
    test = payload["test"]
    procedure = payload["procedure"]
    contained = test["conformal_contains_historical"]
    point = test["point_matches_historical"]
    rule = test["rule_contains_historical"]
    exact = test["rule_exact"]
    lines = [
        (
            f"Field groups {data['n_field_groups']}. Rows {data['n_rows']}. "
            f"Range flags {data['n_range_flag']}. Censored values {data['n_censor_flag']}."
        ),
        f"Nominal coverage {procedure['nominal_coverage']:.4f}.",
        (
            "Conformal set contains the historical family on "
            f"{_ratio(contained['count'], contained['n'])}. "
            f"Mean set size {test['mean_set_size']:.4f}. Empty sets {test['n_empty_sets']}."
        ),
        (
            "Point family matches the historical family on "
            f"{_ratio(point['count'], point['n'])}."
        ),
        (
            "The 1997 limits contain the historical family on "
            f"{_ratio(rule['count'], rule['n'])} and return that family alone on "
            f"{_ratio(exact['count'], exact['n'])}."
        ),
    ]
    for name in FAMILIES:
        row = test["by_family"][name]
        lines.append(
            f"{name}: conformal {row['conformal_contains']}/{row['n']}, "
            f"point {row['point_matches']}/{row['n']}, "
            f"rule contains {row['rule_contains']}/{row['n']}, "
            f"rule alone {row['rule_exact']}/{row['n']}."
        )
    return "\n".join(lines)


def abstract_text(payload: dict) -> str:
    """Research abstract. No citations. Word count is checked by the tests."""
    data = payload["data"]
    test = payload["test"]
    contained = test["conformal_contains_historical"]
    point = test["point_matches_historical"]
    rule = test["rule_contains_historical"]
    exact = test["rule_exact"]
    chemical = test["by_family"]["Chemical"]
    gas = test["by_family"]["Gas"]
    thermal = test["by_family"]["Thermal"]
    paragraphs = [
        (
            "This note screens historical enhanced-oil-recovery families on one public "
            "table of field and project rows. The table is the processed dataset "
            f"deposited by Hezekiah-Braye and Aniedi, Mendeley Data {data['doi']}, "
            f"under {data['license']}. Each row is one field group. The label is the "
            "family that was implemented: chemical, gas, or thermal. The table does "
            "not say that this family was optimal. Range flags and censored viscosities "
            "are kept. The case-level source list is not in the deposit."
        ),
        (
            "Field groups are stratified by family into six folds. A group stays in "
            "one of train, calibration, and test. An L2 multinomial logistic regression "
            "is fit on the training groups. Features are porosity, log10 permeability, "
            "depth, temperature, API gravity, and log10 oil viscosity. The score of a "
            "candidate family is one minus its probability. The set keeps every family "
            "at or below the split-conformal rank ceil((n_cal+1)*0.90), the "
            "finite-sample rule for nominal coverage 0.90. On this file that rank is "
            "the largest calibration score. Coverage pooled over folds describes this "
            "run and is not a second guarantee."
        ),
        (
            "The comparison uses the 1997 recommended limits for API gravity, viscosity, "
            "permeability, depth, and temperature. Oil saturation, composition, "
            "formation type, and net thickness are absent, so they are not applied. "
            "A pass on the available limits is not a full screen and not a recovery design."
        ),
        (
            f"There are {data['n_rows']} rows and {data['n_field_groups']} field groups, "
            f"{data['n_range_flag']} range flags, and {data['n_censor_flag']} censored "
            "values. The set contains the historical family on "
            f"{_ratio(contained['count'], contained['n'])}. Mean set size "
            f"{test['mean_set_size']:.4f}. Empty sets {test['n_empty_sets']}. "
            "The point family matches on "
            f"{_ratio(point['count'], point['n'])}. The 1997 limits contain the "
            f"historical family on {_ratio(rule['count'], rule['n'])} and return it "
            f"alone on {_ratio(exact['count'], exact['n'])}. "
            f"Chemical: conformal {chemical['conformal_contains']}/{chemical['n']}, "
            f"point {chemical['point_matches']}/{chemical['n']}, "
            f"rule contains {chemical['rule_contains']}/{chemical['n']}, "
            f"rule alone {chemical['rule_exact']}/{chemical['n']}. "
            f"Gas: conformal {gas['conformal_contains']}/{gas['n']}, "
            f"point {gas['point_matches']}/{gas['n']}, "
            f"rule contains {gas['rule_contains']}/{gas['n']}, "
            f"rule alone {gas['rule_exact']}/{gas['n']}. "
            f"Thermal: conformal {thermal['conformal_contains']}/{thermal['n']}, "
            f"point {thermal['point_matches']}/{thermal['n']}, "
            f"rule contains {thermal['rule_contains']}/{thermal['n']}, "
            f"rule alone {thermal['rule_exact']}/{thermal['n']}."
        ),
        (
            "The chemical point guess is the weak row: it rarely names chemical, while "
            "gas and thermal point guesses match most held-out projects in those groups. "
            "The 1997 polymer viscosity window is narrow beside heavy-oil polymer rows "
            "in the table. The set is wider than the point guess and still misses some "
            "chemical projects. This text has not been uploaded."
        ),
    ]
    return "\n\n".join(paragraphs)


def manuscript_text(payload: dict) -> str:
    omitted = ", ".join(payload["procedure"]["criteria_omitted"])
    body = [
        "Field-grouped sets for historical enhanced-oil-recovery families",
        "",
        "Abstract",
        "",
        abstract_text(payload),
        "",
        "1. Data",
        "",
        (
            "The rows are the deposited CSV named in data/DATA_LICENSE.md. "
            f"The file hash recorded by the study is {payload['data']['sha256']}. "
            "Values are the deposited central numbers. This repository does not "
            "replace a range or a censored viscosity with another number."
        ),
        "",
        "2. Screen",
        "",
        payload["procedure"]["note"],
        "",
        (
            f"Model: {payload['procedure']['model']}. "
            f"Features: {', '.join(payload['procedure']['features'])}. "
            f"Split: {payload['procedure']['split']}. "
            f"Criteria: {payload['procedure']['criteria']}. "
            f"Limits not applied, because the file does not contain them: {omitted}."
        ),
        "",
        "3. Counts",
        "",
        measured_block(payload),
        "",
        "4. Reading",
        "",
        (
            "Read the chemical row next to the gas and thermal rows. A set that "
            "contains the historical family can still be wide. A 1997 pass on the "
            "variables present in the file can include more than one family. "
            "Agreement with the historical family is not evidence that the family "
            "was the best engineering choice, and it is not a field design."
        ),
        "",
        "5. What is withheld",
        "",
        (
            "The manuscript states split-conformal multinomial logistic regression "
            "and the published 1997 numeric limits. It does not state a chemical "
            "formulation or a field operating procedure. It has not been uploaded."
        ),
        "",
        "References",
        "",
        (
            "Hezekiah-Braye, O., Aniedi, E.E. Processed field-experience dataset for "
            "explainable machine-learning EOR-family screening. Mendeley Data, "
            f"{payload['data']['doi']}, {payload['data']['license']}."
        ),
        "",
        (
            "Taber, J.J., Martin, F.D., Seright, R.S., 1997. EOR screening criteria "
            "revisited—Part 1. SPE Reservoir Engineering 12 (3), 189–198. SPE-35385."
        ),
        "",
        (
            "Vovk, V., Gammerman, A., Shafer, G., 2005. Algorithmic Learning in a "
            "Random World. Springer."
        ),
        "",
        (
            "Acknowledgement. Wording was assembled from the study output so that "
            "every count matches research/results.json. Routine editing assistance "
            "was used. The measurement itself is the executed script."
        ),
        "",
    ]
    return "\n".join(body)


def fill_marked(path: Path, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise ValueError(f"missing results markers in {path}")
    pre, rest = text.split(START, 1)
    _, post = rest.split(END, 1)
    updated = f"{pre}{START}\n{block.rstrip()}\n{END}{post}"
    path.write_text(updated, encoding="utf-8", newline="\n")
