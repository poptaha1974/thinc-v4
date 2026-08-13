# -*- coding: utf-8 -*-
"""Documentation layout and link guards.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

Two documents were named `ARCHITECTURE.md` — one for the packaged engine and one
for the service layer — which is why the service-layer docs now live under
`docs/api/`. These tests keep that split and catch links broken by future moves.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
API_DOCS = DOCS / "api"

SERVICE_LAYER_DOCS = {
    "ADAPTIVE_MARKET_LEARNING.md",
    "API_CONTRACT.md",
    "API_SOCIAL_CULTURE_ADDENDUM.md",
    "ARCHITECTURE.md",
    "DATA_MODEL.md",
    "EGYPTIAN_SOCIAL_CULTURAL_ENGINE.md",
    "EXTERNAL_SOCIAL_RESEARCH_INTELLIGENCE.md",
    "GIFT_DECISION_INTELLIGENCE.md",
    "LEGAL_GUARDRAILS.md",
    "MVP_SCOPE.md",
    "ROADMAP.md",
}

LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def markdown_files() -> list[Path]:
    """Only the Markdown we own.

    Walking the tree would also pick up generated or third-party files such as
    ``dist/RELEASE_NOTES.md`` or ``.pytest_cache/README.md``, which makes the
    collected test count depend on whether a build or a previous run happened —
    and would fail this suite over links we do not control.
    """

    listed = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-z", "*.md"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return [ROOT / name for name in listed.split("\0") if name]


def test_service_layer_docs_live_under_docs_api() -> None:
    assert SERVICE_LAYER_DOCS <= {path.name for path in API_DOCS.glob("*.md")}


def test_docs_root_holds_no_loose_service_layer_docs() -> None:
    stray = {path.name for path in DOCS.glob("*.md")} & SERVICE_LAYER_DOCS
    assert stray == set(), f"these belong in docs/api/: {sorted(stray)}"


def test_engine_and_service_architecture_docs_are_separate() -> None:
    assert (API_DOCS / "ARCHITECTURE.md").exists()
    assert (DOCS / "v4_2" / "ARCHITECTURE.md").exists()


def test_api_docs_index_lists_every_document() -> None:
    index = (API_DOCS / "README.md").read_text(encoding="utf-8")
    missing = [name for name in sorted(SERVICE_LAYER_DOCS) if name not in index]
    assert missing == []


def test_the_link_scan_covers_every_tracked_markdown_file() -> None:
    """Guard the guard: a broken file list would silently scan nothing."""

    scanned = markdown_files()
    assert len(scanned) >= 25
    assert ROOT / "README.md" in scanned
    assert ROOT / "docs/api/README.md" in scanned
    assert all(path.exists() for path in scanned)


@pytest.mark.parametrize("path", markdown_files(), ids=lambda p: str(p.relative_to(ROOT)))
def test_relative_markdown_links_resolve(path: Path) -> None:
    broken: list[str] = []
    for target in LINK_PATTERN.findall(path.read_text(encoding="utf-8")):
        target = target.split(" ")[0].split("#")[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "pplx://", "<")):
            continue
        candidate = (ROOT if target.startswith("/") else path.parent) / target.lstrip("/")
        if not candidate.exists():
            broken.append(target)
    assert broken == [], f"{path.relative_to(ROOT)} links to missing files: {broken}"
