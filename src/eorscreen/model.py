"""L2 multinomial logistic regression and split-conformal sets. No random seed."""

from __future__ import annotations

import math

import numpy as np

FEATURE_NAMES = ("phi_pct", "log10_k_md", "depth_ft", "temp_f", "api", "log10_mu_cp")
L2 = 1.0
STEPS = 4000
LEARNING_RATE = 0.35
ALPHA = 0.10


def feature_row(member: dict) -> np.ndarray:
    if member["k_md"] <= 0 or member["mu_cp"] <= 0:
        raise ValueError(member["case_id"])
    return np.array(
        [
            member["phi_pct"],
            math.log10(member["k_md"]),
            member["depth_ft"],
            member["temp_f"],
            member["api"],
            math.log10(member["mu_cp"]),
        ],
        dtype=float,
    )


def design(groups: list[dict]) -> np.ndarray:
    rows = []
    for group in groups:
        if len(group["members"]) != 1:
            raise ValueError(f"{group['field_group']} does not have one row")
        rows.append(feature_row(group["members"][0]))
    return np.vstack(rows)


def labels(groups: list[dict], classes: tuple[str, ...]) -> np.ndarray:
    index = {name: i for i, name in enumerate(classes)}
    return np.array([index[group["family"]] for group in groups], dtype=int)


def standardize(train: np.ndarray, other: list[np.ndarray]) -> tuple[np.ndarray, list[np.ndarray]]:
    mean = train.mean(axis=0)
    std = train.std(axis=0)
    std = np.where(std < 1e-12, 1.0, std)
    scaled = [(block - mean) / std for block in [train, *other]]
    return scaled[0], scaled[1:]


def fit_softmax(x_train: np.ndarray, y_train: np.ndarray, n_classes: int) -> tuple[np.ndarray, np.ndarray]:
    n_rows, n_features = x_train.shape
    weights = np.zeros((n_features, n_classes))
    bias = np.zeros(n_classes)
    one_hot = np.eye(n_classes)[y_train]
    for _ in range(STEPS):
        probabilities = predict_proba(x_train, weights, bias)
        gradient = (probabilities - one_hot) / n_rows
        weights -= LEARNING_RATE * (x_train.T @ gradient + L2 * weights)
        bias -= LEARNING_RATE * gradient.sum(axis=0)
    return weights, bias


def predict_proba(features: np.ndarray, weights: np.ndarray, bias: np.ndarray) -> np.ndarray:
    logits = features @ weights + bias
    logits = logits - logits.max(axis=1, keepdims=True)
    exp_logits = np.exp(logits)
    return exp_logits / exp_logits.sum(axis=1, keepdims=True)


def conformal_threshold(scores: np.ndarray, alpha: float = ALPHA) -> float:
    """Finite-sample split-conformal quantile. Infinity means the set is every class."""
    n_scores = int(scores.shape[0])
    if n_scores == 0:
        return math.inf
    rank = math.ceil((n_scores + 1) * (1 - alpha))
    if rank > n_scores:
        return math.inf
    ordered = np.sort(scores)
    return float(ordered[rank - 1])


def prediction_set(probabilities: np.ndarray, classes: tuple[str, ...], threshold: float) -> list[str]:
    chosen = []
    for index, name in enumerate(classes):
        score = 1.0 - float(probabilities[index])
        if score <= threshold:
            chosen.append(name)
    return chosen
