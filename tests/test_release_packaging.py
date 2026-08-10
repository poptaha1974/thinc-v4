# -*- coding: utf-8 -*-
"""Tests for the release-packaging contract (no build required).

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
"""
from __future__ import annotations

import gzip
import hashlib
import importlib.util
import io
import sys
import tarfile
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/build_release.py"


def load_build_release() -> ModuleType:
    spec = importlib.util.spec_from_file_location("build_release", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["build_release"] = module
    spec.loader.exec_module(module)
    return module


def test_release_script_declares_expected_outputs() -> None:
    text = SCRIPT.read_text(encoding="utf-8")
    for expected in ("SHA256SUMS", "sbom.cyclonedx.json", "RELEASE_MANIFEST.json", "RELEASE_NOTES.md"):
        assert expected in text


def test_sha256_helper_matches_hashlib(tmp_path: Path) -> None:
    module = load_build_release()
    payload = b"THINC v4.2 \xd8\xa5\xd9\x8a\xd9\x87\xd8\xa7\xd8\xa8 \xd8\xb7\xd9\x87"
    target = tmp_path / "artifact.bin"
    target.write_bytes(payload)
    assert module.sha256_of(target) == hashlib.sha256(payload).hexdigest()


def test_project_version_is_the_single_source_of_truth() -> None:
    module = load_build_release()
    import thinc_v4

    assert module.project_version() == thinc_v4.__version__


def test_sdist_normalization_is_deterministic(tmp_path: Path) -> None:
    module = load_build_release()

    def make_archive(path: Path, mtime: int) -> None:
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode="w") as tar:
            for name, body in (("pkg/a.py", b"a = 1\n"), ("pkg/b.py", b"b = 2\n")):
                info = tarfile.TarInfo(name)
                info.size = len(body)
                info.mtime = mtime
                info.uid = 1000
                info.gid = 1000
                info.uname = "builder"
                info.mode = 0o600
                tar.addfile(info, io.BytesIO(body))
        with path.open("wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=mtime) as gz:
            gz.write(buffer.getvalue())

    first = tmp_path / "first.tar.gz"
    second = tmp_path / "second.tar.gz"
    make_archive(first, 111)
    make_archive(second, 999)

    module._normalize_sdist(first, 1700000000)
    module._normalize_sdist(second, 1700000000)

    assert first.read_bytes() == second.read_bytes()

    with tarfile.open(first, "r:gz") as tar:
        members = tar.getmembers()
    assert [m.name for m in members] == ["pkg/a.py", "pkg/b.py"]
    assert {m.mtime for m in members} == {1700000000}
    assert {m.uid for m in members} == {0}
    assert {m.uname for m in members} == {""}
    assert {m.mode for m in members} == {0o644}


def test_release_workflow_verifies_checksums_and_reproducibility() -> None:
    workflow = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
    assert "sha256sum -c SHA256SUMS" in workflow
    assert "Reproducible build confirmed" in workflow
    assert "master_framework --test" in workflow
