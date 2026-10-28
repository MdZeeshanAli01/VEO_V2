"""Small synthetic NYU-format dataset and predictor, so the full pipeline runs without downloads."""

from pathlib import Path

import cv2
import h5py
import numpy as np


def _scene(rng: np.random.Generator, height: int, width: int) -> tuple[np.ndarray, np.ndarray]:
    """Indoor-like scene: a back wall, a floor, a box in front and a thin pole, with mixed textures."""
    rows, cols = np.mgrid[0:height, 0:width]
    depth = np.full((height, width), rng.uniform(3.5, 6.0), dtype=np.float32)
    horizon = int(height * rng.uniform(0.55, 0.7))
    floor_rows = rows >= horizon
    depth[floor_rows] = (depth.max() * horizon / np.maximum(rows[floor_rows], 1)).astype(np.float32)
    y0, x0 = int(height * 0.35), int(width * rng.uniform(0.15, 0.45))
    depth[y0:y0 + height // 3, x0:x0 + width // 4] = rng.uniform(1.2, 2.5)
    pole_x = int(width * rng.uniform(0.7, 0.85))
    depth[: horizon, pole_x:pole_x + 2] = rng.uniform(1.0, 2.0)

    gray = np.full((height, width), rng.uniform(150, 215))  # flat wall
    gray[floor_rows] = 90 + 40 * ((rows[floor_rows] // 4 + cols[floor_rows] // 4) % 2)  # tiled floor
    gray[y0:y0 + height // 3, x0:x0 + width // 4] = 60 + rng.normal(0, 25, size=(height // 3, width // 4))
    gray[: horizon, pole_x:pole_x + 2] = 30
    rgb = np.clip(np.stack([gray, gray * 0.95, gray * 0.9], axis=-1) + rng.normal(0, 2, (height, width, 3)), 0, 255)
    return rgb.astype(np.uint8), depth


def _sensor_depth(depth: np.ndarray, rgb: np.ndarray) -> np.ndarray:
    """Mimic Kinect dropouts: no measurement on very dark pixels and along a few depth edges."""
    raw = depth.copy()
    raw[rgb.mean(axis=-1) < 40] = 0.0
    step = np.abs(np.diff(np.log(depth), axis=1, prepend=np.log(depth[:, :1]))) > 0.3
    raw[step] = 0.0
    return raw


def write_fixture_mat(path: Path, scenes: int = 8, frames_per_scene: int = 2, height: int = 48, width: int = 64, seed: int = 0) -> Path:
    """Write a file with the layout of nyu_depth_v2_labeled.mat (MATLAB v7.3, reversed axes)."""
    rng = np.random.default_rng(seed)
    count = scenes * frames_per_scene
    images = np.zeros((count, 3, width, height), dtype=np.uint8)
    depths = np.zeros((count, width, height), dtype=np.float32)
    raw_depths = np.zeros_like(depths)
    labels = np.zeros((count, width, height), dtype=np.uint16)
    for index in range(count):
        rgb, depth = _scene(rng, height, width)
        images[index] = rgb.transpose(2, 1, 0)
        depths[index] = depth.transpose(1, 0)
        raw_depths[index] = _sensor_depth(depth, rgb).transpose(1, 0)
        labels[index] = np.where(depth < 3.0, 2, 1).astype(np.uint16).transpose(1, 0)
    path.parent.mkdir(parents=True, exist_ok=True)
    with h5py.File(path, "w") as handle:
        handle.create_dataset("images", data=images)
        handle.create_dataset("depths", data=depths)
        handle.create_dataset("rawDepths", data=raw_depths)
        handle.create_dataset("labels", data=labels)
        refs = handle.create_group("#refs#")
        name_refs = []
        for number, name in enumerate(("wall", "object")):
            refs.create_dataset(f"name{number}", data=np.frombuffer(name.encode("utf-16le"), dtype=np.uint16))
            name_refs.append(refs[f"name{number}"].ref)
        handle.create_dataset("names", data=np.asarray(name_refs, dtype=h5py.ref_dtype).reshape(1, -1))
        scene_refs = []
        for index in range(count):
            name = f"fixture_scene_{index // frames_per_scene:02d}"
            refs.create_dataset(f"{index:04d}", data=np.frombuffer(name.encode("utf-16le"), dtype=np.uint16))
            scene_refs.append(refs[f"{index:04d}"].ref)
        handle.create_dataset("scenes", data=np.asarray(scene_refs, dtype=h5py.ref_dtype).reshape(1, -1))
    return path


def write_fixture_splits(path: Path, scenes: int, frames_per_scene: int = 2, test_scenes: int = 4) -> Path:
    """An official-style splits.mat (1-based trainNdxs/testNdxs) that keeps whole scenes together."""
    from scipy.io import savemat

    count = scenes * frames_per_scene
    test = np.arange(count - test_scenes * frames_per_scene, count) + 1
    train = np.arange(1, count - test_scenes * frames_per_scene + 1)
    savemat(path, {"trainNdxs": train.reshape(-1, 1).astype(float), "testNdxs": test.reshape(-1, 1).astype(float)})
    return path


class SyntheticDisparityPredictor:
    """Stands in for a relative-depth model: returns affine-transformed disparity with structured errors."""

    def __init__(self, seed: int = 0):
        self._rng = np.random.default_rng(seed)

    def predict(self, rgb: np.ndarray, target: np.ndarray) -> np.ndarray:
        height, width = target.shape
        disparity = 1.0 / np.clip(target, 0.1, None)
        # Smear depth edges over ~3 px each side, wider than the sensor holes that sit on the edges
        blurred = cv2.blur(disparity.astype(np.float32), (7, 1)).astype(np.float64)
        rows, cols = np.mgrid[0:height, 0:width]

        def bump(row: float, col: float, radius: float, amount: float) -> np.ndarray:
            return 1.0 + amount * np.exp(-((rows - row * height) ** 2 + (cols - col * width) ** 2) / (2 * (radius * width) ** 2))

        # Smooth errors on the flat upper wall (textureless) and on the tiled floor (texture edges, no depth step)
        blurred *= bump(0.12, 0.2, 0.08, 0.8) * bump(0.92, 0.5, 0.07, 0.6)
        noise = self._rng.normal(0.0, 0.02, size=target.shape)
        return (3.0 * blurred + 0.5 + noise).astype(np.float32)
