"""Calibrate VEO's rules against objective (silver) labels and compare with a learned model.

Everything that is fitted uses the train split; the test split is only scored. Per category we report:
  * the hand-set rule from protocol v2 (score >= 0.5 assigns the label),
  * a two-feature logistic model with a threshold chosen on train to maximise F1 (interpretable),
  * a gradient-boosted model on all features (a learned reference, not interpretable),
each with AUROC and a scene-level bootstrap 95% interval, plus precision, recall and F1 of the label.
"""

import numpy as np

from .scoring import classify
from .silver import SILVER_CATEGORIES

FEATURES = (
    "grad_energy", "corner_strength", "depth_edge_fraction", "depth_step", "thin_fraction",
    "thin_image_fraction", "highlight_ratio", "clipped_fraction", "brightness", "contrast",
    "aspect_ratio", "mean_depth_m",
)
CALIBRATION_FEATURES = {
    "textureless": ("grad_energy", "corner_strength"),
    "boundary_mixing": ("depth_edge_fraction", "depth_step"),
    "thin_object": ("thin_fraction", "thin_image_fraction"),
    "reflection": ("highlight_ratio", "brightness"),
}


def feature_matrix(rows: list[dict], names=FEATURES) -> np.ndarray:
    return np.asarray([[row["features"].get(name, 0.0) for name in names] for row in rows], dtype=float)


def silver_matrix(rows: list[dict]) -> np.ndarray:
    return np.asarray([[category in row["silver"]["labels"] for category in SILVER_CATEGORIES] for row in rows], dtype=bool)


def _auroc(labels: np.ndarray, scores: np.ndarray) -> float | None:
    from sklearn.metrics import roc_auc_score

    return float(roc_auc_score(labels, scores)) if 0 < labels.sum() < len(labels) else None


def _bootstrap_auroc(labels: np.ndarray, scores: np.ndarray, groups: np.ndarray, replicates: int = 1000, seed: int = 42) -> dict:
    """AUROC with a 95% interval from resampling scenes (regions in one scene are not independent)."""
    point = _auroc(labels, scores)
    if point is None:
        return {"auroc": None, "lower": None, "upper": None}
    rng = np.random.default_rng(seed)
    unique = np.unique(groups)
    index_by_group = {group: np.flatnonzero(groups == group) for group in unique}
    values = []
    for _ in range(replicates):
        picked = np.concatenate([index_by_group[group] for group in rng.choice(unique, size=len(unique), replace=True)])
        value = _auroc(labels[picked], scores[picked])
        if value is not None:
            values.append(value)
    return {"auroc": point, "lower": float(np.percentile(values, 2.5)), "upper": float(np.percentile(values, 97.5))}


def _label_metrics(labels: np.ndarray, assigned: np.ndarray) -> dict:
    true_positive = int((labels & assigned).sum())
    precision = true_positive / assigned.sum() if assigned.sum() else 0.0
    recall = true_positive / labels.sum() if labels.sum() else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"assigned": int(assigned.sum()), "precision": precision, "recall": recall, "f1": f1}


def _best_f1_threshold(labels: np.ndarray, probabilities: np.ndarray) -> float:
    candidates = np.unique(np.round(probabilities, 3))
    scores = [_label_metrics(labels, probabilities >= threshold)["f1"] for threshold in candidates]
    return float(candidates[int(np.argmax(scores))]) if len(candidates) else 0.5


def fit(train_rows: list[dict], seed: int = 42) -> dict:
    """Per category: standardised two-feature logistic model with an F1-optimal threshold, and a boosted model."""
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.linear_model import LogisticRegression

    silver = silver_matrix(train_rows)
    all_features = feature_matrix(train_rows)
    models = {}
    for column, category in enumerate(SILVER_CATEGORIES):
        labels = silver[:, column]
        if not 0 < labels.sum() < len(labels):
            models[category] = None
            continue
        names = CALIBRATION_FEATURES[category]
        x = feature_matrix(train_rows, names)
        mean, std = x.mean(axis=0), x.std(axis=0) + 1e-9
        logistic = LogisticRegression(max_iter=1000).fit((x - mean) / std, labels)
        probabilities = logistic.predict_proba((x - mean) / std)[:, 1]
        boosted = HistGradientBoostingClassifier(max_iter=200, learning_rate=0.05, random_state=seed).fit(all_features, labels)
        models[category] = {
            "features": list(names),
            "mean": mean.tolist(),
            "std": std.tolist(),
            "coef": logistic.coef_[0].tolist(),
            "intercept": float(logistic.intercept_[0]),
            "threshold": _best_f1_threshold(labels, probabilities),
            "train_prevalence": float(labels.mean()),
            "_logistic": logistic,
            "_boosted": boosted,
        }
    return models


def calibrated_probability(model: dict, rows: list[dict]) -> np.ndarray:
    x = (feature_matrix(rows, model["features"]) - np.asarray(model["mean"])) / np.asarray(model["std"])
    return model["_logistic"].predict_proba(x)[:, 1]


def evaluate(models: dict, rows: list[dict], settings: dict | None = None, replicates: int = 1000) -> dict:
    """Score the test rows; ``settings`` are the protocol's hand-set rule parameters."""
    silver = silver_matrix(rows)
    groups = np.asarray([row["scene"] for row in rows])
    all_features = feature_matrix(rows)
    hand_scores = [classify(row["features"], True, settings)["scores"] for row in rows]
    report = {"regions": len(rows), "scenes": int(len(np.unique(groups))), "categories": {}}
    for column, category in enumerate(SILVER_CATEGORIES):
        labels = silver[:, column]
        hand = np.asarray([scores.get(category, 0.0) for scores in hand_scores])
        entry = {
            "prevalence": float(labels.mean()) if len(labels) else 0.0,
            "positives": int(labels.sum()),
            "hand_set": {**_bootstrap_auroc(labels, hand, groups, replicates), **_label_metrics(labels, hand >= 0.5)},
        }
        model = models.get(category)
        if model is not None:
            probability = calibrated_probability(model, rows)
            boosted = model["_boosted"].predict_proba(all_features)[:, 1]
            entry["calibrated"] = {**_bootstrap_auroc(labels, probability, groups, replicates), **_label_metrics(labels, probability >= model["threshold"])}
            entry["learned"] = {**_bootstrap_auroc(labels, boosted, groups, replicates), **_label_metrics(labels, boosted >= 0.5)}
        report["categories"][category] = entry
    return report


def public_models(models: dict) -> dict:
    """The JSON-serialisable part of fitted models (drops the sklearn objects)."""
    return {category: None if model is None else {key: value for key, value in model.items() if not key.startswith("_")} for category, model in models.items()}
