"""What each feature should respond to, on synthetic regions.

Tests marked xfail document known v1 defects that Phase 2 will fix. They are strict, so a fix
makes them fail until the marker is removed, which keeps this list accurate.
"""

import numpy as np
import pytest

from veo.features import extract_features
from veo.scoring import score_categories


def _scores(rgb: np.ndarray, depth: np.ndarray, mask: np.ndarray) -> dict[str, float]:
    ys, xs = np.where(mask)
    x0, y0 = int(xs.min()), int(ys.min())
    region = {"bbox": [x0, y0, int(xs.max()) - x0 + 1, int(ys.max()) - y0 + 1], "mask": mask}
    return score_categories(extract_features(rgb, depth, region))


def _canvas(value: float = 128.0, size: int = 64) -> tuple[np.ndarray, np.ndarray]:
    return np.full((size, size, 3), value, dtype=np.uint8), np.full((size, size), 3.0, dtype=np.float32)


def _box(size: int = 64, top: int = 12, left: int = 12, height: int = 40, width: int = 40) -> np.ndarray:
    mask = np.zeros((size, size), dtype=bool)
    mask[top:top + height, left:left + width] = True
    return mask


def test_flat_region_is_textureless():
    rgb, depth = _canvas()
    assert _scores(rgb, depth, _box())["textureless"] > 0.9


def test_checkerboard_is_not_textureless():
    rgb, depth = _canvas()
    rows, cols = np.mgrid[0:64, 0:64]
    rgb[((rows // 4 + cols // 4) % 2).astype(bool)] = 230
    rgb[~((rows // 4 + cols // 4) % 2).astype(bool)] = 30
    assert _scores(rgb, depth, _box())["textureless"] < 0.1


@pytest.mark.xfail(strict=True, reason="phase 2: reflection uses V>200 & S<40, which matches any white wall")
def test_flat_white_wall_is_not_reflection():
    rgb, depth = _canvas(235.0)
    assert _scores(rgb, depth, _box())["reflection"] < 0.5


@pytest.mark.xfail(strict=True, reason="phase 2: thin_object uses bounding-box aspect ratio, so diagonal poles look square")
def test_diagonal_pole_is_thin():
    rgb, depth = _canvas()
    mask = np.zeros((64, 64), dtype=bool)
    for i in range(10, 54):
        mask[i, i - 1:i + 2] = True
    assert _scores(rgb, depth, mask)["thin_object"] > 0.5


@pytest.mark.xfail(strict=True, reason="phase 2: a long strip of a large surface has a high bounding-box aspect ratio")
def test_long_strip_of_wall_is_not_thin():
    rgb, depth = _canvas()
    assert _scores(rgb, depth, _box(top=30, height=4, left=4, width=56))["thin_object"] < 0.5


@pytest.mark.xfail(strict=True, reason="phase 2: grey-level variance treats a smooth lighting gradient as texture")
def test_smooth_gradient_is_textureless():
    rgb, depth = _canvas()
    rgb[:] = np.linspace(40, 220, 64, dtype=np.uint8)[None, :, None]
    assert _scores(rgb, depth, _box())["textureless"] > 0.5


@pytest.mark.xfail(strict=True, reason="phase 2: occlusion scale is 1.0 m/px, so a 50% depth step barely registers")
def test_large_relative_depth_step_is_occlusion():
    rgb, depth = _canvas()
    depth[:, 32:] = 1.5
    depth[:, :32] = 1.0
    assert _scores(rgb, depth, _box(left=20, width=24))["occlusion"] > 0.5
