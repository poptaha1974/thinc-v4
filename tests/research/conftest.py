# -*- coding: utf-8 -*-
"""Fixtures for the research line. No test in this package touches the network.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
"""
from __future__ import annotations

from pathlib import Path

import pytest

from thinc_v4.research import (
    EvidenceLevel,
    ProposalGenerator,
    ProposalStore,
    ResearchPaper,
    TheoryRegistry,
)


def make_paper(
    title: str,
    *,
    abstract: str = "",
    journal: str | None = None,
    year: int = 2025,
    citations: int = 10,
    level: EvidenceLevel = EvidenceLevel.CROSS_SECTIONAL,
    external_id: str = "",
    doi: str | None = None,
    keywords: list[str] | None = None,
) -> ResearchPaper:
    """Build a paper without hitting any external source."""

    return ResearchPaper(
        source="test",
        external_id=external_id or f"test:{title[:24]}",
        title=title,
        abstract=abstract,
        journal=journal,
        publication_year=year,
        cited_by_count=citations,
        evidence_level=level,
        doi=doi,
        keywords=keywords or [],
    )


@pytest.fixture()
def registry(tmp_path: Path) -> TheoryRegistry:
    """A registry seeded from the packaged reference data, stored under tmp_path."""

    reg = TheoryRegistry(tmp_path / "theory_registry.json")
    reg.save()
    return reg


@pytest.fixture()
def generator(registry: TheoryRegistry, tmp_path: Path) -> ProposalGenerator:
    return ProposalGenerator(
        registry,
        ProposalStore(tmp_path / "proposals.json"),
        weights_path=tmp_path / "weights.json",
    )
