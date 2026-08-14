# -*- coding: utf-8 -*-
"""Theory registry, paper store, and the Human-in-the-Loop proposal contract.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from thinc_v4 import framework
from thinc_v4.research import (
    EvidenceLevel,
    PapersStore,
    ProposalGenerator,
    ProposalStore,
    ProposalType,
    ResearchStoreError,
    Theory,
    TheoryRegistry,
    TheoryStatus,
    UpdateProposal,
    load_seed_theories,
    resolve_research_dir,
)
from thinc_v4.weights_schema import CANONICAL_WEIGHT_KEYS, WeightsPayloadError

from .conftest import make_paper

FOUNDING_THEORY_IDS = {
    "loss_aversion",
    "anchoring",
    "social_proof",
    "scarcity",
    "peak_end",
    "default_effect",
    "reciprocity",
    "commitment_consistency",
    "cognitive_ease",
    "endowment_effect",
}


class TestSeedData:
    def test_the_ten_founding_theories_ship_with_the_package(self) -> None:
        seed = load_seed_theories()
        assert set(seed) == FOUNDING_THEORY_IDS

    def test_seed_confidences_match_the_curated_values(self) -> None:
        seed = load_seed_theories()
        assert seed["loss_aversion"].confidence_score == 0.95
        assert seed["endowment_effect"].confidence_score == 0.88
        assert seed["cognitive_ease"].confidence_score == 0.72

    def test_every_seed_theory_is_active_and_bilingual(self) -> None:
        for theory in load_seed_theories().values():
            assert theory.status is TheoryStatus.ACTIVE
            assert theory.name_en and theory.name_ar
            assert 0.0 < theory.confidence_score <= 1.0


class TestStorageLocation:
    def test_research_dir_prefers_the_environment_override(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("THINC_RESEARCH_DIR", str(tmp_path / "state"))
        assert resolve_research_dir() == tmp_path / "state"

    def test_explicit_path_wins_over_the_environment(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("THINC_RESEARCH_DIR", str(tmp_path / "env"))
        assert resolve_research_dir(tmp_path / "explicit") == tmp_path / "explicit"

    def test_a_fresh_registry_is_seeded_not_empty(self, tmp_path: Path) -> None:
        registry = TheoryRegistry(tmp_path / "missing.json")
        assert set(registry.theories) == FOUNDING_THEORY_IDS

    def test_unreadable_registry_refuses_to_start_empty(self, tmp_path: Path) -> None:
        path = tmp_path / "theory_registry.json"
        path.write_text("{broken", encoding="utf-8")
        with pytest.raises(ResearchStoreError, match="unreadable"):
            TheoryRegistry(path)

    def test_saving_creates_missing_parent_directories(self, tmp_path: Path) -> None:
        registry = TheoryRegistry(tmp_path / "nested" / "deep" / "registry.json")
        registry.save()
        assert (tmp_path / "nested" / "deep" / "registry.json").exists()


class TestRegistryOperations:
    def test_round_trip_preserves_theories(self, registry: TheoryRegistry) -> None:
        reloaded = TheoryRegistry(registry.path)
        assert set(reloaded.theories) == set(registry.theories)
        assert reloaded.theories["scarcity"].name_ar == registry.theories["scarcity"].name_ar

    def test_deprecating_removes_a_theory_from_active(self, registry: TheoryRegistry) -> None:
        assert registry.deprecate_theory("peak_end", "دُحضت بأدلة أحدث")
        assert registry.get("peak_end") is not None
        assert "peak_end" not in {t.theory_id for t in registry.active()}
        assert "دُحضت" in registry.theories["peak_end"].description_ar

    def test_unknown_field_is_rejected_instead_of_silently_added(
        self, registry: TheoryRegistry
    ) -> None:
        with pytest.raises(ResearchStoreError, match="no field"):
            registry.update_theory("anchoring", confidenc_score=0.9)

    def test_updating_a_missing_theory_reports_failure(self, registry: TheoryRegistry) -> None:
        assert registry.update_theory("does_not_exist", confidence_score=0.9) is False

    def test_link_paper_is_idempotent(self, registry: TheoryRegistry) -> None:
        registry.link_paper("anchoring", "paper-1")
        registry.link_paper("anchoring", "paper-1")
        assert registry.theories["anchoring"].supporting_papers.count("paper-1") == 1

    def test_find_by_keyword_matches_arabic_and_tags(self, registry: TheoryRegistry) -> None:
        assert registry.find_by_keyword("loss aversion") is not None
        assert registry.find_by_keyword("الندرة") is not None

    def test_related_to_finds_theories_mentioned_in_text(self, registry: TheoryRegistry) -> None:
        found = registry.related_to("a field study of social proof in cairo retail")
        assert "social_proof" in {t.theory_id for t in found}


class TestPapersStore:
    def test_duplicate_doi_is_not_stored_twice(self, tmp_path: Path) -> None:
        store = PapersStore(tmp_path / "papers.json")
        first = make_paper("Anchoring in pricing", doi="10.1/abc", citations=5)
        again = make_paper("Anchoring in pricing (v2)", doi="10.1/abc", citations=40)

        assert store.add_or_update(first) is True
        assert store.add_or_update(again) is False
        assert len(store.papers) == 1

    def test_duplicate_refreshes_citations_upward_only(self, tmp_path: Path) -> None:
        store = PapersStore(tmp_path / "papers.json")
        store.add_or_update(make_paper("X", doi="10.1/x", citations=40))
        store.add_or_update(make_paper("X", doi="10.1/x", citations=5))
        assert next(iter(store.papers.values())).cited_by_count == 40

    def test_add_many_returns_only_new_papers(self, tmp_path: Path) -> None:
        store = PapersStore(tmp_path / "papers.json")
        papers = [make_paper("A", doi="10.1/a"), make_paper("B", doi="10.1/b")]
        assert len(store.add_many(papers)) == 2
        assert store.add_many(papers) == []

    def test_round_trip_survives_reload(self, tmp_path: Path) -> None:
        path = tmp_path / "papers.json"
        PapersStore(path).add_or_update(make_paper("Kept", doi="10.1/keep"))
        assert len(PapersStore(path).papers) == 1


class TestProposalGeneration:
    def test_strong_evidence_on_a_known_theory_proposes_a_confidence_step(
        self, generator: ProposalGenerator
    ) -> None:
        paper = make_paper(
            "A meta-analysis of anchoring in consumer pricing",
            level=EvidenceLevel.META_ANALYSIS,
        )
        proposals = generator.analyze_papers([paper])

        assert [p.proposal_type for p in proposals] == [ProposalType.EVIDENCE_UPDATE]
        proposal = proposals[0]
        assert proposal.target == "anchoring"
        assert proposal.current_value == 0.80
        assert proposal.proposed_value == 0.85
        assert proposal.pending, "generation must never apply anything"

    def test_confidence_step_is_capped_at_one(self, generator: ProposalGenerator) -> None:
        paper = make_paper(
            "A meta-analysis of loss aversion in consumer pricing",
            level=EvidenceLevel.META_ANALYSIS,
        )
        proposals = generator.analyze_papers([paper])
        loss = next(p for p in proposals if p.target == "loss_aversion")
        assert loss.current_value == 0.95
        assert loss.proposed_value == 1.0

    def test_tag_overlap_proposes_for_every_related_theory(
        self, generator: ProposalGenerator
    ) -> None:
        """Documented recall behaviour: curated tags link theories to each other.

        "loss aversion" is a tag of the endowment effect, so one strong paper yields a
        proposal per related theory. Each one is still reviewed separately, so the
        breadth costs review time, not accuracy.
        """

        proposals = generator.analyze_papers(
            [
                make_paper(
                    "A meta-analysis of loss aversion in consumer pricing",
                    level=EvidenceLevel.META_ANALYSIS,
                )
            ]
        )
        targets = {p.target for p in proposals}
        assert "loss_aversion" in targets
        assert len(targets) > 1
        assert all(p.pending for p in proposals)

    def test_weak_evidence_generates_nothing(self, generator: ProposalGenerator) -> None:
        paper = make_paper(
            "Notes on loss aversion in consumer pricing",
            level=EvidenceLevel.CROSS_SECTIONAL,
        )
        assert generator.analyze_papers([paper]) == []

    def test_strong_unrelated_paper_proposes_a_new_theory(
        self, generator: ProposalGenerator
    ) -> None:
        paper = make_paper(
            "A meta-analysis of the Decoy Effect in consumer choice",
            level=EvidenceLevel.META_ANALYSIS,
        )
        proposals = generator.analyze_papers([paper])
        assert [p.proposal_type for p in proposals] == [ProposalType.NEW_THEORY]
        assert proposals[0].target == "decoy_effect"
        assert proposals[0].confidence < paper.evidence_weight()

    @pytest.mark.parametrize(
        ("title", "expected_id"),
        [
            ("A meta-analysis of the Decoy Effect in consumer choice", "decoy_effect"),
            ("A systematic review of the Zeigarnik Effect on recall", "zeigarnik_effect"),
            ("Loss Aversion Theory revisited for shoppers", "loss_aversion_theory"),
            ("a lowercase title with no named theory", None),
        ],
    )
    def test_theory_name_extraction_takes_only_the_capitalised_name(
        self, title: str, expected_id: str | None
    ) -> None:
        """Regression: `re.IGNORECASE` made `[A-Z]` match lowercase.

        The ported pattern therefore swallowed the whole sentence and produced ids
        such as `meta_analysis_of_the_decoy_effect`.
        """

        candidate = ProposalGenerator._candidate_theory(make_paper(title))
        assert (candidate or {}).get("theory_id") == expected_id

    def test_generation_records_which_theories_a_paper_touches(
        self, generator: ProposalGenerator
    ) -> None:
        paper = make_paper(
            "A meta-analysis of scarcity and social proof in retail",
            level=EvidenceLevel.META_ANALYSIS,
        )
        generator.analyze_papers([paper])
        assert set(paper.related_theories) >= {"scarcity", "social_proof"}

    def test_proposals_persist_for_a_later_review_session(
        self, generator: ProposalGenerator
    ) -> None:
        generator.analyze_papers(
            [make_paper("A meta-analysis of anchoring in pricing", level=EvidenceLevel.META_ANALYSIS)]
        )
        reloaded = ProposalStore(generator.store.path)
        assert len(reloaded.pending()) == 1


class TestReviewContract:
    def _proposal(self, generator: ProposalGenerator) -> UpdateProposal:
        return generator.analyze_papers(
            [
                make_paper(
                    "A meta-analysis of anchoring in consumer pricing",
                    level=EvidenceLevel.META_ANALYSIS,
                )
            ]
        )[0]

    def test_approval_applies_exactly_the_reviewed_value(
        self, generator: ProposalGenerator
    ) -> None:
        """The 4.2.1 trap: recomputing from the ratio jumped 0.85 straight to 1.0."""

        proposal = self._proposal(generator)
        before = generator.registry.theories["anchoring"].confidence_score
        assert before == 0.80
        assert proposal.proposed_value == 0.85

        assert generator.approve(proposal.proposal_id, "معتمد")

        after = generator.registry.theories["anchoring"].confidence_score
        assert after == 0.85, "approval must apply proposed_value, not net_evidence()"
        assert after != 1.0

    def test_approval_records_the_review(self, generator: ProposalGenerator) -> None:
        proposal = self._proposal(generator)
        generator.approve(proposal.proposal_id, "معتمد بعد المراجعة")
        stored = ProposalStore(generator.store.path).get(proposal.proposal_id)
        assert stored is not None
        assert stored.approved is True
        assert stored.reviewed_at is not None
        assert stored.reviewer_notes == "معتمد بعد المراجعة"

    def test_rejection_changes_nothing_in_the_model(self, generator: ProposalGenerator) -> None:
        proposal = self._proposal(generator)
        before = generator.registry.theories["anchoring"].confidence_score
        assert generator.reject(proposal.proposal_id, "الورقة غير مصرية السياق")
        assert generator.registry.theories["anchoring"].confidence_score == before
        assert generator.pending() == []

    def test_a_proposal_cannot_be_reviewed_twice(self, generator: ProposalGenerator) -> None:
        proposal = self._proposal(generator)
        assert generator.approve(proposal.proposal_id)
        assert generator.approve(proposal.proposal_id) is False
        assert generator.reject(proposal.proposal_id) is False

    def test_unknown_proposal_id_is_refused(self, generator: ProposalGenerator) -> None:
        assert generator.approve("no-such-proposal") is False

    def test_new_theory_approval_adds_it_to_the_registry(
        self, generator: ProposalGenerator
    ) -> None:
        proposal = generator.analyze_papers(
            [
                make_paper(
                    "A meta-analysis of the Decoy Effect in consumer choice",
                    level=EvidenceLevel.META_ANALYSIS,
                )
            ]
        )[0]
        generator.approve(proposal.proposal_id)
        added = generator.registry.get("decoy_effect")
        assert added is not None
        assert added.status is TheoryStatus.ACTIVE

    def test_deprecation_proposal_deactivates_the_theory(
        self, generator: ProposalGenerator
    ) -> None:
        proposal = UpdateProposal(
            proposal_type=ProposalType.DEPRECATE_THEORY,
            target="peak_end",
            proposed_value=None,
            justification="أدلة أحدث تناقضها",
        )
        generator.store.add([proposal])
        generator.approve(proposal.proposal_id)
        assert generator.registry.theories["peak_end"].status is TheoryStatus.DEPRECATED


class TestWeightChangeProposals:
    def _weights_file(self, path: Path) -> Path:
        payload = {"version": "v4.1.0-c1", "weights": dict(framework.DEFAULT_COMPONENT_WEIGHTS)}
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return path

    def test_a_legacy_key_target_is_translated_before_writing(
        self, registry: TheoryRegistry, tmp_path: Path
    ) -> None:
        weights_path = self._weights_file(tmp_path / "weights.json")
        generator = ProposalGenerator(
            registry, ProposalStore(tmp_path / "proposals.json"), weights_path=weights_path
        )
        # legacy short key + a compensating change keeps the vector valid
        proposal = UpdateProposal(
            proposal_type=ProposalType.WEIGHT_CHANGE,
            target="founder",
            current_value=0.15,
            proposed_value=0.15,
            justification="إعادة تأكيد الوزن باسم قديم",
        )
        generator.store.add([proposal])

        assert generator.approve(proposal.proposal_id)

        written = json.loads(weights_path.read_text(encoding="utf-8"))
        assert set(written["weights"]) == set(CANONICAL_WEIGHT_KEYS)
        assert "founder" not in written["weights"]

    def test_a_change_that_breaks_the_sum_is_refused(
        self, registry: TheoryRegistry, tmp_path: Path
    ) -> None:
        weights_path = self._weights_file(tmp_path / "weights.json")
        before = weights_path.read_text(encoding="utf-8")
        generator = ProposalGenerator(
            registry, ProposalStore(tmp_path / "proposals.json"), weights_path=weights_path
        )
        proposal = UpdateProposal(
            proposal_type=ProposalType.WEIGHT_CHANGE,
            target="founder_os",
            current_value=0.15,
            proposed_value=0.90,
            justification="رفع كبير غير متوازن",
        )
        generator.store.add([proposal])

        with pytest.raises(WeightsPayloadError, match="must sum to 1.0"):
            generator.approve(proposal.proposal_id)

        assert weights_path.read_text(encoding="utf-8") == before, "weights must be untouched"
        stored = generator.store.get(proposal.proposal_id)
        assert stored is not None
        assert stored.pending, "a refused proposal stays pending for review"

    def test_unknown_weight_key_is_refused(self, registry: TheoryRegistry, tmp_path: Path) -> None:
        weights_path = self._weights_file(tmp_path / "weights.json")
        generator = ProposalGenerator(
            registry, ProposalStore(tmp_path / "proposals.json"), weights_path=weights_path
        )
        proposal = UpdateProposal(
            proposal_type=ProposalType.WEIGHT_CHANGE,
            target="mystery_component",
            proposed_value=0.2,
            justification="مفتاح غير معروف",
        )
        generator.store.add([proposal])
        with pytest.raises(WeightsPayloadError, match="unknown weight key"):
            generator.approve(proposal.proposal_id)


class TestNoNetwork:
    def test_the_research_modules_import_no_http_client(self) -> None:
        """Phase 2-3 modules must stay pure; ingestion arrives in its own module."""

        from thinc_v4.research import evidence, proposals, registry, semantic_filter

        for module in (evidence, semantic_filter, registry, proposals):
            source_file = module.__file__
            assert source_file is not None
            source = Path(source_file).read_text(encoding="utf-8")
            assert "urllib.request" not in source
            assert "import requests" not in source

    def test_the_seed_data_ships_inside_the_package(self) -> None:
        from thinc_v4.research.registry import THEORIES_SEED_PATH

        assert THEORIES_SEED_PATH.exists()
        assert THEORIES_SEED_PATH.parent.name == "data"
