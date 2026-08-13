# -*- coding: utf-8 -*-
"""Bidirectional Niche Family Tree validation for THINC v4.2.

THINC™ v4.2 — Invented by Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 Dr. Ehab Taha — Egy-Pioneers Academy.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Mapping


class StrategicDecision(Enum):
    INCOMPLETE = "INCOMPLETE"
    REJECT = "REJECT"
    REPOSITION = "REPOSITION"
    REFINE_OFFER = "REFINE_OFFER"
    ACCEPT_AND_TEST = "ACCEPT_AND_TEST"


class LaunchGate(Enum):
    NO_LAUNCH_BEFORE_MODIFICATION = "NO_LAUNCH_BEFORE_MODIFICATION"
    CONTROLLED_TEST_ALLOWED = "CONTROLLED_TEST_ALLOWED"


class CompletenessStatus(Enum):
    COMPLETE = "COMPLETE"
    INCOMPLETE = "INCOMPLETE"


class FeedbackAction(Enum):
    KEEP = "KEEP"
    REFINE = "REFINE"
    SPLIT = "SPLIT"
    PIVOT = "PIVOT"
    REJECT = "REJECT"


@dataclass(frozen=True)
class CompletenessGate:
    status: CompletenessStatus
    missing_components: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status.value,
            "missing_components": list(self.missing_components),
        }


@dataclass
class NicheValidationReport:
    discovery_path: Dict[str, str]
    reverse_validation_path: Dict[str, str]
    convergence: Dict[str, Any]
    strategic_decision: StrategicDecision
    launch_gate: LaunchGate
    critical_risks: List[str]
    unresolved_evidence: List[str]
    required_actions: List[str]
    feedback_plan: Dict[str, Any]
    completeness_gate: CompletenessGate

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["strategic_decision"] = self.strategic_decision.value
        data["launch_gate"] = self.launch_gate.value
        data["completeness_gate"] = self.completeness_gate.to_dict()
        return data


@dataclass
class NicheFeedbackReport:
    action: FeedbackAction
    parent_niche_decision: FeedbackAction
    confidence_update: str
    reasons: List[str] = field(default_factory=list)
    recommended_next_step: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": self.action.value,
            "parent_niche_decision": self.parent_niche_decision.value,
            "confidence_update": self.confidence_update,
            "reasons": list(self.reasons),
            "recommended_next_step": self.recommended_next_step,
        }


class NicheValidationEngine:
    """Validate the approved top-down and bottom-up THINC niche paths."""

    PATH_LEVELS = (
        "market",
        "niche",
        "micro_niche",
        "persona",
        "problem_jtbd",
        "product",
    )
    REVERSE_LEVELS = tuple(reversed(PATH_LEVELS))
    REQUIRED_INPUTS = (
        "product_solves_problem",
        "persona_matches_problem",
        "offer_strength",
        "economics_viable",
        "critical_risks",
        "unresolved_evidence",
    )

    @staticmethod
    def _clean_path(raw: Any) -> Dict[str, str]:
        if not isinstance(raw, Mapping):
            return {}
        return {str(key): str(value).strip() for key, value in raw.items()}

    @classmethod
    def _missing_components(
        cls,
        payload: Mapping[str, Any],
        discovery: Mapping[str, str],
        reverse: Mapping[str, str],
    ) -> List[str]:
        missing: List[str] = []
        for level in cls.PATH_LEVELS:
            if not discovery.get(level, "").strip():
                missing.append(f"discovery_path.{level}")
        for level in cls.REVERSE_LEVELS:
            if not reverse.get(level, "").strip():
                missing.append(f"reverse_validation_path.{level}")
        for field_name in cls.REQUIRED_INPUTS:
            if field_name not in payload:
                missing.append(field_name)
        return missing

    @classmethod
    def evaluate(
        cls,
        payload: Mapping[str, Any],
        *,
        market_signal_pass: bool,
    ) -> NicheValidationReport:
        if not isinstance(payload, Mapping):
            payload = {}
        discovery = cls._clean_path(payload.get("discovery_path"))
        reverse = cls._clean_path(payload.get("reverse_validation_path"))
        missing = cls._missing_components(payload, discovery, reverse)
        completeness = CompletenessGate(
            status=(
                CompletenessStatus.INCOMPLETE
                if missing
                else CompletenessStatus.COMPLETE
            ),
            missing_components=missing,
        )

        critical_risks = [
            str(item).strip()
            for item in payload.get("critical_risks", [])
            if str(item).strip()
        ] if isinstance(payload.get("critical_risks", []), list) else [str(payload.get("critical_risks"))]
        unresolved = [
            str(item).strip()
            for item in payload.get("unresolved_evidence", [])
            if str(item).strip()
        ] if isinstance(payload.get("unresolved_evidence", []), list) else [str(payload.get("unresolved_evidence"))]

        offer_strength = str(payload.get("offer_strength", "")).strip().lower()
        if not missing and offer_strength not in {"strong", "weak"}:
            raise ValueError("offer_strength must be 'strong' or 'weak'.")

        path_alignment = all(
            discovery.get(level, "").casefold()
            == reverse.get(level, "").casefold()
            for level in cls.PATH_LEVELS
        ) if not missing else False
        product_fit = payload.get("product_solves_problem") is True
        persona_fit = payload.get("persona_matches_problem") is True
        economics_viable = payload.get("economics_viable") is True

        convergence = {
            "aligned": bool(
                path_alignment
                and product_fit
                and persona_fit
                and offer_strength == "strong"
                and economics_viable
                and market_signal_pass
                and not critical_risks
                and not unresolved
            ),
            "path_alignment": path_alignment,
            "specific_customer": persona_fit,
            "evidenced_problem": product_fit,
            "suitable_solution": product_fit,
            "economics_viable": economics_viable,
            "market_signal_pass": bool(market_signal_pass),
        }

        actions: List[str] = []
        if missing:
            decision = StrategicDecision.INCOMPLETE
            actions.extend(f"Provide {item}" for item in missing)
        elif not product_fit:
            decision = StrategicDecision.REJECT
            actions.append("Reject this product/problem pairing and return to the Opportunity Map.")
        elif not persona_fit or not path_alignment:
            decision = StrategicDecision.REPOSITION
            actions.append("Rebuild the target Persona and Micro-Niche from observed problem evidence.")
        elif (
            offer_strength == "weak"
            or not economics_viable
            or critical_risks
            or unresolved
        ):
            decision = StrategicDecision.REFINE_OFFER
            if offer_strength == "weak":
                actions.append("Refine the offer, proof, price, or risk reversal.")
            if not economics_viable:
                actions.append("Rebuild unit economics before any paid launch.")
            actions.extend(f"Resolve critical risk: {item}" for item in critical_risks)
            actions.extend(f"Collect missing evidence: {item}" for item in unresolved)
        elif not market_signal_pass:
            decision = StrategicDecision.REFINE_OFFER
            actions.append("Complete or refresh mandatory market evidence before testing.")
        else:
            decision = StrategicDecision.ACCEPT_AND_TEST
            actions.append("Proceed only to a controlled test; scale remains a separate gate.")

        launch_gate = (
            LaunchGate.CONTROLLED_TEST_ALLOWED
            if decision is StrategicDecision.ACCEPT_AND_TEST
            else LaunchGate.NO_LAUNCH_BEFORE_MODIFICATION
        )
        feedback_plan = {
            "after_controlled_test": [
                "Update Product and Offer confidence from delivered-order economics.",
                "Update Persona and Micro-Niche confidence from qualified buyers and objections.",
                "Escalate to Niche-level rejection only after repeated contrary evidence across multiple micro-niches and solutions.",
            ],
            "allowed_actions_pending_final_label_confirmation": [
                action.value for action in FeedbackAction
            ],
        }

        return NicheValidationReport(
            discovery_path=discovery,
            reverse_validation_path=reverse,
            convergence=convergence,
            strategic_decision=decision,
            launch_gate=launch_gate,
            critical_risks=critical_risks,
            unresolved_evidence=unresolved,
            required_actions=actions,
            feedback_plan=feedback_plan,
            completeness_gate=completeness,
        )


class NicheFeedbackEngine:
    """Update product, micro-niche, and niche hypotheses from real outcomes."""

    @staticmethod
    def evaluate(payload: Mapping[str, Any]) -> NicheFeedbackReport:
        if not isinstance(payload, Mapping):
            raise ValueError("niche feedback must be an object")
        product_outcome = str(payload.get("product_outcome", "")).strip().lower()
        micro_outcome = str(payload.get("micro_niche_outcome", "")).strip().lower()
        evidence_strength = str(payload.get("evidence_strength", "")).strip().lower()
        tested_micro_niches = int(payload.get("tested_micro_niches", 0))
        tested_solutions = int(payload.get("tested_solutions", 0))
        all_failed = payload.get("all_tested_hypotheses_failed") is True

        if product_outcome not in {"passed", "failed", "mixed"}:
            raise ValueError("product_outcome must be passed, failed, or mixed")
        if micro_outcome not in {"passed", "failed", "mixed"}:
            raise ValueError("micro_niche_outcome must be passed, failed, or mixed")
        if evidence_strength not in {"weak", "moderate", "strong"}:
            raise ValueError("evidence_strength must be weak, moderate, or strong")

        if product_outcome == "failed" and micro_outcome == "passed":
            return NicheFeedbackReport(
                action=FeedbackAction.PIVOT,
                parent_niche_decision=FeedbackAction.KEEP,
                confidence_update="Product confidence down; Micro-Niche and Niche preserved.",
                reasons=["The customer/problem opportunity remains but the tested product failed."],
                recommended_next_step="Return to the Opportunity Map and test another product or solution.",
            )

        enough_breadth_to_reject = (
            tested_micro_niches >= 2
            and tested_solutions >= 2
            and evidence_strength == "strong"
            and all_failed
        )
        if micro_outcome == "failed" and enough_breadth_to_reject:
            return NicheFeedbackReport(
                action=FeedbackAction.REJECT,
                parent_niche_decision=FeedbackAction.REJECT,
                confidence_update="Repeated strong contrary evidence reduced parent Niche confidence.",
                reasons=["Multiple Micro-Niches and multiple solutions failed under strong evidence."],
                recommended_next_step="Reject or redefine the parent Niche hypothesis with an audit trail.",
            )

        if micro_outcome == "failed":
            return NicheFeedbackReport(
                action=FeedbackAction.REFINE,
                parent_niche_decision=FeedbackAction.KEEP,
                confidence_update="Micro-Niche confidence down; parent Niche unchanged.",
                reasons=["One Micro-Niche or one solution is insufficient to reject its parent Niche."],
                recommended_next_step="Refine or split the Micro-Niche and test another solution.",
            )

        if product_outcome == "passed" and micro_outcome == "passed":
            return NicheFeedbackReport(
                action=FeedbackAction.KEEP,
                parent_niche_decision=FeedbackAction.KEEP,
                confidence_update="Product, Micro-Niche, and Niche confidence increased.",
                reasons=["Observed outcomes support the current hypothesis."],
                recommended_next_step="Keep the hypothesis and continue controlled validation before scale.",
            )

        return NicheFeedbackReport(
            action=FeedbackAction.SPLIT,
            parent_niche_decision=FeedbackAction.KEEP,
            confidence_update="Mixed evidence; preserve the parent Niche and segment the hypothesis.",
            reasons=["Outcomes are mixed and do not justify a parent-level rejection."],
            recommended_next_step="Split by Persona, Problem/JTBD, or buying context and retest.",
        )

