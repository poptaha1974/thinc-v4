# -*- coding: utf-8 -*-
"""Ingestion and the supervised update cycle — entirely offline.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

Every fetch goes through an injected double. If any test here ever needs the
network, that is a design regression, not a flaky test.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import pytest

from thinc_v4.research import (
    AutoUpdater,
    EvidenceLevel,
    PapersStore,
    ProposalGenerator,
    ProposalStore,
    ResearchIngestor,
    SemanticFilter,
    TheoryRegistry,
)
from thinc_v4.research.auto_updater import FALLBACK_QUERIES, QUERY_CONTEXTS

OPENALEX_RESPONSE: Dict[str, Any] = {
    "results": [
        {
            "id": "https://openalex.org/W1",
            "title": "A meta-analysis of anchoring in consumer pricing",
            "publication_year": 2025,
            "cited_by_count": 120,
            "doi": "https://doi.org/10.1/anchor",
            "abstract_inverted_index": {"Anchoring": [0], "shifts": [1], "purchase": [2]},
            "authorships": [{"author": {"display_name": "A. Researcher"}}, {"author": {}}],
            "primary_location": {"source": {"display_name": "Journal of Marketing"}},
            "concepts": [{"display_name": "Anchoring"}, {"other": "ignored"}],
        }
    ]
}

SEMANTIC_SCHOLAR_RESPONSE: Dict[str, Any] = {
    "data": [
        {
            "paperId": "SS1",
            "title": "Scarcity cues and consumer choice",
            "year": 2024,
            "citationCount": 30,
            "venue": "Marketing Science",
            "authors": [{"name": "B. Scholar"}, {}],
            "abstract": "A field study of shopper scarcity perception.",
            "externalIds": {"DOI": "10.2/scarcity"},
        }
    ]
}


class RecordingFetcher:
    """Test double: serves canned payloads and records the URLs requested."""

    def __init__(self, payloads: Dict[str, Dict[str, Any] | None] | None = None) -> None:
        self.payloads = payloads or {}
        self.urls: List[str] = []

    def __call__(self, url: str, *, timeout: float = 30.0) -> Dict[str, Any] | None:
        self.urls.append(url)
        for marker, payload in self.payloads.items():
            if marker in url:
                return payload
        return None


class TestIngestion:
    def test_openalex_record_maps_to_a_paper(self) -> None:
        ingestor = ResearchIngestor(RecordingFetcher({"openalex": OPENALEX_RESPONSE}))
        outcome = ingestor.search_openalex("anchoring")

        assert not outcome.failed
        paper = outcome.papers[0]
        assert paper.source == "openalex"
        assert paper.title.startswith("A meta-analysis of anchoring")
        assert paper.publication_year == 2025
        assert paper.cited_by_count == 120
        assert paper.journal == "Journal of Marketing"
        assert paper.authors == ["A. Researcher"], "authors without a name are skipped"
        assert paper.keywords == ["Anchoring"]

    def test_inverted_abstract_is_rebuilt_in_order(self) -> None:
        ingestor = ResearchIngestor(RecordingFetcher({"openalex": OPENALEX_RESPONSE}))
        paper = ingestor.search_openalex("anchoring").papers[0]
        assert paper.abstract == "Anchoring shifts purchase"

    def test_semantic_scholar_record_maps_to_a_paper(self) -> None:
        ingestor = ResearchIngestor(RecordingFetcher({"semanticscholar": SEMANTIC_SCHOLAR_RESPONSE}))
        outcome = ingestor.search_semantic_scholar("scarcity")

        paper = outcome.papers[0]
        assert paper.source == "semantic_scholar"
        assert paper.doi == "10.2/scarcity"
        assert paper.url is not None and paper.url.endswith("SS1")

    def test_a_failed_request_is_reported_not_silently_empty(self) -> None:
        outcome = ResearchIngestor(RecordingFetcher()).search_openalex("anything")
        assert outcome.papers == []
        assert outcome.failed
        assert outcome.detail

    def test_query_is_quoted_into_the_url(self) -> None:
        fetcher = RecordingFetcher({"openalex": OPENALEX_RESPONSE})
        ResearchIngestor(fetcher).search_openalex('"Loss Aversion" consumer behavior')
        assert "%22Loss+Aversion%22" in fetcher.urls[0]

    def test_openalex_filters_are_present(self) -> None:
        url = ResearchIngestor(RecordingFetcher()).openalex_url(
            "x", from_year=2023, min_citations=5, max_results=7
        )
        assert "from_publication_date:2023-01-01" in url
        assert "is_oa:true" in url
        assert "cited_by_count:%3E5" in url or "cited_by_count:>5" in url
        assert "per-page=7" in url

    def test_cache_avoids_a_second_request(self, tmp_path: Path) -> None:
        fetcher = RecordingFetcher({"openalex": OPENALEX_RESPONSE})
        ingestor = ResearchIngestor(fetcher, cache_dir=tmp_path / "cache")
        ingestor.search_openalex("anchoring")
        ingestor.search_openalex("anchoring")
        assert len(fetcher.urls) == 1

    def test_no_cache_dir_means_no_files_written(self, tmp_path: Path) -> None:
        fetcher = RecordingFetcher({"openalex": OPENALEX_RESPONSE})
        ResearchIngestor(fetcher).search_openalex("anchoring")
        assert list(tmp_path.iterdir()) == []

    def test_corrupt_cache_entry_falls_back_to_fetching(self, tmp_path: Path) -> None:
        cache = tmp_path / "cache"
        cache.mkdir()
        fetcher = RecordingFetcher({"openalex": OPENALEX_RESPONSE})
        ingestor = ResearchIngestor(fetcher, cache_dir=cache)
        url = ingestor.openalex_url("anchoring", from_year=2023)
        cache_path = ingestor._cache_path("openalex", url)
        assert cache_path is not None
        cache_path.write_text("{broken", encoding="utf-8")

        outcome = ingestor.search_openalex("anchoring", from_year=2023)
        assert outcome.papers, "a broken cache entry must not look like an empty result"


class TestUpdateCycle:
    def _updater(self, tmp_path: Path, fetcher: RecordingFetcher) -> AutoUpdater:
        registry = TheoryRegistry(tmp_path / "theory_registry.json")
        registry.save()
        return AutoUpdater(
            tmp_path,
            registry=registry,
            papers=PapersStore(tmp_path / "papers.json"),
            generator=ProposalGenerator(
                registry, ProposalStore(tmp_path / "proposals.json"), tmp_path / "weights.json"
            ),
            semantic_filter=SemanticFilter(tmp_path / "rejection_log.json"),
            ingestor=ResearchIngestor(fetcher),
            request_spacing=0.0,
        )

    def test_queries_quote_each_active_theory_name(self, tmp_path: Path) -> None:
        updater = self._updater(tmp_path, RecordingFetcher())
        queries = updater.build_queries()
        assert '"Loss Aversion" consumer behavior' in queries
        assert all(query.startswith('"') for query in queries)
        assert len(queries) <= 35

    def test_empty_registry_uses_the_fallback_queries(self, tmp_path: Path) -> None:
        registry = TheoryRegistry(tmp_path / "empty.json", seed_if_missing=False)
        updater = AutoUpdater(
            tmp_path,
            registry=registry,
            papers=PapersStore(tmp_path / "papers.json"),
            ingestor=ResearchIngestor(RecordingFetcher()),
            request_spacing=0.0,
        )
        assert updater.build_queries() == list(FALLBACK_QUERIES)

    def test_context_suffixes_are_applied(self, tmp_path: Path) -> None:
        updater = self._updater(tmp_path, RecordingFetcher())
        first_theory_queries = [q for q in updater.build_queries() if "Loss Aversion" in q]
        assert len(first_theory_queries) == len(QUERY_CONTEXTS)

    def test_full_cycle_produces_pending_proposals_only(self, tmp_path: Path) -> None:
        fetcher = RecordingFetcher({"openalex": OPENALEX_RESPONSE})
        updater = self._updater(tmp_path, fetcher)
        before = updater.registry.theories["anchoring"].confidence_score

        run = updater.run_cycle("manual", max_queries=2)

        assert run.status == "completed"
        assert run.papers_fetched >= 1
        assert run.papers_new == 1, "the same paper must be deduplicated across queries"
        assert run.proposals_generated >= 1
        assert all(p.pending for p in updater.pending())
        assert updater.registry.theories["anchoring"].confidence_score == before, (
            "a cycle must never change the model on its own"
        )

    def test_cycle_records_filtered_out_papers(self, tmp_path: Path) -> None:
        contaminated = {
            "results": [
                {
                    "id": "https://openalex.org/W9",
                    "title": "Concussion in Sports and the athlete brain",
                    "publication_year": 2025,
                    "cited_by_count": 80,
                }
            ]
        }
        updater = self._updater(tmp_path, RecordingFetcher({"openalex": contaminated}))
        run = updater.run_cycle("manual", max_queries=1)

        assert run.papers_fetched == 1
        assert run.papers_filtered_out == 1
        assert run.papers_new == 0
        assert run.proposals_generated == 0

    def test_failed_source_is_recorded_in_the_run(self, tmp_path: Path) -> None:
        updater = self._updater(tmp_path, RecordingFetcher())
        run = updater.run_cycle("cron", max_queries=2)
        assert run.queries_failed, "a dead source must not look like 'no results'"
        assert run.papers_fetched == 0

    def test_semantic_scholar_is_only_a_fallback_for_thin_results(self, tmp_path: Path) -> None:
        fetcher = RecordingFetcher(
            {"openalex": OPENALEX_RESPONSE, "semanticscholar": SEMANTIC_SCHOLAR_RESPONSE}
        )
        updater = self._updater(tmp_path, fetcher)
        updater.run_cycle("manual", max_queries=1)
        # OpenAlex returned a single paper (< 3), so the fallback is consulted
        assert any("semanticscholar" in url for url in fetcher.urls)

    def test_run_history_is_appended(self, tmp_path: Path) -> None:
        updater = self._updater(tmp_path, RecordingFetcher({"openalex": OPENALEX_RESPONSE}))
        updater.run_cycle("manual", max_queries=1)
        updater.run_cycle("cron", max_queries=1)
        history = json.loads((tmp_path / AutoUpdater.RUNS_FILENAME).read_text(encoding="utf-8"))
        assert len(history) == 2
        assert [entry["triggered_by"] for entry in history] == ["manual", "cron"]

    def test_an_empty_cycle_still_materializes_the_registry(self, tmp_path: Path) -> None:
        """A run that fetched nothing must be distinguishable from a run that never happened."""

        updater = self._updater(tmp_path, RecordingFetcher())  # every query fails
        run = updater.run_cycle("cron", max_queries=1)

        assert run.papers_fetched == 0
        assert (tmp_path / TheoryRegistry.FILENAME).exists(), (
            "the scheduled job reads this file to prove the cycle changed no confidence"
        )

    def test_a_cron_cycle_leaves_every_confidence_untouched(self, tmp_path: Path) -> None:
        """The invariant the monthly workflow asserts."""

        from thinc_v4.research import load_seed_theories

        updater = self._updater(tmp_path, RecordingFetcher({"openalex": OPENALEX_RESPONSE}))
        updater.run_cycle("cron", max_queries=2)

        seed = load_seed_theories()
        for theory_id, theory in seed.items():
            assert updater.registry.theories[theory_id].confidence_score == theory.confidence_score

    def test_stats_summarize_the_state(self, tmp_path: Path) -> None:
        updater = self._updater(tmp_path, RecordingFetcher({"openalex": OPENALEX_RESPONSE}))
        updater.run_cycle("manual", max_queries=1)
        stats = updater.stats()
        assert stats["theories_active"] == 10
        assert stats["papers_stored"] == 1
        assert stats["proposals_pending"] >= 1

    def test_approval_after_a_cycle_applies_the_reviewed_value(self, tmp_path: Path) -> None:
        updater = self._updater(tmp_path, RecordingFetcher({"openalex": OPENALEX_RESPONSE}))
        updater.run_cycle("manual", max_queries=1)
        proposal = next(p for p in updater.pending() if p.target == "anchoring")

        assert updater.approve(proposal.proposal_id, "معتمد")

        assert updater.registry.theories["anchoring"].confidence_score == proposal.proposed_value
        assert updater.registry.theories["anchoring"].confidence_score < 1.0

    def test_graded_level_is_stored_with_the_paper(self, tmp_path: Path) -> None:
        updater = self._updater(tmp_path, RecordingFetcher({"openalex": OPENALEX_RESPONSE}))
        updater.run_cycle("manual", max_queries=1)
        stored = next(iter(updater.papers.papers.values()))
        assert stored.evidence_level is EvidenceLevel.META_ANALYSIS


class TestCli:
    def test_stats_command_runs_without_network(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        from thinc_v4.research.auto_updater import main

        main(["stats", "--dir", str(tmp_path)])
        out = capsys.readouterr().out
        assert "theories_active: 10" in out

    def test_pending_command_reports_an_empty_queue(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        from thinc_v4.research.auto_updater import main

        main(["pending", "--dir", str(tmp_path)])
        assert "لا اقتراحات معلّقة" in capsys.readouterr().out

    def test_approve_requires_an_id(self, tmp_path: Path) -> None:
        from thinc_v4.research.auto_updater import main

        with pytest.raises(SystemExit):
            main(["approve", "--dir", str(tmp_path)])
