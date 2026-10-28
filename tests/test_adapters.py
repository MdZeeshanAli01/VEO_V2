"""Model adapters and model-backed CLI commands, with torch/transformers replaced by stand-ins."""

import sys
import types
from pathlib import Path

import numpy as np
import pytest

from veo import cli
from veo.fixtures import write_fixture_mat
from veo.inference import (
    OfficialMetricDepthPredictor,
    PrecomputedPredictor,
    TransformersDepthPredictor,
)

REPO = Path(__file__).resolve().parents[1]


class FakeTensor:
    def __init__(self, array):
        self._array = array

    def squeeze(self):
        return FakeTensor(np.squeeze(self._array))

    def detach(self):
        return self

    def cpu(self):
        return self

    def numpy(self):
        return self._array


@pytest.fixture
def fake_torch(monkeypatch):
    torch = types.ModuleType("torch")
    torch.cuda = types.SimpleNamespace(is_available=lambda: False)
    torch.load = lambda path, map_location=None: {"weights": str(path)}
    monkeypatch.setitem(sys.modules, "torch", torch)
    return torch


@pytest.fixture
def fake_transformers(monkeypatch, fake_torch):
    created = {}

    def pipeline(task, model, device):
        created.update(task=task, model=model, device=device)

        def run(images, batch_size=None):
            def one(image):
                height, width = np.asarray(image).shape[:2]
                return {"predicted_depth": FakeTensor(np.ones((1, height // 2, width // 2), dtype=np.float32))}
            return [one(image) for image in images] if isinstance(images, list) else one(images)

        return run

    module = types.ModuleType("transformers")
    module.pipeline = pipeline
    monkeypatch.setitem(sys.modules, "transformers", module)
    return created


def test_transformers_predictor_resizes_to_input(fake_transformers):
    predictor = TransformersDepthPredictor("org/model", device="auto")
    assert fake_transformers == {"task": "depth-estimation", "model": "org/model", "device": -1}
    rgb = np.zeros((48, 64, 3), dtype=np.uint8)
    assert predictor.predict(rgb).shape == (48, 64)
    assert [p.shape for p in predictor.predict_batch([rgb, rgb])] == [(48, 64), (48, 64)]


def test_transformers_predictor_explains_missing_extra(monkeypatch):
    monkeypatch.setitem(sys.modules, "transformers", None)
    with pytest.raises(ImportError, match="model"):
        TransformersDepthPredictor("org/model")


def test_official_metric_predictor_loads_checkpoint(tmp_path, monkeypatch, fake_torch):
    checkpoint = tmp_path / "metric.pth"
    checkpoint.write_bytes(b"")
    loaded = {}

    class DepthAnythingV2:
        def __init__(self, **config):
            loaded["config"] = config

        def load_state_dict(self, state):
            loaded["state"] = state

        def to(self, device):
            loaded["device"] = device
            return self

        def eval(self):
            return self

        def infer_image(self, bgr):
            return np.full(bgr.shape[:2], 2.5)

    package = types.ModuleType("depth_anything_v2")
    dpt = types.ModuleType("depth_anything_v2.dpt")
    dpt.DepthAnythingV2 = DepthAnythingV2
    monkeypatch.setitem(sys.modules, "depth_anything_v2", package)
    monkeypatch.setitem(sys.modules, "depth_anything_v2.dpt", dpt)
    predictor = OfficialMetricDepthPredictor(tmp_path, checkpoint, "vitb", max_depth=20.0)
    assert loaded["config"]["encoder"] == "vitb" and loaded["config"]["max_depth"] == 20.0
    assert loaded["device"] == "cpu"
    prediction = predictor.predict(np.zeros((8, 10, 3), dtype=np.uint8))
    assert prediction.dtype == np.float32 and prediction.shape == (8, 10)


def test_official_metric_predictor_requires_checkpoint(tmp_path, fake_torch):
    with pytest.raises(FileNotFoundError):
        OfficialMetricDepthPredictor(tmp_path, tmp_path / "missing.pth")


def test_precomputed_predictor_checks_shape(tmp_path):
    np.save(tmp_path / "a.npy", np.ones((3, 4), dtype=np.float32))
    with pytest.raises(ValueError, match="shape"):
        PrecomputedPredictor(tmp_path).predict_for_sample("a", (4, 3))
    with pytest.raises(FileNotFoundError):
        PrecomputedPredictor(tmp_path).predict_for_sample("b", (3, 4))


@pytest.fixture
def recorded(monkeypatch):
    calls = []

    def recorder(name):
        def record(*args, **kwargs):
            calls.append((name, args, kwargs))
            return {"records": []} if name == "run_alignment_ablation" else []
        return record

    for name in ("run_model", "run_precomputed", "run_official_metric", "run_alignment_ablation"):
        monkeypatch.setattr(cli, name, recorder(name))
    return calls


def _main(monkeypatch, *args):
    monkeypatch.setattr(sys, "argv", ["veo", *args])
    cli.main()


def test_model_commands_pass_their_arguments(monkeypatch, recorded, tmp_path):
    config = str(REPO / "configs" / "nyu.yaml")
    _main(monkeypatch, "run-model", "--config", config, "--model-id", "org/m", "--limit", "3", "--output-dir", str(tmp_path))
    _main(monkeypatch, "run-precomputed", "--config", config, "--prediction-dir", str(tmp_path))
    _main(monkeypatch, "run-official-metric", "--config", config, "--encoder", "vitl", "--max-depth", "12")
    names = [name for name, _, _ in recorded]
    assert names == ["run_model", "run_precomputed", "run_official_metric"]
    model_config = recorded[0][1][0]
    assert recorded[0][1][1:] == ("org/m", "auto", 3) and model_config.outputs.directory == tmp_path
    metric_config = recorded[2][1][0]
    assert metric_config.experiment.align_scale_shift is False
    assert metric_config.experiment.model_name == "metric_hypersim_vitl"
    assert recorded[2][1][3:5] == ("vitl", 12.0)


def test_split_commands_run_each_split(monkeypatch, recorded, tmp_path):
    config = str(REPO / "configs" / "nyu.yaml")
    _main(monkeypatch, "evaluate-splits", "--config", config, "--split-root", str(tmp_path), "--output-dir", str(tmp_path / "eval"))
    _main(monkeypatch, "compare-alignment", "--config", config, "--split-root", str(tmp_path), "--output-dir", str(tmp_path / "align"))
    splits = [args[0].dataset.split for _, args, _ in recorded]
    assert splits == ["development", "validation", "test"] * 2


def test_extract_and_split_commands_on_fixture_mat(monkeypatch, tmp_path):
    mat = write_fixture_mat(tmp_path / "nyu.mat", scenes=6)
    _main(monkeypatch, "extract-nyu", "--mat-path", str(mat), "--rgb-dir", str(tmp_path / "rgb"), "--depth-dir", str(tmp_path / "depth"), "--count", "3")
    assert len(list((tmp_path / "rgb").glob("*.png"))) == 3
    _main(monkeypatch, "prepare-nyu-splits", "--mat-path", str(mat), "--output-dir", str(tmp_path / "splits"))
    for split in ("development", "validation", "test"):
        assert (tmp_path / "splits" / split / "manifest.txt").exists()
