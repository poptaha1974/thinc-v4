# -*- coding: utf-8 -*-
"""Documentation layout and link guards.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

Two documents were named `ARCHITECTURE.md` — one for the packaged engine and one
for the service layer — which is why the service-layer docs now live under
`docs/api/`. These tests keep that split and catch links broken by future moves.
"""
from __future__ import annotations

import re
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
SKIP_DIRS = {".git", ".venv", "dist", "build", "node_modules", "__pycache__"}


def markdown_files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*.md")
        if not any(part in SKIP_DIRS for part in path.parts)
    ]


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
