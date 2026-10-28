import hashlib
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "web_app"))
import fetch_assets  # noqa: E402


@pytest.fixture
def web_root(tmp_path, monkeypatch):
    payload = b"asset bytes"
    monkeypatch.setattr(fetch_assets, "WEB_ROOT", tmp_path)
    monkeypatch.setattr(fetch_assets, "ASSETS", {"data/file.js": hashlib.sha256(payload).hexdigest()})
    return tmp_path, payload


def _serve(monkeypatch, body: bytes) -> list[str]:
    calls = []

    def fake_urlretrieve(url, destination):
        calls.append(url)
        Path(destination).write_bytes(body)

    monkeypatch.setattr(fetch_assets.urllib.request, "urlretrieve", fake_urlretrieve)
    return calls


def test_downloads_missing_file_and_verifies_checksum(web_root, monkeypatch):
    root, payload = web_root
    calls = _serve(monkeypatch, payload)
    monkeypatch.setattr(sys, "argv", ["fetch_assets.py"])
    assert fetch_assets.main() == 0
    assert (root / "data" / "file.js").read_bytes() == payload
    assert calls == [f"{fetch_assets.RELEASE}/file.js"]


def test_present_file_with_matching_checksum_is_not_downloaded(web_root, monkeypatch):
    root, payload = web_root
    (root / "data").mkdir()
    (root / "data" / "file.js").write_bytes(payload)
    calls = _serve(monkeypatch, b"unused")
    monkeypatch.setattr(sys, "argv", ["fetch_assets.py"])
    assert fetch_assets.main() == 0
    assert calls == []


def test_checksum_mismatch_is_rejected_and_leaves_no_file(web_root, monkeypatch):
    root, _ = web_root
    _serve(monkeypatch, b"tampered")
    monkeypatch.setattr(sys, "argv", ["fetch_assets.py"])
    with pytest.raises(RuntimeError, match="Checksum mismatch"):
        fetch_assets.main()
    assert not (root / "data" / "file.js").exists()
    assert not list((root / "data").glob("*.part"))


def test_check_mode_reports_missing_files(web_root, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["fetch_assets.py", "--check"])
    assert fetch_assets.main() == 1


def test_real_manifest_matches_files_in_checkout():
    # Fails if a regenerated video/data file is committed without updating the checksums
    missing = [name for name, digest in fetch_assets.ASSETS.items() if (fetch_assets.WEB_ROOT / name).exists() and not fetch_assets.is_current(fetch_assets.WEB_ROOT / name, digest)]
    assert missing == []
