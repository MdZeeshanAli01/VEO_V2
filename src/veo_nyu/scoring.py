import numpy as np


def clip01(value: float) -> float:
    return float(np.clip(value, 0.0, 1.0))


def score_categories(features: dict[str, float], include_reflection: bool = True, thresholds: dict[str, float] | None = None) -> dict[str, float]:
    thresholds = thresholds or {}
    texture_scale = thresholds.get("texture_variance_scale", 500.0)
    edge_scale = thresholds.get("edge_density_scale", 3.0)
    contrast_scale = thresholds.get("contrast_scale", 60.0)
    occlusion_scale = thresholds.get("occlusion_scale", 1.0)
    reflection_scale = thresholds.get("reflection_scale", 5.0)
    scores = {
        "textureless": clip01(1.0 - features["texture_var"] / texture_scale),
        "boundary_mixing": clip01(features["edge_density"] * edge_scale),
        "poor_lighting": clip01(1.0 - features["contrast"] / contrast_scale) if features["brightness"] < 60 or features["brightness"] > 200 else 0.0,
        "thin_object": clip01((features["aspect_ratio"] - 3.0) / 5.0),
        "occlusion": clip01(features["depth_discontinuity"] / occlusion_scale),
    }
    if include_reflection:
        scores["reflection"] = clip01(features["highlight_ratio"] * reflection_scale)
    return scores


def classify(features: dict[str, float], include_reflection: bool = True, thresholds: dict[str, float] | None = None) -> dict:
    thresholds = thresholds or {}
    margin_threshold = thresholds.get("ambiguity_margin", 0.10)
    scores = score_categories(features, include_reflection, thresholds)
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    top_cause, top_score = ranked[0]
    second_score = ranked[1][1] if len(ranked) > 1 else 0.0
    margin = top_score - second_score
    ambiguous = top_score < 0.4 or margin < margin_threshold
    confidence = "Low" if ambiguous else "High" if top_score > 0.6 else "Medium"
    return {"scores": scores, "top_cause": "ambiguous" if ambiguous else top_cause, "confidence": confidence, "score_margin": float(margin)}
