import json
import os
from pathlib import Path

import numpy as np
import pytest

from veo.config import ExperimentConfig
from veo.fixtures import SyntheticDisparityPredictor, _scene
from veo.pipeline import analyze_sample
from veo.reproduce import reproduce

REPO = Path(__file__).resolve().parents[1]
GOLDEN = REPO / "tests" / "fixtures" / "golden_analyze_sample.json"


def _golden_view(result: dict) -> dict:
    """The parts of an analysis that must not change silently."""
    return {
        "metrics": {name: round(value, 5) for name, value in result["metrics"].items()},
        "alignment": {name: round(result["alignment"][name], 5) for name in ("scale", "shift")},
        "num_regions": result["num_regions"],
        "regions": [
            {"bbox": region["bbox"], "area": region["area"], "top_cause": region["top_cause"], "confidence": region["confidence"]}
            for region in result["regions"]
        ],
    }


def test_analyze_sample_matches_golden_output():
    rgb, depth = _scene(np.random.default_rng(7), 96, 128)
    prediction = SyntheticDisparityPredictor(seed=7).predict(rgb, depth)
    config = ExperimentConfig(align_scale_shift=True, prediction_space="inverse_depth")
    view = _golden_view(analyze_sample(rgb, depth, prediction, np.ones_like(depth, dtype=bool), config))
    if os.environ.get("VEO_UPDATE_GOLDEN"):
        GOLDEN.parent.mkdir(exist_ok=True)
        GOLDEN.write_text(json.dumps(view, indent=2) + "\n", encoding="utf-8")
    assert view == json.loads(GOLDEN.read_text(encoding="utf-8")), "set VEO_UPDATE_GOLDEN=1 to accept an intended change"


def test_reproduce_fixture_runs_every_stage(tmp_path):
    summary = reproduce(tmp_path, REPO / "configs" / "nyu.yaml", fixture=True)
    results = summary.parent
    for name in ("signal_ablation.json", "scoring_sanity_check.json", "oracle_boundary_filter.json"):
        payload = json.loads((results / name).read_text(encoding="utf-8"))
        assert payload["provenance"]["git_commit"] is not None
    alignment = json.loads((results / "synthetic-disparity" / "alignment_ablation.json").read_text(encoding="utf-8"))
    signs = alignment["summary"]["inverse_depth_scale_shift"]["scale_sign_counts"]
    assert signs["positive"] == len(alignment["per_scene_scales"]) > 0
    assert alignment["summary"]["direct_depth_scale_shift"]["scale_sign_counts"]["negative"] == signs["positive"]
    text = summary.read_text(encoding="utf-8")
    for heading in ("## Model: synthetic-disparity", "## Alignment protocols", "## Signal ablation", "## Oracle boundary filter"):
        assert heading in text
    oracle = json.loads((results / "oracle_boundary_filter.json").read_text(encoding="utf-8"))
    assert oracle["oracle"] is True and oracle["evaluated_scenes"] > 0


def test_reproduce_requires_the_dataset_when_not_a_fixture(tmp_path):
    with pytest.raises(FileNotFoundError, match="download-nyu"):
        reproduce(tmp_path, REPO / "configs" / "nyu.yaml", mat_path=tmp_path / "missing.mat")
