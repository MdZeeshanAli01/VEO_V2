import numpy as np


def align_scale_shift(prediction: np.ndarray, target: np.ndarray, valid_mask: np.ndarray) -> tuple[np.ndarray, float, float]:
    if prediction.shape != target.shape or valid_mask.shape != target.shape:
        raise ValueError("Prediction, target, and valid_mask must have identical shapes")
    if int(valid_mask.sum()) < 2:
        return prediction.astype(np.float32), 1.0, 0.0
    p = prediction[valid_mask].astype(np.float64)
    t = target[valid_mask].astype(np.float64)
    design = np.stack([p, np.ones_like(p)], axis=1)
    scale, shift = np.linalg.lstsq(design, t, rcond=None)[0]
    return (prediction * scale + shift).astype(np.float32), float(scale), float(shift)


def compute_metrics(prediction: np.ndarray, target: np.ndarray, valid_mask: np.ndarray) -> dict[str, float]:
    if prediction.shape != target.shape or valid_mask.shape != target.shape:
        raise ValueError("Prediction, target, and valid_mask must have identical shapes")
    if not valid_mask.any():
        raise ValueError("Cannot compute metrics with an empty valid mask")
    pred = prediction[valid_mask].astype(np.float64)
    truth = np.clip(target[valid_mask].astype(np.float64), 1e-6, None)
    abs_rel = np.mean(np.abs(pred - truth) / truth)
    rmse = np.sqrt(np.mean((pred - truth) ** 2))
    ratio = np.maximum(pred / truth, truth / np.clip(pred, 1e-6, None))
    delta1 = np.mean(ratio < 1.25)
    return {"abs_rel": float(abs_rel), "rmse": float(rmse), "delta1": float(delta1)}


def compute_error_map(prediction: np.ndarray, target: np.ndarray, valid_mask: np.ndarray) -> np.ndarray:
    error_map = np.zeros_like(target, dtype=np.float32)
    safe_target = np.clip(target, 1e-6, None)
    error_map[valid_mask] = np.abs(prediction[valid_mask] - safe_target[valid_mask]) / safe_target[valid_mask]
    return error_map
