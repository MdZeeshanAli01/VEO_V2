import numpy as np
from PIL import Image

from veo_nyu.data import discover_pairs, load_depth, validate_pairs
from veo_nyu.features import extract_features
from veo_nyu.inference import PrecomputedPredictor
from veo_nyu.metrics import align_scale_shift, compute_metrics
from veo_nyu.nyu_dataset import extract_labeled_mat
from veo_nyu.regions import extract_failure_regions
from veo_nyu.reports import write_summary
from veo_nyu.scoring import classify


def test_alignment_recovers_affine_depth():
    prediction = np.arange(16, dtype=np.float32).reshape(4, 4)
    target = 2.0 * prediction + 1.0
    aligned, scale, shift = align_scale_shift(prediction, target, np.ones((4, 4), dtype=bool))
    assert np.isclose(scale, 2.0)
    assert np.isclose(shift, 1.0)
    assert np.allclose(aligned, target)


def test_metrics_use_only_valid_pixels():
    prediction = np.array([[1.0, 3.0], [100.0, 1.0]], dtype=np.float32)
    target = np.ones((2, 2), dtype=np.float32)
    valid = np.array([[True, True], [False, True]])
    metrics = compute_metrics(prediction, target, valid)
    assert np.isclose(metrics["abs_rel"], 2.0 / 3.0)


def test_regions_respect_area_and_mask():
    error = np.zeros((8, 8), dtype=np.float32)
    error[2:5, 2:5] = 1.0
    valid = np.ones_like(error, dtype=bool)
    regions = extract_failure_regions(error, valid, percentile=80, min_area=3)
    assert len(regions) == 1
    assert regions[0]["area"] == 9


def test_classification_returns_documented_fields():
    result = classify({
        "texture_var": 10.0,
        "edge_density": 0.1,
        "brightness": 128.0,
        "contrast": 20.0,
        "highlight_ratio": 0.0,
        "aspect_ratio": 1.0,
        "depth_discontinuity": 2.0,
    })
    assert result["top_cause"] == "occlusion"
    assert result["confidence"] == "High"


def test_nyu_pair_discovery_and_precomputed_prediction(tmp_path):
    rgb_dir = tmp_path / "rgb"
    depth_dir = tmp_path / "depth"
    prediction_dir = tmp_path / "predictions"
    rgb_dir.mkdir()
    depth_dir.mkdir()
    prediction_dir.mkdir()
    Image.fromarray(np.zeros((3, 4, 3), dtype=np.uint8)).save(rgb_dir / "scene_0001.png")
    Image.fromarray(np.full((3, 4), 2000, dtype=np.uint16)).save(depth_dir / "scene_0001.png")
    np.save(prediction_dir / "scene_0001.npy", np.ones((3, 4), dtype=np.float32))
    pairs = discover_pairs(rgb_dir, depth_dir)
    validate_pairs(pairs)
    assert load_depth(pairs[0].depth_path).mean() == 2.0
    assert PrecomputedPredictor(prediction_dir).predict_for_sample("scene_0001", (3, 4)).shape == (3, 4)


def test_summary_exports_region_csv(tmp_path):
    records = [{"sample_id": "scene_0001", "metrics": {"abs_rel": 0.1, "rmse": 0.2, "delta1": 0.9}, "num_regions": 1, "regions": [{"region_id": 1, "mean_error": 0.4, "area": 8, "top_cause": "occlusion", "confidence": "High"}]}]
    write_summary(records, tmp_path)
    assert (tmp_path / "summary.json").exists()
    assert "occlusion" in (tmp_path / "regions.csv").read_text(encoding="utf-8")


def test_extract_official_nyu_mat_layout(tmp_path):
    mat_path = tmp_path / "nyu.mat"
    import h5py

    with h5py.File(mat_path, "w") as handle:
        handle.create_dataset("images", data=np.zeros((1, 3, 4, 3), dtype=np.uint8))
        handle.create_dataset("depths", data=np.full((1, 4, 3), 2.0, dtype=np.float32))
    extracted = extract_labeled_mat(mat_path, tmp_path / "rgb", tmp_path / "depth")
    assert extracted == 1
    assert Image.open(tmp_path / "rgb" / "scene_0001.png").size == (4, 3)
    assert np.allclose(np.load(tmp_path / "depth" / "scene_0001.npy"), 2.0)


def test_features_handle_one_pixel_wide_region():
    rgb = np.zeros((3, 1, 3), dtype=np.uint8)
    depth = np.ones((3, 1), dtype=np.float32)
    region = {"bbox": [0, 0, 1, 3], "mask": np.ones((3, 1), dtype=bool)}
    features = extract_features(rgb, depth, region)
    assert features["depth_discontinuity"] == 0.0
