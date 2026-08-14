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
    assert "master_framework --test" in workflow
    assert 'gates["status"] == "PASSED"' in workflow
    assert 'repro["verified"] is True' in workflow


def test_release_workflow_never_overwrites_the_gated_build() -> None:
    """A gate-skipping rebuild must not replace the published artifacts."""

    workflow = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
    packaging_steps = workflow.split("- name: Upload release artifacts")[0]
    assert "--skip-gates" not in packaging_steps.replace("inputs.skip_gates && '--skip-gates'", "")


def test_reproducibility_is_recorded_in_the_manifest() -> None:
    text = SCRIPT.read_text(encoding="utf-8")
    assert '"reproducibility": reproducibility' in text
    assert "double build in one invocation" in text


def test_release_workflow_rejects_a_fallback_sbom() -> None:
    workflow = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
    assert "SBOM fell back to" in workflow


def test_sbom_generator_is_recorded_in_the_manifest() -> None:
    module = load_build_release()
    text = SCRIPT.read_text(encoding="utf-8")
    assert module.PRIMARY_SBOM_GENERATOR == "cyclonedx-py"
    assert module.FALLBACK_SBOM_GENERATOR == "builtin-fallback"
    assert '"generator": SBOM_GENERATOR' in text


def test_release_extra_pins_a_cyclonedx_cli_with_the_environment_command() -> None:
    """`cyclonedx_py environment` exists in 5.x+; older 4.x used a different CLI."""

    import tomllib

    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    pins = data["project"]["optional-dependencies"]["release"]
    cyclonedx = next(pin for pin in pins if pin.startswith("cyclonedx-bom"))
    major = int(cyclonedx.split("==")[1].split(".")[0])
    assert major >= 5, f"{cyclonedx} predates the 'environment' subcommand"


def test_release_workflow_recovers_from_a_moved_tag() -> None:
    """A deleted-and-recreated tag must not leave an orphaned draft release."""

    workflow = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
    assert "--verify-tag" in workflow
    assert "stale or draft release" in workflow
    assert "Confirm exactly one published release for the tag" in workflow


def test_monthly_research_workflow_keeps_the_human_in_the_loop() -> None:
    """The scheduled cycle must propose only, and prove it did not apply anything."""

    workflow = (ROOT / ".github/workflows/research-monthly.yml").read_text(encoding="utf-8")

    assert "cron: '15 1 1 * *'" in workflow, "monthly schedule"
    assert "Assert the cycle changed no theory confidence" in workflow
    assert "a cron cycle must not change confidence" in workflow
    # state is kept off main so a scheduled job never rewrites released code
    assert "research-state" in workflow
    assert "branch: main" not in workflow
    # a reviewer is told, rather than the queue growing silently
    assert "gh issue create" in workflow
    # rsync --delete would otherwise remove the worktree's .git link, and the
    # resulting git failure inside an `if` condition is swallowed: the first real
    # run reported success while publishing nothing
    assert "--exclude .git" in workflow
    assert "Confirm the published state is reachable" in workflow
    assert "the research-state branch is missing" in workflow
