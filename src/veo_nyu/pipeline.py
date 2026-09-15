from dataclasses import asdict

import numpy as np

from .config import ExperimentConfig
from .features import extract_features
from .metrics import align_scale_shift, compute_error_map, compute_metrics
from .regions import extract_failure_regions
from .scoring import classify


def analyze_sample(rgb: np.ndarray, target: np.ndarray, prediction: np.ndarray, valid_mask: np.ndarray, config: ExperimentConfig) -> dict:
    if rgb.shape[:2] != target.shape or target.shape != prediction.shape:
        raise ValueError("RGB, target, and prediction dimensions do not match")
    scale, shift = 1.0, 0.0
    aligned_prediction = prediction.astype(np.float32)
    if config.align_scale_shift:
        aligned_prediction, scale, shift = align_scale_shift(aligned_prediction, target, valid_mask)
    metrics = compute_metrics(aligned_prediction, target, valid_mask)
    error_map = compute_error_map(aligned_prediction, target, valid_mask)
    regions = extract_failure_regions(error_map, valid_mask, config.error_percentile, config.min_region_area)
    result_regions = []
    for region in regions:
        features = extract_features(rgb, target, region)
        classification = classify(features, config.include_reflection)
        result_regions.append({
            "region_id": region["region_id"],
            "bbox": region["bbox"],
            "area": region["area"],
            "mean_error": region["mean_error"],
            "features": features,
            **classification,
        })
    return {
        "metrics": metrics,
        "alignment": {"scale": scale, "shift": shift, "enabled": config.align_scale_shift},
        "threshold": float(np.percentile(error_map[valid_mask], config.error_percentile)),
        "num_regions": len(result_regions),
        "regions": result_regions,
        "config": asdict(config),
    }
