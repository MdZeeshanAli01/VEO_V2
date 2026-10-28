"""Record where a result came from: code version, configuration and environment."""

import hashlib
import json
import platform
import subprocess
import sys
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path

PACKAGES = ("veo", "numpy", "scipy", "opencv-python", "pillow", "h5py", "torch", "transformers")


def _git(*args: str) -> str | None:
    try:
        completed = subprocess.run(["git", *args], capture_output=True, text=True, timeout=10, check=True)
    except (OSError, subprocess.SubprocessError):
        return None
    return completed.stdout.strip()


def _version(package: str) -> str | None:
    try:
        return metadata.version(package)
    except metadata.PackageNotFoundError:
        return None


def config_hash(config) -> str:
    """Stable short hash of a config dataclass or dict, so results from different settings never collide."""
    values = asdict(config) if is_dataclass(config) else config
    encoded = json.dumps(values, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:16]


def file_sha256(path: Path, chunk_size: int = 1 << 20) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def provenance(config=None, inputs: dict[str, Path] | None = None) -> dict:
    """Provenance block to embed in every result file."""
    status = _git("status", "--porcelain")
    record = {
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "git_commit": _git("rev-parse", "HEAD"),
        "git_dirty": bool(status) if status is not None else None,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": {name: _version(name) for name in PACKAGES},
    }
    if config is not None:
        record["config_hash"] = config_hash(config)
    if inputs:
        record["inputs"] = {
            name: {"path": str(path), "sha256": file_sha256(path) if path.is_file() else None}
            for name, path in inputs.items()
        }
    return record
