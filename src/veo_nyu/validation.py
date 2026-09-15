from collections import Counter

from .scoring import classify


def cohens_kappa(first: list[str], second: list[str]) -> float:
    if len(first) != len(second) or not first:
        raise ValueError("Both label lists must be non-empty and have equal length")
    total = len(first)
    categories = set(first) | set(second)
    observed = sum(left == right for left, right in zip(first, second)) / total
    first_counts = Counter(first)
    second_counts = Counter(second)
    expected = sum((first_counts[label] / total) * (second_counts[label] / total) for label in categories)
    if expected == 1.0:
        return 1.0
    return float((observed - expected) / (1.0 - expected))


def ablation_change(records: list[dict], dropped_signal: str, include_reflection: bool = True) -> dict[str, int]:
    changed = 0
    total = 0
    for record in records:
        for region in record["regions"]:
            features = dict(region["features"])
            if dropped_signal not in features:
                continue
            if dropped_signal == "texture_var":
                features["texture_var"] = 500.0
            elif dropped_signal == "edge_density":
                features["edge_density"] = 0.0
            elif dropped_signal == "brightness":
                features["brightness"] = 128.0
                features["contrast"] = 60.0
            elif dropped_signal == "contrast":
                features["contrast"] = 60.0
            elif dropped_signal == "highlight_ratio":
                features["highlight_ratio"] = 0.0
            elif dropped_signal == "aspect_ratio":
                features["aspect_ratio"] = 1.0
            elif dropped_signal == "depth_discontinuity":
                features["depth_discontinuity"] = 0.0
            else:
                raise ValueError(f"Unsupported ablation signal: {dropped_signal}")
            new_label = classify(features, include_reflection)["top_cause"]
            changed += new_label != region["top_cause"]
            total += 1
    return {"changed_regions": changed, "total_regions": total}
