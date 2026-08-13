#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a documented, verifiable THINC release package.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

Produces, under `dist/`:
- `thinc_v4-<version>.tar.gz` and `thinc_v4-<version>-py3-none-any.whl`
- `SHA256SUMS` — `sha256sum -c`-compatible checksum file
- `sbom.cyclonedx.json` — CycloneDX 1.5 SBOM of the package and its dependencies
- `RELEASE_MANIFEST.json` — artifacts, digests, tool versions, git commit,
  quality-gate results, and the THINC identity hash
- `RELEASE_NOTES.md` — human-readable release record with verification steps

Usage:
    python scripts/build_release.py [--skip-gates]

Determinism: `SOURCE_DATE_EPOCH` is pinned to the HEAD commit time (or to
`SOURCE_DATE_EPOCH` if already set), so rebuilding the same commit with the same
toolchain reproduces the same archives.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def run(command: list[str], *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    print(f"$ {' '.join(command)}", flush=True)
    return subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True, check=False)


def must_run(command: list[str], *, env: dict[str, str] | None = None) -> str:
    result = run(command, env=env)
    if result.returncode != 0:
        sys.stderr.write(result.stdout + result.stderr)
        raise SystemExit(f"command failed: {' '.join(command)}")
    return result.stdout.strip()


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def project_version() -> str:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    version: str = data["project"]["version"]
    return version


def git_metadata() -> dict[str, str]:
    commit = must_run(["git", "rev-parse", "HEAD"])
    branch = must_run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    dirty = must_run(["git", "status", "--porcelain"])
    commit_epoch = must_run(["git", "log", "-1", "--pretty=%ct"])
    return {
        "commit": commit,
        "branch": branch,
        "worktree": "dirty" if dirty else "clean",
        "commit_epoch": commit_epoch,
    }


def quality_gates(skip: bool) -> dict[str, Any]:
    if skip:
        return {"status": "SKIPPED"}
    gates: dict[str, Any] = {}
    for name, command in (
        ("ruff", [sys.executable, "-m", "ruff", "check", "."]),
        ("mypy", [sys.executable, "-m", "mypy"]),
        ("pytest", [sys.executable, "-m", "pytest", "-q"]),
    ):
        result = run(command)
        gates[name] = {
            "command": " ".join(command),
            "returncode": result.returncode,
            "summary": (result.stdout.strip().splitlines() or [""])[-1],
        }
        if result.returncode != 0:
            sys.stderr.write(result.stdout + result.stderr)
            raise SystemExit(f"quality gate failed: {name}")

    selftest = run([sys.executable, "-m", "thinc_v4.v4_2.master_framework", "--test"])
    if selftest.returncode != 0:
        sys.stderr.write(selftest.stdout + selftest.stderr)
        raise SystemExit("quality gate failed: v4.2 self-test")
    payload = json.loads(selftest.stdout)
    gates["v4_2_selftest"] = {
        "passed": payload["passed"],
        "failed": payload["failed"],
        "success_rate": payload["success_rate"],
        "v3_status": payload["v3_status"],
    }
    gates["status"] = "PASSED"
    return gates


def build_distributions(source_date_epoch: str, outdir: Path = DIST) -> list[Path]:
    if outdir.exists():
        shutil.rmtree(outdir)
    env = dict(os.environ)
    env["SOURCE_DATE_EPOCH"] = source_date_epoch
    env["PYTHONHASHSEED"] = "0"
    must_run([sys.executable, "-m", "build", "--sdist", "--wheel", "--outdir", str(outdir)], env=env)
    for archive in outdir.glob("*.tar.gz"):
        _normalize_sdist(archive, int(source_date_epoch))
    return sorted(p for p in outdir.iterdir() if p.suffix in {".gz", ".whl"})


def verify_reproducible(source_date_epoch: str, artifacts: list[Path]) -> dict[str, Any]:
    """Rebuild the archives in a scratch directory and compare digests.

    Running the check inside the same invocation keeps the published manifest and
    notes describing the *gated* build, instead of being overwritten by a second,
    gate-skipping build.
    """

    expected = {path.name: sha256_of(path) for path in artifacts}
    with tempfile.TemporaryDirectory(prefix="thinc-repro-") as scratch:
        rebuilt = build_distributions(source_date_epoch, Path(scratch) / "dist")
        actual = {path.name: sha256_of(path) for path in rebuilt}
    mismatches = sorted(
        name for name in expected if expected[name] != actual.get(name)
    )
    if mismatches:
        raise SystemExit(f"build is not reproducible: {mismatches}")
    return {
        "verified": True,
        "method": "double build in one invocation, archive digests compared",
        "archives": sorted(expected),
    }


