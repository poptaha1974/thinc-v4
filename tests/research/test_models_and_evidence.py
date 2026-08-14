# -*- coding: utf-8 -*-
"""Models and evidence grading — the numbers are pinned, not re-derived.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
"""
from __future__ import annotations

import pytest

from thinc_v4.research import (
    EVIDENCE_WEIGHTS,
    EvidenceLevel,
    Theory,
    grade_and_annotate,
    grade_paper,
    utc_now,
)

from .conftest import make_paper


class TestEvidenceWeights:
    def test_hierarchy_is_monotonic_from_meta_analysis_down(self) -> None:
        order = [
            EvidenceLevel.META_ANALYSIS,
            EvidenceLevel.SYSTEMATIC_REVIEW,
            EvidenceLevel.RCT,
            EvidenceLevel.COHORT,
            EvidenceLevel.CASE_CONTROL,
            EvidenceLevel.CROSS_SECTIONAL,
            EvidenceLevel.CASE_REPORT,
            EvidenceLevel.EXPERT_OPINION,
        ]
        weights = [EVIDENCE_WEIGHTS[level] for level in order]
        assert weights == sorted(weights, reverse=True)
        assert weights[0] == 1.00
        assert weights[-1] == 0.10

    def test_evidence_weight_is_pinned_for_a_known_paper(self) -> None:
        paper = make_paper(
            "Loss aversion in retail pricing",
            year=2025,
            citations=100,
            level=EvidenceLevel.META_ANALYSIS,
        )
        # base 1.0 capped at 1.0, citation boost log10(100)/10 = 0.2 → min(1.0, 1.2)=1.0
        # recency for a one-year-old paper = 0.9
        assert paper.evidence_weight(now_year=2026) == 0.9

    def test_recency_floor_protects_old_but_strong_papers(self) -> None:
        paper = make_paper("Anchoring", year=2000, citations=0, level=EvidenceLevel.RCT)
        assert paper.evidence_weight(now_year=2026) == pytest.approx(0.8 * 0.5, abs=1e-3)

    def test_evidence_weight_does_not_depend_on_the_calendar(self) -> None:
        """The 4.2.1 CI break came from time-coupled assertions; keep this pinnable."""

        paper = make_paper("Scarcity", year=2024, level=EvidenceLevel.RCT)
        assert paper.evidence_weight(now_year=2025) > paper.evidence_weight(now_year=2030)


class TestGrading:
    @pytest.mark.parametrize(
        ("title", "expected"),
        [
            ("A meta-analysis of scarcity appeals", EvidenceLevel.META_ANALYSIS),
            ("A systematic review of nudging", EvidenceLevel.SYSTEMATIC_REVIEW),
            ("A randomised controlled trial of price framing", EvidenceLevel.RCT),
            ("A prospective cohort study of shoppers", EvidenceLevel.COHORT),
            ("A cross-sectional survey of buyers", EvidenceLevel.CROSS_SECTIONAL),
            ("Notes on consumer choice", EvidenceLevel.CROSS_SECTIONAL),
        ],
    )
    def test_titles_map_to_levels(self, title: str, expected: EvidenceLevel) -> None:
        assert grade_paper(make_paper(title)) is expected

    def test_meta_analysis_outranks_a_bare_systematic_review_mention(self) -> None:
        paper = make_paper("A systematic review and meta-analysis of default effects")
        assert grade_paper(paper) is EvidenceLevel.META_ANALYSIS

    def test_reputable_journal_lifts_an_otherwise_unclassified_paper(self) -> None:
        paper = make_paper("Brand trust and repurchase", journal="Journal of Marketing")
        assert grade_paper(paper) is EvidenceLevel.COHORT

    def test_grade_and_annotate_writes_the_level_back(self) -> None:
        papers = [make_paper("A meta-analysis of reciprocity"), make_paper("Retail notes")]
        graded = grade_and_annotate(papers)
        assert [p.evidence_level for p in graded] == [
            EvidenceLevel.META_ANALYSIS,
            EvidenceLevel.CROSS_SECTIONAL,
        ]


class TestTheory:
    def test_net_evidence_is_neutral_without_linked_papers(self) -> None:
        assert Theory(theory_id="t", name_en="T", name_ar="ت", category="x").net_evidence() == 0.5

    def test_net_evidence_is_the_supporting_share(self) -> None:
        theory = Theory(
            theory_id="t",
            name_en="T",
            name_ar="ت",
            category="x",
            supporting_papers=["a", "b", "c"],
            contradicting_papers=["d"],
        )
        assert theory.net_evidence() == 0.75

    def test_matching_uses_the_english_name_and_tags(self) -> None:
        theory = Theory(
            theory_id="loss_aversion",
            name_en="Loss Aversion",
            name_ar="الخوف من الخسارة",
            category="behavioral_economics",
            tags=["prospect theory"],
        )
        assert theory.matches("a study of loss aversion in cairo")
        assert theory.matches("applying prospect theory to pricing")
        assert not theory.matches("a study of brand recall")

    def test_stored_timestamps_are_timezone_aware(self) -> None:
        assert utc_now().tzinfo is not None
        theory = Theory(theory_id="t", name_en="T", name_ar="ت", category="x")
        assert theory.added_at.tzinfo is not None


class TestPaperIdentity:
    def test_doi_wins_over_external_id_for_dedupe(self) -> None:
        paper = make_paper("X", doi="10.1/ABC", external_id="openalex:W1")
        assert paper.dedupe_key() == "10.1/abc"

    def test_searchable_text_includes_keywords(self) -> None:
        paper = make_paper("Title", abstract="Abstract", keywords=["Nudge"])
        assert "nudge" in paper.searchable_text()
