# -*- coding: utf-8 -*-
"""Data models for the THINC research line (Auto-Updater and theory registry).

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

Ported from the self-updating edition (v4.2.1 EG, 2026-07-31) into the packaged
distribution. Behavioural values — the Cochrane evidence weights, the citation and
recency multipliers, `net_evidence()` — are preserved exactly; the tests pin them.

Changes made during the port, all of them mechanical:
- Pydantic v2 API (`model_dump()` instead of the deprecated `.dict()`).
- Explicit optional types (`int | None`) instead of `int = None`, which MyPy strict
  rejects and which silently typed those fields as non-optional.
- Timezone-aware UTC timestamps instead of naive local ones, so records written in
  Cairo and read anywhere else compare correctly.
"""
from __future__ import annotations

import math
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    """Timezone-aware UTC now, used for every stored timestamp."""

    return datetime.now(timezone.utc)


def _new_id() -> str:
    return str(uuid.uuid4())


class EvidenceLevel(str, Enum):
    """Strength of scientific evidence — Cochrane hierarchy, strongest first."""

    META_ANALYSIS = "meta_analysis"
    SYSTEMATIC_REVIEW = "systematic_review"
    RCT = "randomized_controlled_trial"
    COHORT = "cohort_study"
    CASE_CONTROL = "case_control"
    CROSS_SECTIONAL = "cross_sectional"
    CASE_REPORT = "case_report"
    EXPERT_OPINION = "expert_opinion"


class TheoryStatus(str, Enum):
    ACTIVE = "active"
    CANDIDATE = "candidate"
    DEPRECATED = "deprecated"
    UNDER_REVIEW = "under_review"


class ProposalType(str, Enum):
    """The four kinds of update the generator may propose."""

    NEW_THEORY = "new_theory"
    EVIDENCE_UPDATE = "evidence_update"
    DEPRECATE_THEORY = "deprecate_theory"
    WEIGHT_CHANGE = "weight_change"


#: Evidence level → base weight (0-1).
EVIDENCE_WEIGHTS: Dict[EvidenceLevel, float] = {
    EvidenceLevel.META_ANALYSIS: 1.00,
    EvidenceLevel.SYSTEMATIC_REVIEW: 0.90,
    EvidenceLevel.RCT: 0.80,
    EvidenceLevel.COHORT: 0.60,
    EvidenceLevel.CASE_CONTROL: 0.50,
    EvidenceLevel.CROSS_SECTIONAL: 0.40,
    EvidenceLevel.CASE_REPORT: 0.20,
    EvidenceLevel.EXPERT_OPINION: 0.10,
}

#: Evidence levels strong enough to justify raising a theory's confidence.
STRONG_EVIDENCE: frozenset[EvidenceLevel] = frozenset(
    {EvidenceLevel.META_ANALYSIS, EvidenceLevel.SYSTEMATIC_REVIEW, EvidenceLevel.RCT}
)

#: Evidence levels strong enough to justify proposing a brand-new theory.
NEW_THEORY_EVIDENCE: frozenset[EvidenceLevel] = frozenset(
    {EvidenceLevel.META_ANALYSIS, EvidenceLevel.SYSTEMATIC_REVIEW}
)


class ResearchPaper(BaseModel):
    """A paper pulled from an open scientific database."""

    paper_id: str = Field(default_factory=_new_id)
    source: str
    external_id: str
    title: str
    authors: List[str] = Field(default_factory=list)
    publication_year: int
    journal: str | None = None
    doi: str | None = None
    url: str | None = None
    abstract: str | None = None
    cited_by_count: int = 0
    evidence_level: EvidenceLevel = EvidenceLevel.CROSS_SECTIONAL
    keywords: List[str] = Field(default_factory=list)
    related_theories: List[str] = Field(default_factory=list)
    fetched_at: datetime = Field(default_factory=utc_now)
    relevance_score: float = 0.0

    def evidence_weight(self, *, now_year: int | None = None) -> float:
        """Evidence strength as a 0-1 weight: level, citations, and recency.

        `now_year` exists so tests can pin the recency multiplier instead of
        depending on the calendar — the kind of time coupling that broke CI in
        4.2.1.
        """

        base = EVIDENCE_WEIGHTS.get(self.evidence_level, 0.3)
        citation_boost = min(0.3, math.log10(max(1, self.cited_by_count)) / 10)
        current_year = now_year if now_year is not None else utc_now().year
        recency = max(0.5, 1.0 - (current_year - self.publication_year) * 0.1)
        return round(min(1.0, base + citation_boost) * recency, 3)

    def searchable_text(self) -> str:
        """Lowercased title + abstract + keywords, used by filtering and matching."""

        return " ".join(
            [self.title or "", self.abstract or "", " ".join(self.keywords)]
        ).lower()

    def dedupe_key(self) -> str:
        """Identity used to avoid storing the same paper twice."""

        return (self.doi or self.external_id or self.paper_id).lower()


class Theory(BaseModel):
    """A behavioural or marketing theory tracked in the registry."""

    theory_id: str
    name_en: str
    name_ar: str
    category: str
    original_author: str | None = None
    original_year: int | None = None
    current_version: str = "1.0"
    status: TheoryStatus = TheoryStatus.ACTIVE
    description_ar: str = ""
    supporting_papers: List[str] = Field(default_factory=list)
    contradicting_papers: List[str] = Field(default_factory=list)
    confidence_score: float = 0.7
    last_updated: datetime = Field(default_factory=utc_now)
    added_at: datetime = Field(default_factory=utc_now)
    tags: List[str] = Field(default_factory=list)

    def net_evidence(self) -> float:
        """Supporting share of the linked evidence; 0.5 when nothing is linked."""

        total = len(self.supporting_papers) + len(self.contradicting_papers)
        if total == 0:
            return 0.5
        return round(len(self.supporting_papers) / total, 3)

    def matches(self, text: str) -> bool:
        """Whether `text` (already lowercased) mentions this theory or a tag."""

        if self.name_en.lower() in text:
            return True
        return any(tag.lower() in text for tag in self.tags if tag)


class UpdateProposal(BaseModel):
    """A proposed change awaiting Dr. Ehab Taha's review. Never auto-applied."""

    proposal_id: str = Field(default_factory=_new_id)
    created_at: datetime = Field(default_factory=utc_now)
    proposal_type: ProposalType
    target: str
    current_value: Any | None = None
    proposed_value: Any = None
    justification: str
    supporting_paper_ids: List[str] = Field(default_factory=list)
    confidence: float = 0.5
    approved: bool | None = None
    reviewed_at: datetime | None = None
    reviewer_notes: str | None = None

    @property
    def pending(self) -> bool:
        return self.approved is None


class UpdateRun(BaseModel):
    """One full update cycle."""

    run_id: str = Field(default_factory=_new_id)
    started_at: datetime = Field(default_factory=utc_now)
    completed_at: datetime | None = None
    sources_queried: List[str] = Field(default_factory=list)
    papers_fetched: int = 0
    papers_filtered_out: int = 0
    papers_new: int = 0
    proposals_generated: int = 0
    proposals_approved: int = 0
    proposals_rejected: int = 0
    triggered_by: str = "cron"
    status: str = "running"
    error: str | None = None
    queries_failed: List[str] = Field(default_factory=list)
