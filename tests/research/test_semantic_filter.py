# -*- coding: utf-8 -*-
"""Semantic filter — regression guards for the documented contamination failure.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from thinc_v4.research import SemanticFilter

from .conftest import make_paper

#: The exact papers that the unfiltered run wrongly proposed as behavioural evidence.
CONTAMINATED_TITLES = [
    "Explainable AI in Healthcare: a systematic review",
    "Concussion in Sports: long-term outcomes for the athlete",
    "Chronic Coronary Disease management guidelines",
    "Eating Disorders and social media exposure",
]


class TestContaminationRegression:
    @pytest.mark.parametrize("title", CONTAMINATED_TITLES)
    def test_medical_and_sports_papers_are_rejected(self, title: str) -> None:
        verdict = SemanticFilter().evaluate(make_paper(title))
        assert not verdict.accepted, f"{title!r} must never enter the research base"

    def test_a_social_or_loss_mention_alone_is_not_enough(self) -> None:
        """The original bug: any 'social' or 'loss' token was treated as relevant."""

        paper = make_paper(
            "Social determinants of hearing loss in elderly patients",
            abstract="A clinical cohort of patient outcomes.",
        )
        assert not SemanticFilter().evaluate(paper).accepted

    def test_on_topic_behavioural_paper_is_accepted(self) -> None:
        paper = make_paper(
            "Loss aversion and consumer purchase decisions under inflation",
            abstract="A study of shopper willingness to pay.",
        )
        verdict = SemanticFilter().evaluate(paper)
        assert verdict.accepted
        assert verdict.rule == "required_keywords_matched"

    def test_off_topic_without_blacklist_words_is_still_rejected(self) -> None:
        verdict = SemanticFilter().evaluate(make_paper("Soil composition in the Nile delta"))
        assert not verdict.accepted
        assert verdict.rule == "no_required_keyword_matched"


class TestJournalRules:
    def test_whitelisted_journal_is_accepted(self) -> None:
        paper = make_paper("Anything at all", journal="Journal of Consumer Research")
        verdict = SemanticFilter().evaluate(paper)
        assert verdict.accepted
        assert verdict.rule == "whitelist_journal"

    def test_blacklisted_journal_is_rejected(self) -> None:
        paper = make_paper("Consumer choice of treatments", journal="The Lancet")
        verdict = SemanticFilter().evaluate(paper)
        assert not verdict.accepted
        assert verdict.rule in {"blacklist_journal", "blacklist_keyword"}

    def test_journal_whitelist_precedes_keywords_by_default(self) -> None:
        """Documented shipped precedence: a trusted journal short-circuits the scan.

        `frontiers in psychology` is whitelisted and also publishes clinical work, so
        by default a medical paper from it is accepted. This test pins the shipped
        behaviour rather than changing a filtering policy silently.
        """

        paper = make_paper(
            "Depression treatment adherence in patients",
            journal="Frontiers in Psychology",
        )
        assert SemanticFilter().evaluate(paper).accepted

    def test_hard_blacklist_wins_when_explicitly_enabled(self) -> None:
        paper = make_paper(
            "Depression treatment adherence in patients",
            journal="Frontiers in Psychology",
        )
        verdict = SemanticFilter(hard_blacklist_wins=True).evaluate(paper)
        assert not verdict.accepted
        assert verdict.rule == "blacklist_keyword"


class TestFilteringAndLog:
    def test_filter_papers_splits_and_logs_with_reasons(self, tmp_path: Path) -> None:
        log_path = tmp_path / "rejection_log.json"
        filt = SemanticFilter(log_path)
        papers = [
            make_paper("Loss aversion in consumer pricing"),
            make_paper("Concussion in Sports and the athlete brain"),
            make_paper("Soil composition of the Nile delta"),
        ]

        accepted = filt.filter_papers(papers)

        assert [p.title for p in accepted] == ["Loss aversion in consumer pricing"]
        logged = json.loads(log_path.read_text(encoding="utf-8"))
        assert len(logged) == 2
        assert all(entry["reason"] for entry in logged)
        reasons = {entry["reason"].split(":")[0] for entry in logged}
        assert reasons == {"blacklist_keyword", "no_required_keyword_matched"}

    def test_log_is_appended_across_runs(self, tmp_path: Path) -> None:
        log_path = tmp_path / "rejection_log.json"
        rejected = [make_paper("Olympic athlete performance")]
        SemanticFilter(log_path).filter_papers(rejected)
        SemanticFilter(log_path).filter_papers(rejected)
        assert len(json.loads(log_path.read_text(encoding="utf-8"))) == 2

    def test_no_path_means_no_file_is_written(self, tmp_path: Path) -> None:
        filt = SemanticFilter()
        filt.filter_papers([make_paper("Olympic athlete performance")])
        assert filt.stats()["total_rejections"] == 1
        assert list(tmp_path.iterdir()) == []

    def test_stats_group_by_rule(self, tmp_path: Path) -> None:
        filt = SemanticFilter(tmp_path / "log.json")
        filt.filter_papers(
            [
                make_paper("Cancer therapy adherence"),
                make_paper("Soil composition"),
                make_paper("Olympic athlete diets"),
            ]
        )
        stats = filt.stats()
        assert stats["total_rejections"] == 3
        assert stats["by_reason"]["blacklist_keyword"] == 2
        assert stats["by_reason"]["no_required_keyword_matched"] == 1

    def test_corrupt_log_does_not_break_filtering(self, tmp_path: Path) -> None:
        log_path = tmp_path / "log.json"
        log_path.write_text("{not json", encoding="utf-8")
        filt = SemanticFilter(log_path)
        assert filt.rejection_log == []
        assert filt.evaluate(make_paper("Consumer choice")).accepted
