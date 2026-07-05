# -*- coding: utf-8 -*-
"""Adaptive Market Learning Engine for THINC v4.0.

This module turns THINC from a fixed decision-support model into a learning
operating system that updates its assumptions when the market changes.

It learns from:
- campaign prediction vs actual results,
- Meta performance drift,
- WhatsApp objections,
- customer behavior shifts,
- competitor response,
- supplier reliability,
- profit leakage,
- creative fatigue,
- post-purchase experience,
- and brand/ethics guardrails.

Important caution:
    This engine does not automatically rewrite strategy without human review.
    It produces structured learning signals, hypothesis updates, and recommended
    experiments. A human operator should approve major rule changes.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List


class MarketSignalType(Enum):
    CAMPAIGN_RESULT = "campaign_result"
    WHATSAPP_OBJECTION = "whatsapp_objection"
    COMPETITOR_MOVE = "competitor_move"
    SUPPLIER_EVENT = "supplier_event"
    CREATIVE_FATIGUE = "creative_fatigue"
    PROFIT_LEAKAGE = "profit_leakage"
    POST_PURCHASE_FEEDBACK = "post_purchase_feedback"
    BRAND_DRIFT = "brand_drift"
    ETHICS_RISK = "ethics_risk"
    CULTURAL_SHIFT = "cultural_shift"


class LearningSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class LearningAction(Enum):
    KEEP_RULE = "keep_rule"
    WATCH = "watch"
    RUN_EXPERIMENT = "run_experiment"
    UPDATE_WEIGHT = "update_weight"
    UPDATE_RULE = "update_rule"
    ESCALATE_HUMAN_REVIEW = "escalate_human_review"
    PAUSE_SCALING = "pause_scaling"


class HumanBehaviorShift(Enum):
    PRICE_SENSITIVITY_UP = "price_sensitivity_up"
    TRUST_DEMAND_UP = "trust_demand_up"
    DELIVERY_URGENCY_UP = "delivery_urgency_up"
    SOCIAL_PROOF_DEMAND_UP = "social_proof_demand_up"
    NOVELTY_FATIGUE = "novelty_fatigue"
    VALUE_SEEKING_UP = "value_seeking_up"
    STATUS_SIGNALING_UP = "status_signaling_up"
    CHANNEL_MIGRATION = "channel_migration"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class PredictionSnapshot:
    expected_score: float
    expected_real_cpa: float | None = None
    expected_conversion_rate: float | None = None
    expected_delivery_rate: float | None = None
    expected_net_profit: float | None = None
    expected_objections: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class ActualOutcomeSnapshot:
    actual_score: float | None = None
    actual_real_cpa: float | None = None
    actual_conversion_rate: float | None = None
    actual_delivery_rate: float | None = None
    actual_net_profit: float | None = None
    observed_objections: List[str] = field(default_factory=list)
    comments_sentiment: str | None = None
    repeat_purchase_rate: float | None = None
    refund_or_return_rate: float | None = None


@dataclass(frozen=True)
class MarketSignal:
    signal_type: MarketSignalType
    description: str
    evidence: str
    severity: LearningSeverity = LearningSeverity.MEDIUM
    affected_layer: str = "general"
    suggested_shift: HumanBehaviorShift = HumanBehaviorShift.UNKNOWN


@dataclass(frozen=True)
class LearningInput:
    context_name: str
    prediction: PredictionSnapshot
    actual: ActualOutcomeSnapshot
    signals: List[MarketSignal] = field(default_factory=list)
    current_weights: Dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class LearningOutput:
    learning_score: float
    severity: LearningSeverity
    action: LearningAction
    prediction_gap_summary: List[str]
    detected_behavior_shifts: List[str]
    rule_updates: Dict[str, float]
    experiments_to_run: List[str]
    blind_spots_discovered: List[str]
    human_review_notes: List[str]
    next_observation_plan: List[str]


class AdaptiveMarketLearningEngine:
    """Detects market drift and recommends controlled model adaptation."""

    DEFAULT_WEIGHTS: Dict[str, float] = {
        "price_sensitivity": 1.0,
        "trust_weight": 1.0,
        "delivery_urgency": 1.0,
        "social_proof": 1.0,
        "packaging": 1.0,
        "creative_freshness": 1.0,
        "supplier_reliability": 1.0,
        "profit_leakage": 1.0,
        "brand_consistency": 1.0,
        "ethics_guardrail": 1.0,
    }

    @staticmethod
    def _bounded(value: float, lower: float = 0.1, upper: float = 3.0) -> float:
        return round(max(lower, min(upper, value)), 3)

    @staticmethod
    def _gap(expected: float | None, actual: float | None) -> float | None:
        if expected is None or actual is None or expected == 0:
            return None
        return (actual - expected) / abs(expected)

    @staticmethod
    def compare_prediction_to_actual(prediction: PredictionSnapshot, actual: ActualOutcomeSnapshot) -> List[str]:
        summary: List[str] = []
        gaps = {
            "score": AdaptiveMarketLearningEngine._gap(prediction.expected_score, actual.actual_score),
            "real_cpa": AdaptiveMarketLearningEngine._gap(prediction.expected_real_cpa, actual.actual_real_cpa),
            "conversion_rate": AdaptiveMarketLearningEngine._gap(prediction.expected_conversion_rate, actual.actual_conversion_rate),
            "delivery_rate": AdaptiveMarketLearningEngine._gap(prediction.expected_delivery_rate, actual.actual_delivery_rate),
            "net_profit": AdaptiveMarketLearningEngine._gap(prediction.expected_net_profit, actual.actual_net_profit),
        }
        for name, gap in gaps.items():
            if gap is None:
                continue
            pct = round(gap * 100, 2)
            if abs(gap) >= 0.25:
                summary.append(f"{name} changed materially vs prediction: {pct}% gap.")
            elif abs(gap) >= 0.1:
                summary.append(f"{name} changed moderately vs prediction: {pct}% gap.")

        unexpected_objections = [obj for obj in actual.observed_objections if obj not in prediction.expected_objections]
        if unexpected_objections:
            summary.append("Unexpected objections appeared: " + " | ".join(unexpected_objections[:6]))
        if not summary:
            summary.append("Prediction and actual outcome are broadly aligned within MVP tolerance.")
        return summary

    @staticmethod
    def infer_behavior_shifts(signals: List[MarketSignal], actual: ActualOutcomeSnapshot) -> List[HumanBehaviorShift]:
        shifts: List[HumanBehaviorShift] = []
        text = " ".join([s.description + " " + s.evidence for s in signals]).lower()
        objections = " ".join(actual.observed_objections).lower()

        if any(word in text + objections for word in ["غالي", "السعر", "خصم", "أوفر", "أرخص", "expensive", "price"]):
            shifts.append(HumanBehaviorShift.PRICE_SENSITIVITY_UP)
        if any(word in text + objections for word in ["ثقة", "نصب", "حقيقي", "زي الصورة", "review", "trust", "scam"]):
            shifts.append(HumanBehaviorShift.TRUST_DEMAND_UP)
        if any(word in text + objections for word in ["هتلحق", "بكرة", "نهارده", "توصيل", "delivery", "late"]):
            shifts.append(HumanBehaviorShift.DELIVERY_URGENCY_UP)
        if any(word in text + objections for word in ["مين جرب", "تقييم", "صور عملاء", "reviews", "proof"]):
            shifts.append(HumanBehaviorShift.SOCIAL_PROOF_DEMAND_UP)
        if any(word in text for word in ["ctr down", "frequency", "مل", "اتحرق", "fatigue"]):
            shifts.append(HumanBehaviorShift.NOVELTY_FATIGUE)
        if any(word in text + objections for word in ["قيمة", "ينفع", "عملي", "worth", "value"]):
            shifts.append(HumanBehaviorShift.VALUE_SEEKING_UP)
        if any(word in text + objections for word in ["شيك", "محترم", "مقام", "برستيج", "status"]):
            shifts.append(HumanBehaviorShift.STATUS_SIGNALING_UP)
        if any(word in text for word in ["tiktok", "instagram", "facebook", "whatsapp", "channel"]):
            shifts.append(HumanBehaviorShift.CHANNEL_MIGRATION)

        unique: List[HumanBehaviorShift] = []
        for shift in shifts:
            if shift not in unique:
                unique.append(shift)
        return unique or [HumanBehaviorShift.UNKNOWN]

    @staticmethod
    def propose_weight_updates(weights: Dict[str, float], shifts: List[HumanBehaviorShift], signals: List[MarketSignal]) -> Dict[str, float]:
        updated = dict(AdaptiveMarketLearningEngine.DEFAULT_WEIGHTS)
        updated.update(weights or {})

        for shift in shifts:
            if shift == HumanBehaviorShift.PRICE_SENSITIVITY_UP:
                updated["price_sensitivity"] = AdaptiveMarketLearningEngine._bounded(updated["price_sensitivity"] + 0.15)
            elif shift == HumanBehaviorShift.TRUST_DEMAND_UP:
                updated["trust_weight"] = AdaptiveMarketLearningEngine._bounded(updated["trust_weight"] + 0.2)
            elif shift == HumanBehaviorShift.DELIVERY_URGENCY_UP:
                updated["delivery_urgency"] = AdaptiveMarketLearningEngine._bounded(updated["delivery_urgency"] + 0.15)
            elif shift == HumanBehaviorShift.SOCIAL_PROOF_DEMAND_UP:
                updated["social_proof"] = AdaptiveMarketLearningEngine._bounded(updated["social_proof"] + 0.15)
            elif shift == HumanBehaviorShift.NOVELTY_FATIGUE:
                updated["creative_freshness"] = AdaptiveMarketLearningEngine._bounded(updated["creative_freshness"] + 0.2)
            elif shift == HumanBehaviorShift.VALUE_SEEKING_UP:
                updated["packaging"] = AdaptiveMarketLearningEngine._bounded(updated["packaging"] + 0.05)
                updated["profit_leakage"] = AdaptiveMarketLearningEngine._bounded(updated["profit_leakage"] + 0.1)
            elif shift == HumanBehaviorShift.STATUS_SIGNALING_UP:
                updated["packaging"] = AdaptiveMarketLearningEngine._bounded(updated["packaging"] + 0.15)

        for signal in signals:
            if signal.signal_type == MarketSignalType.SUPPLIER_EVENT:
                updated["supplier_reliability"] = AdaptiveMarketLearningEngine._bounded(updated["supplier_reliability"] + 0.2)
            if signal.signal_type == MarketSignalType.PROFIT_LEAKAGE:
                updated["profit_leakage"] = AdaptiveMarketLearningEngine._bounded(updated["profit_leakage"] + 0.2)
            if signal.signal_type == MarketSignalType.BRAND_DRIFT:
                updated["brand_consistency"] = AdaptiveMarketLearningEngine._bounded(updated["brand_consistency"] + 0.25)
            if signal.signal_type == MarketSignalType.ETHICS_RISK:
                updated["ethics_guardrail"] = AdaptiveMarketLearningEngine._bounded(updated["ethics_guardrail"] + 0.3)

        return updated

    @staticmethod
    def experiments_for(shifts: List[HumanBehaviorShift], signals: List[MarketSignal]) -> List[str]:
        experiments: List[str] = []
        if HumanBehaviorShift.PRICE_SENSITIVITY_UP in shifts:
            experiments.append("Test value framing vs discount framing while keeping the same product price.")
        if HumanBehaviorShift.TRUST_DEMAND_UP in shifts:
            experiments.append("Test creative with real photos, reviews, exchange policy, and unboxing proof stack.")
        if HumanBehaviorShift.DELIVERY_URGENCY_UP in shifts:
            experiments.append("Test city-limited fast delivery promise instead of national promise.")
        if HumanBehaviorShift.SOCIAL_PROOF_DEMAND_UP in shifts:
            experiments.append("Test customer-photo carousel and WhatsApp screenshots against product-only creative.")
        if HumanBehaviorShift.NOVELTY_FATIGUE in shifts:
            experiments.append("Rotate first 3 seconds, hook, and UGC angle before changing the entire offer.")
        if HumanBehaviorShift.STATUS_SIGNALING_UP in shifts:
            experiments.append("Test premium packaging angle: 'شكلها أغلى من سعرها' vs practical use angle.")

        for signal in signals:
            if signal.signal_type == MarketSignalType.COMPETITOR_MOVE:
                experiments.append("Run competitor-response test: stronger bundle vs faster delivery vs better packaging.")
            if signal.signal_type == MarketSignalType.SUPPLIER_EVENT:
                experiments.append("Test backup supplier or substitute product before scaling spend.")
            if signal.signal_type == MarketSignalType.PROFIT_LEAKAGE:
                experiments.append("Run margin audit: packaging, delivery, returns, discounts, COD fees, and damaged units.")

        return experiments or ["Run a controlled A/B test before changing core model rules."]

    @staticmethod
    def evaluate_learning(payload: LearningInput) -> LearningOutput:
        prediction_gaps = AdaptiveMarketLearningEngine.compare_prediction_to_actual(payload.prediction, payload.actual)
        shifts = AdaptiveMarketLearningEngine.infer_behavior_shifts(payload.signals, payload.actual)
        updated_weights = AdaptiveMarketLearningEngine.propose_weight_updates(payload.current_weights, shifts, payload.signals)

        severity_score = 0.0
        for signal in payload.signals:
            severity_score += {
                LearningSeverity.LOW: 0.5,
                LearningSeverity.MEDIUM: 1.0,
                LearningSeverity.HIGH: 2.0,
                LearningSeverity.CRITICAL: 3.0,
            }[signal.severity]

        gap_count = sum(1 for item in prediction_gaps if "materially" in item.lower())
        severity_score += gap_count * 1.2
        if payload.actual.actual_net_profit is not None and payload.actual.actual_net_profit < 0:
            severity_score += 2.5
        if payload.actual.refund_or_return_rate is not None and payload.actual.refund_or_return_rate > 0.25:
            severity_score += 1.5

        learning_score = round(min(10.0, severity_score), 2)
        severity = (
            LearningSeverity.CRITICAL if learning_score >= 7.5 else
            LearningSeverity.HIGH if learning_score >= 5 else
            LearningSeverity.MEDIUM if learning_score >= 2 else
            LearningSeverity.LOW
        )

        if severity == LearningSeverity.CRITICAL:
            action = LearningAction.PAUSE_SCALING
        elif severity == LearningSeverity.HIGH:
            action = LearningAction.ESCALATE_HUMAN_REVIEW
        elif severity == LearningSeverity.MEDIUM:
            action = LearningAction.RUN_EXPERIMENT
        elif shifts != [HumanBehaviorShift.UNKNOWN]:
            action = LearningAction.WATCH
        else:
            action = LearningAction.KEEP_RULE

        blind_spots: List[str] = []
        for signal in payload.signals:
            if signal.severity in {LearningSeverity.HIGH, LearningSeverity.CRITICAL}:
                blind_spots.append(f"New high-impact signal in {signal.affected_layer}: {signal.description}")
        if any("Unexpected objections" in gap for gap in prediction_gaps):
            blind_spots.append("Customer objection pattern changed; update objection library.")
        if not blind_spots:
            blind_spots.append("No new critical blind spot detected; continue observation.")

        human_notes = [
            "Do not auto-update core rules from one campaign only.",
            "Require repeated signals or strong evidence before changing strategic weights.",
            "Protect brand positioning and ethics guardrails even when short-term CPA improves.",
        ]
        if severity in {LearningSeverity.HIGH, LearningSeverity.CRITICAL}:
            human_notes.append("Human review required before scaling or changing permanent rules.")

        observation_plan = [
            "Collect next 7 days of Meta CPA, Real CPA, confirmation rate, delivery rate, and net profit.",
            "Tag WhatsApp objections by category: price, trust, delivery, taste, social risk, exchange policy.",
            "Monitor competitor offer, price, packaging, and delivery promise weekly.",
            "Track creative fatigue: CTR, frequency, comments quality, CPA drift.",
            "Compare expected vs actual repeat purchase and review generation.",
        ]

        return LearningOutput(
            learning_score=learning_score,
            severity=severity,
            action=action,
            prediction_gap_summary=prediction_gaps,
            detected_behavior_shifts=[shift.value for shift in shifts],
            rule_updates=updated_weights,
            experiments_to_run=AdaptiveMarketLearningEngine.experiments_for(shifts, payload.signals),
            blind_spots_discovered=blind_spots,
            human_review_notes=human_notes,
            next_observation_plan=observation_plan,
        )