def _normalize_sdist(archive: Path, mtime: int) -> None:
    """Rewrite an sdist deterministically so its SHA-256 is reproducible.

    setuptools does not fully pin tar member metadata, and the gzip container
    header embeds the wall-clock build time. Every member is re-emitted in name
    order with a fixed mtime, ownership, and normalized permissions.
    """

    with tarfile.open(archive, "r:gz") as source:
        members = sorted(source.getmembers(), key=lambda m: m.name)
        payloads: list[tuple[tarfile.TarInfo, bytes | None]] = []
        for member in members:
            data = source.extractfile(member).read() if member.isfile() else None  # type: ignore[union-attr]
            payloads.append((member, data))

    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w", format=tarfile.PAX_FORMAT) as target:
        for member, data in payloads:
            member.mtime = mtime
            member.uid = member.gid = 0
            member.uname = member.gname = ""
            member.mode = 0o755 if member.isdir() else 0o644
            member.pax_headers = {}
            target.addfile(member, io.BytesIO(data) if data is not None else None)

    with open(archive, "wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=mtime, compresslevel=9) as gz:
            gz.write(buffer.getvalue())


#: Set by `build_sbom` so the manifest records which generator actually ran.
SBOM_GENERATOR = "unknown"
PRIMARY_SBOM_GENERATOR = "cyclonedx-py"
FALLBACK_SBOM_GENERATOR = "builtin-fallback"


def build_sbom(version: str, artifacts: list[Path], git: dict[str, str]) -> Path:
    """Generate a CycloneDX SBOM, falling back to a self-built document."""

    global SBOM_GENERATOR

    target = DIST / "sbom.cyclonedx.json"
    generated = run(
        [
            sys.executable,
            "-m",
            "cyclonedx_py",
            "environment",
            "--pyproject",
            str(ROOT / "pyproject.toml"),
            "--mc-type",
            "application",
            "--spec-version",
            "1.5",
            "--output-format",
            "JSON",
            "--output-reproducible",
            "-o",
            str(target),
        ]
    )
    if generated.returncode == 0 and target.exists():
        SBOM_GENERATOR = PRIMARY_SBOM_GENERATOR
        print(f"SBOM: generated with {PRIMARY_SBOM_GENERATOR}")
        _annotate_sbom(target, version, artifacts, git)
        return target

    SBOM_GENERATOR = FALLBACK_SBOM_GENERATOR
    print("SBOM: cyclonedx-py unavailable, writing a minimal CycloneDX 1.5 document")
    sys.stderr.write(
        "WARNING: falling back to the minimal SBOM. Install the pinned "
        "'cyclonedx-bom' from the 'release' extra for a full dependency SBOM.\n"
    )
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    dependencies = data["project"].get("dependencies", [])
    components: list[dict[str, Any]] = []
    for requirement in dependencies:
        name, _, pinned = requirement.partition("==")
        components.append(
            {
                "type": "library",
                "name": name.strip(),
                "version": pinned.strip() or "unpinned",
                "purl": f"pkg:pypi/{name.strip().lower()}@{pinned.strip()}" if pinned else None,
                "scope": "required",
            }
        )
    document = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "version": 1,
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tools": [{"vendor": "Egy-Pioneers", "name": "thinc build_release.py", "version": version}],
            "authors": [{"name": "Dr. Ehab Taha (الدكتور إيهاب طه)"}],
            "component": {
                "type": "application",
                "name": data["project"]["name"],
                "version": version,
                "description": data["project"]["description"],
                "licenses": [{"license": {"name": "Proprietary — © 2026 Dr. Ehab Taha"}}],
                "hashes": [
                    {"alg": "SHA-256", "content": sha256_of(path)} for path in artifacts
                ],
                "properties": [
                    {"name": "git.commit", "value": git["commit"]},
                    {"name": "python.requires", "value": data["project"]["requires-python"]},
                ],
            },
        },
        "components": components,
    }
    target.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target


