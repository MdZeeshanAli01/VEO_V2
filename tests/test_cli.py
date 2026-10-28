import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest

from veo import cli

REPO = Path(__file__).resolve().parents[1]


def run_cli(monkeypatch, *args: str) -> None:
    monkeypatch.setattr(sys, "argv", ["veo", *args])
    cli.main()


@pytest.fixture(scope="module")
def fixture_run(tmp_path_factory):
    workdir = tmp_path_factory.mktemp("cli")
    with pytest.MonkeyPatch.context() as monkeypatch:
        run_cli(monkeypatch, "reproduce", "--fixture", "--workdir", str(workdir), "--config", str(REPO / "configs" / "nyu.yaml"))
    outputs = workdir / "outputs" / "fixture"
    return {
        "workdir": workdir,
        "split": outputs / "splits" / "test",
        "model_dir": outputs / "synthetic-disparity",
        "summary": workdir / "results" / "fixture" / "SUMMARY.md",
    }


def test_smoke_command(monkeypatch, capsys):
    run_cli(monkeypatch, "smoke")
    assert "Smoke test passed" in capsys.readouterr().out


def test_reproduce_command_writes_summary(fixture_run):
    assert "## Model: synthetic-disparity" in fixture_run["summary"].read_text(encoding="utf-8")


def test_manifest_command(monkeypatch, fixture_run, tmp_path):
    split = fixture_run["split"]
    run_cli(monkeypatch, "manifest", "--config", str(REPO / "configs" / "nyu.yaml"), "--manifest", str(split / "manifest.txt"), "--output-dir", str(tmp_path))
    manifest = json.loads(next(tmp_path.glob("*_manifest.json")).read_text(encoding="utf-8"))
    assert len(manifest) == len((split / "manifest.txt").read_text(encoding="utf-8").split())  // 2


def test_prepare_rating_then_human_agreement(monkeypatch, fixture_run, tmp_path):
    split, model_dir = fixture_run["split"], fixture_run["model_dir"]
    results_path = model_dir / "model_results.json"
    rating_dir = tmp_path / "rating"
    run_cli(
        monkeypatch, "prepare-rating", "--results-path", str(results_path), "--rgb-dir", str(split / "rgb"),
        "--depth-dir", str(split / "depth"), "--prediction-dir", str(model_dir / "predictions"),
        "--output-dir", str(rating_dir), "--limit", "6",
    )
    with (rating_dir / "rating_template.csv").open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 6 and all(Path(row["panel_path"]).exists() for row in rows)

    for name, label in (("rater1.csv", "textureless"), ("rater2.csv", "boundary_mixing")):
        with (tmp_path / name).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["rating_id", "human_label"])
            writer.writeheader()
            writer.writerows({"rating_id": row["rating_id"], "human_label": label} for row in rows)
    output = tmp_path / "human_agreement.json"
    subprocess.run(
        [sys.executable, str(REPO / "experiments" / "human_agreement.py"), "--rater1", str(tmp_path / "rater1.csv"),
         "--rater2", str(tmp_path / "rater2.csv"), "--results-path", str(results_path), "--count", "6", "--output", str(output)],
        check=True, env={**__import__("os").environ, "PYTHONPATH": str(REPO / "src")},
    )
    result = json.loads(output.read_text(encoding="utf-8"))
    assert result["veo_vs_rater1"]["n"] == 6
    assert result["inter_rater_kappa"] is not None


def test_download_nyu_skips_existing_file(tmp_path, capsys):
    target = tmp_path / "nyu.mat"
    target.write_bytes(b"not really a mat file")
    (tmp_path / "splits.mat").write_bytes(b"nor this")
    cli.download_nyu(target, url="http://invalid.example/never", splits_url="http://invalid.example/never")
    assert capsys.readouterr().out.count("sha256") == 2
