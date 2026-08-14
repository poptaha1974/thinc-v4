# -*- coding: utf-8 -*-
"""Update proposals: generation, review, and application.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

**Human-in-the-Loop is the contract of this module.** Generating a proposal never
changes the model. A proposal takes effect only through `approve()`, which records
the reviewer and then applies exactly what was reviewed.

Two documented traps are preserved as behaviour and pinned by tests:

1. Approving an `evidence_update` applies `proposed_value` directly. Recomputing
   confidence from the supporting/contradicting ratio would jump to 1.0 whenever no
   contradicting paper exists — which is how a 0.85 confidence once became 1.0 in a
   single step.
2. A `weight_change` is applied through the canonical weights schema, so a proposal
   naming a legacy short key cannot silently write an unrecognised key into
   `weights.json`.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from ..weights_schema import canonical_key, normalize_payload, validate_weights
from .models import (
    NEW_THEORY_EVIDENCE,
    STRONG_EVIDENCE,
    ProposalType,
    ResearchPaper,
    Theory,
    TheoryStatus,
    UpdateProposal,
    utc_now,
)
from .registry import ResearchStoreError, TheoryRegistry, _write_json, resolve_research_dir

#: Confidence increment proposed when strong evidence supports an existing theory.
CONFIDENCE_STEP = 0.05
#: A brand-new theory starts at a discounted share of the paper's evidence weight.
NEW_THEORY_DISCOUNT = 0.7
#: Pattern used to guess a theory name from a paper title.
#:
#: The ported version passed `re.IGNORECASE`, which makes `[A-Z]` match lowercase
#: too, so the "capitalised words" intent was lost and the match ran backwards over
#: the sentence: "A meta-analysis of the Decoy Effect" produced the theory id
#: `meta_analysis_of_the_decoy_effect`. Capitalisation is now required (that is the
#: actual signal for a named theory) and at most three words are taken, while the
#: trailing noun still matches in either case.
THEORY_NAME_PATTERN = re.compile(
    r"\b([A-Z][a-z]+(?:[-\s][A-Z][a-z]+){0,2})\s+"
    r"([Tt]heory|[Ee]ffect|[Bb]ias|[Hh]euristic|[Pp]rinciple|[Hh]ypothesis)\b"
)


class ProposalStore:
    """Persisted list of proposals with their review state."""

    FILENAME = "proposals.json"

    def __init__(self, path: Path | None = None) -> None:
        self.path = path if path is not None else resolve_research_dir() / self.FILENAME
        self.proposals: List[UpdateProposal] = self._load()

    def _load(self) -> List[UpdateProposal]:
        if not self.path.exists():
            return []
        try:
            with self.path.open(encoding="utf-8") as handle:
                payload = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            raise ResearchStoreError(f"Proposal store at {self.path} is unreadable: {exc}") from exc
        if not isinstance(payload, list):
            raise ResearchStoreError(f"Proposal store at {self.path} must contain a list")
        return [UpdateProposal(**entry) for entry in payload]

    def save(self) -> None:
        _write_json(self.path, [p.model_dump(mode="json") for p in self.proposals])

    def add(self, proposals: Sequence[UpdateProposal]) -> None:
        self.proposals.extend(proposals)
        self.save()

    def pending(self) -> List[UpdateProposal]:
        return [p for p in self.proposals if p.pending]

    def get(self, proposal_id: str) -> UpdateProposal | None:
        return next((p for p in self.proposals if p.proposal_id == proposal_id), None)


class ProposalGenerator:
    """Turns graded papers into reviewable proposals, and applies approved ones."""

    def __init__(
        self,
        registry: TheoryRegistry,
        store: ProposalStore | None = None,
        weights_path: Path | None = None,
    ) -> None:
        self.registry = registry
        self.store = store if store is not None else ProposalStore()
        self.weights_path = weights_path

    # ── generation ────────────────────────────────────────────────────────────

    def analyze_papers(self, papers: Sequence[ResearchPaper]) -> List[UpdateProposal]:
        """Propose updates from `papers`. Nothing is applied here."""

        generated: List[UpdateProposal] = []

        for paper in papers:
            related = self.registry.related_to(paper.searchable_text())
            paper.related_theories = [theory.theory_id for theory in related]

            if related and paper.evidence_level in STRONG_EVIDENCE:
                generated.extend(self._confidence_proposals(paper, related))
            elif not related and paper.evidence_level in NEW_THEORY_EVIDENCE:
                candidate = self._candidate_theory(paper)
                if candidate is not None:
                    generated.append(self._new_theory_proposal(paper, candidate))

        self.store.add(generated)
        return generated

    def _confidence_proposals(
        self, paper: ResearchPaper, related: Sequence[Theory]
    ) -> List[UpdateProposal]:
        proposals: List[UpdateProposal] = []
        for theory in related:
            proposals.append(
                UpdateProposal(
                    proposal_type=ProposalType.EVIDENCE_UPDATE,
                    target=theory.theory_id,
                    current_value=theory.confidence_score,
                    proposed_value=min(1.0, round(theory.confidence_score + CONFIDENCE_STEP, 3)),
                    justification=(
                        f"ورقة {paper.evidence_level.value} من {paper.publication_year} "
                        f"باستشهادات {paper.cited_by_count} تدعم نظرية '{theory.name_ar}'. "
                        f"عنوان الورقة: {paper.title[:150]}"
                    ),
                    supporting_paper_ids=[paper.paper_id],
                    confidence=paper.evidence_weight(),
                )
            )
        return proposals

    def _new_theory_proposal(
        self, paper: ResearchPaper, candidate: Dict[str, str]
    ) -> UpdateProposal:
        return UpdateProposal(
            proposal_type=ProposalType.NEW_THEORY,
            target=candidate["theory_id"],
            current_value=None,
            proposed_value=candidate,
            justification=(
                f"مصدر قوي ({paper.evidence_level.value}) يقترح نظرية غير موجودة في السجل. "
                f"العنوان: {paper.title[:150]}"
            ),
            supporting_paper_ids=[paper.paper_id],
            confidence=round(paper.evidence_weight() * NEW_THEORY_DISCOUNT, 3),
        )

    @staticmethod
    def _candidate_theory(paper: ResearchPaper) -> Dict[str, str] | None:
        """Guess a theory name from the title. Heuristic; the human decides."""

        match = THEORY_NAME_PATTERN.search(paper.title or "")
        if match is None:
            return None
        name = match.group(0)
        theory_id = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")[:60]
        if not theory_id:
            return None
        return {
            "theory_id": theory_id,
            "name_en": name.title(),
            "name_ar": f"{name.title()} (يحتاج ترجمة)",
            "category": "behavioral_economics",
        }

    # ── review ────────────────────────────────────────────────────────────────

    def pending(self) -> List[UpdateProposal]:
        return self.store.pending()

    def approve(self, proposal_id: str, notes: str = "") -> bool:
        """Approve and apply a pending proposal."""

        proposal = self.store.get(proposal_id)
        if proposal is None or not proposal.pending:
            return False
        self._apply(proposal)
        proposal.approved = True
        proposal.reviewed_at = utc_now()
        proposal.reviewer_notes = notes
        self.store.save()
        return True

    def reject(self, proposal_id: str, notes: str = "") -> bool:
        proposal = self.store.get(proposal_id)
        if proposal is None or not proposal.pending:
            return False
        proposal.approved = False
        proposal.reviewed_at = utc_now()
        proposal.reviewer_notes = notes
        self.store.save()
        return True

    # ── application ───────────────────────────────────────────────────────────

    def _apply(self, proposal: UpdateProposal) -> None:
        if proposal.proposal_type is ProposalType.NEW_THEORY:
            self._apply_new_theory(proposal)
        elif proposal.proposal_type is ProposalType.EVIDENCE_UPDATE:
            self._apply_evidence_update(proposal)
        elif proposal.proposal_type is ProposalType.DEPRECATE_THEORY:
            self.registry.deprecate_theory(proposal.target, proposal.justification)
        elif proposal.proposal_type is ProposalType.WEIGHT_CHANGE:
            self._apply_weight_change(proposal)

    def _apply_new_theory(self, proposal: UpdateProposal) -> None:
        data = proposal.proposed_value
        if not isinstance(data, dict) or "theory_id" not in data:
            raise ResearchStoreError(
                f"Proposal {proposal.proposal_id} carries no usable theory definition"
            )
        self.registry.add_theory(
            Theory(
                theory_id=str(data["theory_id"]),
                name_en=str(data.get("name_en", data["theory_id"])),
                name_ar=str(data.get("name_ar", data["theory_id"])),
                category=str(data.get("category", "behavioral_economics")),
                status=TheoryStatus.ACTIVE,
                supporting_papers=list(proposal.supporting_paper_ids),
                confidence_score=proposal.confidence,
                description_ar=proposal.justification[:500],
            )
        )

    def _apply_evidence_update(self, proposal: UpdateProposal) -> None:
        theory = self.registry.get(proposal.target)
        if theory is None:
            raise ResearchStoreError(f"Unknown theory {proposal.target!r}")
        try:
            reviewed = float(proposal.proposed_value)
        except (TypeError, ValueError) as exc:
            raise ResearchStoreError(
                f"Proposal {proposal.proposal_id} has a non-numeric confidence"
            ) from exc
        # Apply exactly the reviewed value; recomputing from the ratio would jump
        # to 1.0 whenever there is no contradicting paper.
        theory.confidence_score = min(1.0, max(0.0, reviewed))
        for paper_id in proposal.supporting_paper_ids:
            if paper_id not in theory.supporting_papers:
                theory.supporting_papers.append(paper_id)
        theory.last_updated = utc_now()
        self.registry.save()

    def _apply_weight_change(self, proposal: UpdateProposal) -> None:
        from ..calibration import load_weights, save_weights

        payload: Dict[str, Any] = load_weights(self.weights_path)
        key = canonical_key(proposal.target)
        try:
            value = float(proposal.proposed_value)
        except (TypeError, ValueError) as exc:
            raise ResearchStoreError(
                f"Proposal {proposal.proposal_id} has a non-numeric weight"
            ) from exc
        weights = dict(payload["weights"])
        weights[key] = value
        # A single changed weight must still leave a valid vector; refuse otherwise
        # instead of persisting a file that silently falls back on load.
        validate_weights(weights)
        payload["weights"] = weights
        payload["previous_version"] = payload.get("version", "unversioned")
        payload["version"] = f"{payload.get('version', 'unversioned')}+proposal-{proposal.proposal_id[:8]}"
        normalized, _ = normalize_payload(payload)
        save_weights(normalized, self.weights_path)
