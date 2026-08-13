# -*- coding: utf-8 -*-
"""Media economics and media test protocol value objects.

THINC™ v4.2 — Invented by Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 Dr. Ehab Taha — Egy-Pioneers Academy.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Dict, List
from .market_signals import (
    DecisionStage,
    MarketSignalGateResult,
)


class SalesChannel(Enum):
    WEBSITE = "website"
    WHATSAPP = "whatsapp"
    INSTAGRAM_DM = "instagram_dm"
    MESSENGER = "messenger"
    LEAD_FORM = "lead_form"


class TestBudgetMode(Enum):
    CONTROLLED_ABO = "Controlled ABO"
    META_AB_TEST = "Meta A/B Test"


class EvidenceMode(Enum):
    LEAN = "lean"
    STANDARD = "standard"
    CONSERVATIVE = "conservative"


@dataclass
class MediaEconomicsInput:
    """Per-order economics used to protect cash before any media scale decision."""

    selling_price: float
    product_cost: float
    packaging_cost: float = 0.0
    company_shipping_cost: float = 0.0
    collection_fees: float = 0.0
    expected_return_cost_per_order: float = 0.0
    variable_operations_cost: float = 0.0
    confirmation_rate_pct: float = 80.0
    delivery_rate_from_confirmed_pct: float = 75.0
    safety_margin_pct: float = 30.0


@dataclass
class MediaTestConfig:
    sales_channel: SalesChannel
    total_daily_budget: float
    angle_variants: int = 4
    hook_variants: int = 4
    editing_variants: int = 3
    offer_variants: int = 2
    pixel_ready: bool = False
    capi_ready: bool = False
    purchase_event_configured: bool = False
    sales_messaging_objective_available: bool = False
    country: str = "Egypt"
    audience_description: str = "Broad audience; same audience across all creative variants"
    exclude_existing_customers_days: int = 180
    budget_mode: TestBudgetMode = TestBudgetMode.CONTROLLED_ABO
    evidence_mode: EvidenceMode = EvidenceMode.STANDARD
    decision_stage: DecisionStage = DecisionStage.PRE_TEST_RESEARCH


@dataclass
class CampaignObjectivePlan:
    objective: str
    conversion_location: str
    destination: str
    performance_goal: str
    optimization_event: str
    readiness: str
    prerequisites: List[str]
    rationale: List[str]


@dataclass
class MediaEconomicsResult:
    contribution_margin_before_ads: float
    break_even_delivered_cpa: float
    target_delivered_cpa: float
    target_confirmed_cpa: float
    target_purchase_cpa: float
    confirmation_rate_pct: float
    delivery_rate_from_confirmed_pct: float
    expected_purchase_to_delivery_rate_pct: float


@dataclass
class MediaTestStagePlan:
    stage: str
    variable_tested: str
    variants: int
    recommended_days: int
    daily_budget_total: float
    daily_budget_per_variant: float
    target_spend_per_variant: float
    estimated_stage_budget: float
    controlled_variables: List[str]
    graduation_gate: List[str]


@dataclass
class StopLossPolicy:
    attention_review_impressions: int
    hard_review_impressions: int
    soft_stop_spend: float
    hard_stop_spend: float
    soft_stop_conditions: List[str]
    hard_stop_conditions: List[str]
    diagnostic_checks_before_kill: List[str]


@dataclass
class ScalePolicy:
    minimum_delivered_orders: int
    recommended_delivered_orders: int
    minimum_stable_days: int
    minimum_delivery_rate_pct: float
    maximum_delivered_cpa: float
    required_conditions: List[str]
    scaling_method: List[str]


@dataclass
class MediaTestProtocolReport:
    decision: str
    decision_reasons: List[str]
    market_signal_gate: MarketSignalGateResult
    objective_plan: CampaignObjectivePlan
    economics: MediaEconomicsResult
    campaign_structure: Dict[str, Any]
    stages: List[MediaTestStagePlan]
    stop_loss: StopLossPolicy
    scale_policy: ScalePolicy
    warnings: List[str]

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["market_signal_gate"] = self.market_signal_gate.to_dict()
        return data
