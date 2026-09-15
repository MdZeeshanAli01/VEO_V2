from pathlib import Path

import h5py
import numpy as np
from PIL import Image


def extract_labeled_mat(mat_path: Path, rgb_dir: Path, depth_dir: Path, start: int = 0, count: int | None = None) -> int:
    """Extract aligned RGB/depth pairs from the official NYU v2 labeled MAT file.

    The v7.3 MAT file stores MATLAB arrays in reversed HDF5 order. The official
    ``depths`` variable is the dense, in-painted depth in metres.
    """
    with h5py.File(mat_path, "r") as handle:
        total = int(handle["images"].shape[0])
        stop = total if count is None else min(total, start + count)
        if start < 0 or start >= total or start >= stop:
            raise ValueError(f"Invalid extraction range: start={start}, count={count}, total={total}")
        rgb_dir.mkdir(parents=True, exist_ok=True)
        depth_dir.mkdir(parents=True, exist_ok=True)
        for index in range(start, stop):
            sample_id = f"scene_{index + 1:04d}"
            image = np.asarray(handle["images"][index], dtype=np.uint8).transpose(2, 1, 0)
            depth = np.asarray(handle["depths"][index], dtype=np.float32).transpose(1, 0)
            Image.fromarray(image, mode="RGB").save(rgb_dir / f"{sample_id}.png")
            np.save(depth_dir / f"{sample_id}.npy", depth)
    return stop - start


def _scene_names(handle: h5py.File) -> list[str]:
    references = np.asarray(handle["scenes"][:]).reshape(-1)
    names = []
    for reference in references:
        value = handle["#refs#"][reference][()]
        names.append(value.tobytes().decode("utf-16le").rstrip("\x00"))
    return names


def create_scene_splits(mat_path: Path, seed: int = 42, train_fraction: float = 0.70, validation_fraction: float = 0.15) -> dict[str, list[dict]]:
    with h5py.File(mat_path, "r") as handle:
        scenes = _scene_names(handle)
    unique_scenes = sorted(set(scenes))
    generator = np.random.default_rng(seed)
    shuffled = unique_scenes.copy()
    generator.shuffle(shuffled)
    train_end = int(len(shuffled) * train_fraction)
    validation_end = train_end + int(len(shuffled) * validation_fraction)
    partitions = {
        "development": set(shuffled[:train_end]),
        "validation": set(shuffled[train_end:validation_end]),
        "test": set(shuffled[validation_end:]),
    }
    return {
        split: [{"index": index, "sample_id": f"scene_{index + 1:04d}", "scene": scene} for index, scene in enumerate(scenes) if scene in selected]
        for split, selected in partitions.items()
    }


def extract_split(mat_path: Path, split_records: list[dict], output_dir: Path) -> int:
    rgb_dir = output_dir / "rgb"
    depth_dir = output_dir / "depth"
    rgb_dir.mkdir(parents=True, exist_ok=True)
    depth_dir.mkdir(parents=True, exist_ok=True)
    with h5py.File(mat_path, "r") as handle:
        for record in split_records:
            index = record["index"]
            image = np.asarray(handle["images"][index], dtype=np.uint8).transpose(2, 1, 0)
            depth = np.asarray(handle["depths"][index], dtype=np.float32).transpose(1, 0)
            Image.fromarray(image, mode="RGB").save(rgb_dir / f"{record['sample_id']}.png")
            np.save(depth_dir / f"{record['sample_id']}.npy", depth)
    return len(split_records)