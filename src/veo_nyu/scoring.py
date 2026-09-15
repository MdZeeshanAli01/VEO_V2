import numpy as np


def clip01(value: float) -> float:
    return float(np.clip(value, 0.0, 1.0))


def score_categories(features: dict[str, float], include_reflection: bool = True) -> dict[str, float]:
    scores = {
        "textureless": clip01(1.0 - features["texture_var"] / 500.0),
        "boundary_mixing": clip01(features["edge_density"] * 3.0),
        "poor_lighting": clip01(1.0 - features["contrast"] / 60.0) if features["brightness"] < 60 or features["brightness"] > 200 else 0.0,
        "thin_object": clip01((features["aspect_ratio"] - 3.0) / 5.0),
        "occlusion": clip01(features["depth_discontinuity"] / 1.0),
    }
    if include_reflection:
        scores["reflection"] = clip01(features["highlight_ratio"] * 5.0)
    return scores


def classify(features: dict[str, float], include_reflection: bool = True) -> dict:
    scores = score_categories(features, include_reflection)
    top_cause = max(scores, key=scores.get)
    top_score = scores[top_cause]
    confidence = "High" if top_score > 0.6 else "Medium" if top_score > 0.4 else "Low"
    return {"scores": scores, "top_cause": top_cause, "confidence": confidence}
