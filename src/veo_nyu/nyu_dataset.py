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