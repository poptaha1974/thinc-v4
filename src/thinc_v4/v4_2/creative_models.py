# -*- coding: utf-8 -*-
"""Creative intelligence value objects (enums and dataclasses).

THINC™ v4.2 — Invented by Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 Dr. Ehab Taha — Egy-Pioneers Academy.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List


class BenefitType(Enum):
    FUNCTIONAL = "Functional"
    EMOTIONAL = "Emotional"
    SOCIAL = "Social"
    ECONOMIC = "Economic"


class AngleArchetype(Enum):
    PROBLEM = "Problem / Pain"
    TRANSFORMATION = "Transformation / Before-After"
    SPEED = "Speed / First Use"
    SAVINGS = "Savings / Alternative Cost"
    TRUST = "Trust / Authenticity / Guarantee"
    SOCIAL_PROOF = "Social Proof / Testimonial"
    OCCASION = "Occasion / Life Event"
    CONVENIENCE = "Convenience / Time Saving"
    INGREDIENT = "Ingredient / Mechanism"
    OBJECTION = "Objection Reversal"
    IDENTITY = "Identity / Self-Image"


class CreativeFormat(Enum):
    UGC = "UGC"
    DEMO = "Product Demo"
    BEFORE_AFTER = "Before / After"
    TESTIMONIAL = "Testimonial"
    CINEMATIC = "Cinematic"
    EXPERT = "Expert Explanation"
    COMPARISON = "Comparison"


class ExperimentVariable(Enum):
    ANGLE = "angle"
    HOOK = "hook"
    EDITING = "editing"
    OFFER = "offer"
    CTA = "cta"


@dataclass
class ProductFeature:
    name: str
    proof: str = ""
    functional_benefit: str = ""
    emotional_benefit: str = ""
    social_benefit: str = ""
    economic_benefit: str = ""
    claim_risk: str = "low"


@dataclass
class ProductProblem:
    visible_problem: str
    daily_cost: str = ""
    financial_cost: str = ""
    emotional_cost: str = ""
    urgency: float = 5.0
    frequency: float = 5.0


@dataclass
class EgyptianConsumerPersona:
    name: str
    age_range: str
    context: str
    dominant_pains: List[str]
    desired_outcomes: List[str]
    buying_triggers: List[str]
    objections: List[str]
    preferred_proof: List[str]
    price_sensitivity: float = 5.0
    trust_sensitivity: float = 7.0


@dataclass
class ProductIntelligenceInput:
    product_name: str
    category: str
    core_job: str
    features: List[ProductFeature]
    problems: List[ProductProblem]
    differentiators: List[str]
    proof_assets: List[str]
    usage_context: str = ""
    price: float | None = None
    competitor_reference_price: float | None = None
    forbidden_claims: List[str] = field(default_factory=list)


@dataclass
class AdvertisingAngle:
    id: str
    name: str
    archetype: AngleArchetype
    promise: str
    pain: str
    persona_name: str
    proof_required: List[str]
    recommended_formats: List[CreativeFormat]
    sample_hooks: List[str]
    scores: Dict[str, float]
    total_score: float
    cautions: List[str] = field(default_factory=list)


@dataclass
class StoryboardBeat:
    start_second: float
    end_second: float
    purpose: str
    visual: str
    on_screen_text: str
    voiceover: str = ""
    editing_note: str = ""


@dataclass
class CreativeBlueprint:
    angle_id: str
    format: CreativeFormat
    duration_seconds: int
    hook: str
    beats: List[StoryboardBeat]
    proof_sequence: List[str]
    cta: str
    export_ratios: List[str] = field(default_factory=lambda: ["9:16", "4:5", "1:1"])


@dataclass
class CreativeVariant:
    variant_id: str
    angle_id: str
    hook: str
    editing_style: str
    offer: str
    cta: str
    format: CreativeFormat


@dataclass
class CreativePerformance:
    variant_id: str
    spend: float
    impressions: int
    three_second_views: int
    outbound_clicks: int
    purchases: int
    confirmed_orders: int
    delivered_orders: int
    revenue: float
    gross_profit_per_delivered_order: float = 0.0
    average_watch_seconds: float = 0.0
    video_duration_seconds: float = 1.0


@dataclass
class WinnerDecision:
    variant_id: str
    decision: str
    score: float
    metrics: Dict[str, float]
    reasons: List[str]
