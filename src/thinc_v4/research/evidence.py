# -*- coding: utf-8 -*-
"""Cochrane-style evidence grading for research papers.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

Pure functions over a paper's own text — no network, no state — so the grading
rules are fully testable. The keyword sets and their precedence are ported
unchanged from the self-updating edition.
"""
from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple

from .models import EvidenceLevel, ResearchPaper

META_KEYWORDS: Tuple[str, ...] = (
    "meta-analysis",
    "meta analysis",
    "metaanalysis",
    "systematic review",
    "cochrane review",
    "network meta-analysis",
)
RCT_KEYWORDS: Tuple[str, ...] = (
    "randomized controlled trial",
    "randomised controlled trial",
    "rct",
    "double-blind",
    "placebo-controlled",
    "randomized clinical",
)
COHORT_KEYWORDS: Tuple[str, ...] = (
    "cohort study",
    "longitudinal study",
    "prospective cohort",
    "retrospective cohort",
)
CROSS_SECTIONAL_KEYWORDS: Tuple[str, ...] = (
    "cross-sectional",
    "survey study",
    "questionnaire",
)
#: Journals treated as reputable enough to assume a cohort-grade design.
REPUTABLE_JOURNALS: Tuple[str, ...] = (
    "nature",
    "science",
    "lancet",
    "nejm",
    "journal of marketing",
    "journal of consumer research",
    "psychological science",
)

#: Level assigned when nothing else matches.
DEFAULT_LEVEL = EvidenceLevel.CROSS_SECTIONAL


def _contains_any(text: str, needles: Iterable[str]) -> bool:
    return any(needle in text for needle in needles)


def grade_paper(paper: ResearchPaper) -> EvidenceLevel:
    """Infer the evidence level from the title, abstract, and journal."""

    text = f"{paper.title} {paper.abstract or ''}".lower()
    journal = (paper.journal or "").lower()

    if _contains_any(text, META_KEYWORDS):
        # "systematic review" alone is one rung below a meta-analysis
        if "systematic review" in text and "meta-analysis" not in text:
            return EvidenceLevel.SYSTEMATIC_REVIEW
        return EvidenceLevel.META_ANALYSIS

    if _contains_any(text, RCT_KEYWORDS):
        return EvidenceLevel.RCT

    if _contains_any(text, COHORT_KEYWORDS):
        return EvidenceLevel.COHORT

    if _contains_any(text, CROSS_SECTIONAL_KEYWORDS):
        return EvidenceLevel.CROSS_SECTIONAL

    if _contains_any(journal, REPUTABLE_JOURNALS):
        return EvidenceLevel.COHORT

    return DEFAULT_LEVEL


def grade_and_annotate(papers: Sequence[ResearchPaper]) -> List[ResearchPaper]:
    """Grade every paper in place and return them."""

    for paper in papers:
        paper.evidence_level = grade_paper(paper)
    return list(papers)
