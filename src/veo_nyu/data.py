from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image


@dataclass(frozen=True)
class RGBDepthPair:
    sample_id: str
    rgb_path: Path
    depth_path: Path


def discover_manifest(manifest_path: Path) -> list[RGBDepthPair]:
    pairs = []
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        fields = line.strip().split()
        if not fields or fields[0].startswith("#"):
            continue
        if len(fields) != 2:
            raise ValueError(f"Each manifest line must contain RGB and depth paths: {line}")
        rgb_path, depth_path = (Path(field) for field in fields)
        pairs.append(RGBDepthPair(rgb_path.stem, rgb_path, depth_path))
    return pairs


def discover_pairs(rgb_dir: Path, depth_dir: Path) -> list[RGBDepthPair]:
    rgb_files = {path.stem: path for path in rgb_dir.glob("*") if path.suffix.lower() in {".png", ".jpg", ".jpeg"}}
    depth_files = {path.stem: path for path in depth_dir.glob("*") if path.suffix.lower() in {".png", ".npy"}}
    sample_ids = sorted(rgb_files.keys() & depth_files.keys())
    return [RGBDepthPair(sample_id, rgb_files[sample_id], depth_files[sample_id]) for sample_id in sample_ids]


def validate_pairs(pairs: list[RGBDepthPair], rgb_dir: Path | None = None, depth_dir: Path | None = None) -> None:
    if not pairs:
        location = f" RGB directory: {rgb_dir}; depth directory: {depth_dir}." if rgb_dir and depth_dir else ""
        raise FileNotFoundError(
            "No matching NYU RGB/depth pairs were found."
            f"{location} Expected files with identical stems, for example "
            "data/nyu/rgb/scene_0001.png and data/nyu/depth/scene_0001.png."
        )
    duplicate_ids = {pair.sample_id for pair in pairs if sum(item.sample_id == pair.sample_id for item in pairs) > 1}
    if duplicate_ids:
        raise ValueError(f"Duplicate sample IDs found: {sorted(duplicate_ids)}")


def load_rgb(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGB"), dtype=np.uint8)


def load_depth(path: Path, depth_scale: float = 1000.0) -> np.ndarray:
    if path.suffix.lower() in {".h5", ".hdf5"}:
        import h5py

        with h5py.File(path, "r") as handle:
            distance = np.asarray(handle["dataset"], dtype=np.float32)
        width, height, focal = 1024, 768, 886.81
        image_x = np.linspace((-0.5 * width) + 0.5, (0.5 * width) - 0.5, width)[None, :].repeat(height, 0)
        image_y = np.linspace((-0.5 * height) + 0.5, (0.5 * height) - 0.5, height)[:, None].repeat(width, 1)
        norm = np.sqrt(image_x**2 + image_y**2 + focal**2)
        return distance / norm * focal
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
