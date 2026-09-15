from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image


@dataclass(frozen=True)
class RGBDepthPair:
    sample_id: str
    rgb_path: Path
    depth_path: Path


def discover_pairs(rgb_dir: Path, depth_dir: Path) -> list[RGBDepthPair]:
    rgb_files = {path.stem: path for path in rgb_dir.glob("*") if path.suffix.lower() in {".png", ".jpg", ".jpeg"}}
    depth_files = {path.stem: path for path in depth_dir.glob("*") if path.suffix.lower() in {".png", ".npy"}}
    sample_ids = sorted(rgb_files.keys() & depth_files.keys())
    return [RGBDepthPair(sample_id, rgb_files[sample_id], depth_files[sample_id]) for sample_id in sample_ids]


def validate_pairs(pairs: list[RGBDepthPair]) -> None:
    if not pairs:
        raise FileNotFoundError("No matching RGB/depth pairs were found")
    duplicate_ids = {pair.sample_id for pair in pairs if sum(item.sample_id == pair.sample_id for item in pairs) > 1}
    if duplicate_ids:
        raise ValueError(f"Duplicate sample IDs found: {sorted(duplicate_ids)}")


def load_rgb(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGB"), dtype=np.uint8)


def load_depth(path: Path, depth_scale: float = 1000.0) -> np.ndarray:
    if path.suffix.lower() == ".npy":
        depth = np.asarray(np.load(path), dtype=np.float32)
    else:
        raw = np.asarray(Image.open(path))
        depth = raw.astype(np.float32) / depth_scale
    if depth.ndim != 2:
        raise ValueError(f"Depth must be 2D, got shape {depth.shape} from {path}")
    return depth


def make_valid_mask(depth: np.ndarray, max_depth_m: float = 10.0) -> np.ndarray:
    return np.isfinite(depth) & (depth > 0.0) & (depth <= max_depth_m)
