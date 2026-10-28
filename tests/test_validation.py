import json
from pathlib import Path

import pytest

from veo.scoring import classify
from veo.validation import NEUTRAL_VALUES, ablation_change, agreement_report, labels_from_confusion

V1 = Path(__file__).resolve().parents[1] / "results" / "v1"


def test_agreement_report_reproduces_v1_human_study():
    stored = json.loads((V1 / "human_validation_results.json").read_text(encoding="utf-8"))
    reference, predicted = labels_from_confusion(stored["confusion_matrix"])
    report = agreement_report(reference, predicted)
    assert report["n"] == 50
    assert report["accuracy"] == pytest.approx(0.36)
    assert report["kappa"] == pytest.approx(stored["cohens_kappa_r1_veo"])
    assert report["macro_f1"] == pytest.approx(stored["macro_f1"])
    assert report["abstained"] == 21
    selective = report["selective"]
    assert selective["n"] == 29
    assert selective["accuracy"] == pytest.approx(17 / 29)
    assert selective["kappa"] == pytest.approx(0.4719, abs=1e-4)
    assert selective["majority_label"] == "boundary_mixing"
    assert selective["majority_baseline_accuracy"] == pytest.approx(12 / 29)
    assert (report["per_class"]["reflection"]["correct"], report["per_class"]["reflection"]["predicted"]) == (0, 7)


def test_agreement_report_without_abstentions_has_full_coverage():
    report = agreement_report(["a", "b", "a"], ["a", "a", "a"])
    assert report["coverage"] == 1.0
    assert report["selective"]["accuracy"] == report["accuracy"]


def _region(**overrides):
    features = {
        "texture_var": 600.0, "edge_density": 0.0, "brightness": 30.0, "contrast": 10.0,
        "highlight_ratio": 0.0, "aspect_ratio": 1.0, "depth_discontinuity": 0.0, **overrides,
    }
    return {"features": features, "top_cause": "poor_lighting"}


@pytest.mark.parametrize("signal", sorted(NEUTRAL_VALUES))
def test_ablation_changes_only_the_named_signal(signal, monkeypatch):
    seen = []
    monkeypatch.setattr("veo.validation.classify", lambda features, include_reflection: seen.append(features) or {"top_cause": "x"})
    region = _region()
    ablation_change([{"regions": [region]}], signal)
    changed = {key for key, value in seen[0].items() if value != region["features"][key]}
    assert changed <= {signal}


def test_brightness_ablation_is_not_a_duplicate_of_contrast():
    # Dark, low-contrast region: brightness alone decides poor_lighting
    records = [{"regions": [_region()]}]
    assert ablation_change(records, "brightness")["changed_regions"] == 1
    assert ablation_change(records, "contrast")["changed_regions"] == 1
    # Already mid-grey: neutralising brightness leaves the label unchanged
    mid_grey = _region(brightness=128.0)
    mid_grey["top_cause"] = classify(mid_grey["features"])["top_cause"]
    assert ablation_change([{"regions": [mid_grey]}], "brightness")["changed_regions"] == 0