def _annotate_sbom(target: Path, version: str, artifacts: list[Path], git: dict[str, str]) -> None:
    """Attach artifact digests, commit, and ownership properties to the SBOM."""

    document: dict[str, Any] = json.loads(target.read_text(encoding="utf-8"))
    metadata = document.setdefault("metadata", {})
    component = metadata.setdefault("component", {})
    component.setdefault("name", "thinc-v4")
    component["version"] = version
    properties = component.setdefault("properties", [])
    properties.append({"name": "thinc:git.commit", "value": git["commit"]})
    properties.append({"name": "thinc:owner", "value": "Dr. Ehab Taha (الدكتور إيهاب طه)"})
    for path in artifacts:
        properties.append({"name": f"thinc:artifact.sha256:{path.name}", "value": sha256_of(path)})
    target.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-gates", action="store_true", help="skip lint/type/test gates")
    parser.add_argument(
        "--skip-reproducibility-check",
        action="store_true",
        help="skip the second build used to prove reproducibility",
    )
    args = parser.parse_args()

    version = project_version()
    git = git_metadata()
    source_date_epoch = os.environ.get("SOURCE_DATE_EPOCH", git["commit_epoch"])

    gates = quality_gates(args.skip_gates)
    artifacts = build_distributions(source_date_epoch)
    reproducibility: dict[str, Any] = {"verified": False, "method": "SKIPPED"}
    if not args.skip_reproducibility_check:
        reproducibility = verify_reproducible(source_date_epoch, artifacts)
        print("Reproducible build confirmed")
    sbom_path = build_sbom(version, artifacts, git)

    from thinc_v4 import __version__ as package_version
    from thinc_v4.v4_2.identity import compute_identity_hash, get_watermark, verify_attribution

    if package_version != version:
        raise SystemExit(f"version drift: pyproject={version} package={package_version}")
    if not verify_attribution():
        raise SystemExit("identity protection violated: attribution was modified")

    checksum_targets = artifacts + [sbom_path]
    digests = {path.name: sha256_of(path) for path in checksum_targets}
    (DIST / "SHA256SUMS").write_text(
        "".join(f"{digest}  {name}\n" for name, digest in sorted(digests.items())),
        encoding="utf-8",
    )

    manifest: dict[str, Any] = {
        "package": "thinc-v4",
        "version": version,
        "layers": {"v4_0": "4.0", "v4_2": "4.2"},
        "built_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_date_epoch": source_date_epoch,
        "git": git,
        "builder": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
        },
        "identity": {
            "inventor": "Dr. Ehab Taha (الدكتور إيهاب طه)",
            "identity_hash_sha256": compute_identity_hash(),
            "attribution_verified": True,
        },
        "quality_gates": gates,
        "reproducibility": reproducibility,
        "artifacts": [
            {"name": path.name, "bytes": path.stat().st_size, "sha256": digests[path.name]}
            for path in checksum_targets
        ],
        "sbom": {
            "file": sbom_path.name,
            "format": "CycloneDX",
            "spec_version": "1.5",
            "generator": SBOM_GENERATOR,
            "components": len(json.loads(sbom_path.read_text(encoding="utf-8")).get("components", [])),
        },
    }
    (DIST / "RELEASE_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    notes = [
        f"# THINC v{version} — Release Record",
        "",
        "**Inventor / Author / Owner:** Dr. Ehab Taha (الدكتور إيهاب طه).",
        f"**Commit:** `{git['commit']}` ({git['worktree']} worktree)  ",
        f"**Built (UTC):** {manifest['built_at_utc']}  ",
        f"**SOURCE_DATE_EPOCH:** `{source_date_epoch}` (reproducible archives)  ",
        f"**Identity hash (SHA-256):** `{manifest['identity']['identity_hash_sha256']}`",
        "",
        "## Artifacts",
        "",
        "| File | Size | SHA-256 |",
        "|---|---|---|",
    ]
    for entry in manifest["artifacts"]:
        notes.append(f"| `{entry['name']}` | {entry['bytes']:,} B | `{entry['sha256']}` |")
    notes += [
        "",
        "## Quality gates",
        "",
        f"```\n{json.dumps(gates, ensure_ascii=False, indent=2)}\n```",
        "",
        "## Reproducibility",
        "",
        f"```\n{json.dumps(reproducibility, ensure_ascii=False, indent=2)}\n```",
        "",
        "## Verification",
        "",
        "```bash",
        "cd dist",
        "sha256sum -c SHA256SUMS",
        "python -c \"import json;print(json.load(open('sbom.cyclonedx.json'))['bomFormat'])\"",
        "```",
        "",
        "## Ownership",
        "",
        get_watermark().strip(),
        "",
        "THINC™ is the proprietary intellectual property of Dr. Ehab Taha (الدكتور إيهاب طه).",
        "Attribution, watermarks, and ownership notices must not be removed or weakened.",
        "",
    ]
    (DIST / "RELEASE_NOTES.md").write_text("\n".join(notes), encoding="utf-8")

    print("\n".join(f"{d}  {n}" for n, d in sorted(digests.items())))
    print(f"\nRelease package ready in {DIST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
