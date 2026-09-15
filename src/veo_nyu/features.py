import cv2
import numpy as np


def extract_features(rgb: np.ndarray, target: np.ndarray, region: dict) -> dict[str, float]:
    x, y, width, height = region["bbox"]
    rgb_patch = rgb[y:y + height, x:x + width]
    depth_patch = target[y:y + height, x:x + width]
    region_mask = region["mask"][y:y + height, x:x + width]
    gray = cv2.cvtColor(rgb_patch, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    valid_depth = depth_patch[region_mask]
    if valid_depth.size > 1 and depth_patch.shape[0] > 1 and depth_patch.shape[1] > 1:
        gy, gx = np.gradient(depth_patch.astype(np.float32))
        depth_discontinuity = float(np.hypot(gx, gy)[region_mask].mean())
    else:
        depth_discontinuity = 0.0
    hsv = cv2.cvtColor(rgb_patch, cv2.COLOR_RGB2HSV)
    highlights = (hsv[:, :, 2] > 200) & (hsv[:, :, 1] < 40)
    return {
        "texture_var": float(np.var(gray[region_mask])) if region_mask.any() else 0.0,
        "edge_density": float(edges[region_mask].mean() / 255.0) if region_mask.any() else 0.0,
        "brightness": float(gray[region_mask].mean()) if region_mask.any() else 0.0,
        "contrast": float(gray[region_mask].std()) if region_mask.any() else 0.0,
        "highlight_ratio": float(highlights[region_mask].mean()) if region_mask.any() else 0.0,
        "aspect_ratio": float(max(width, height) / max(min(width, height), 1)),
        "depth_discontinuity": depth_discontinuity,
        "mean_depth_m": float(valid_depth.mean()) if valid_depth.size else 0.0,
    }
