import numpy as np
from scipy import ndimage


def extract_failure_regions(error_map: np.ndarray, valid_mask: np.ndarray, percentile: float = 85.0, min_area: int = 25) -> list[dict]:
    if error_map.shape != valid_mask.shape:
        raise ValueError("error_map and valid_mask must have identical shapes")
    valid_errors = error_map[valid_mask]
    if valid_errors.size == 0:
        return []
    threshold = float(np.percentile(valid_errors, percentile))
    binary = (error_map > threshold) & valid_mask
    labels, count = ndimage.label(binary)
    regions = []
    for region_id in range(1, count + 1):
        mask = labels == region_id
        area = int(mask.sum())
        if area < min_area:
            continue
        ys, xs = np.where(mask)
        x0, x1 = int(xs.min()), int(xs.max())
        y0, y1 = int(ys.min()), int(ys.max())
        regions.append({
            "region_id": region_id,
            "bbox": [x0, y0, x1 - x0 + 1, y1 - y0 + 1],
            "area": area,
            "mean_error": float(error_map[mask].mean()),
            "mask": mask,
        })
    return regions
