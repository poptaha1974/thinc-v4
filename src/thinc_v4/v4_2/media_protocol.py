# -*- coding: utf-8 -*-
"""Media test protocol engine: economics guardrails, stages, stop-loss, and scale policy.

THINC™ v4.2 — Invented by Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 Dr. Ehab Taha — Egy-Pioneers Academy.
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple
from .market_signals import (
    DecisionStage,
    GateDecision,
    MarketSignalEvidence,
    MarketSignalTriangulationEngine,
)
from .media_models import (
    CampaignObjectivePlan,
    EvidenceMode,
    MediaEconomicsInput,
    MediaEconomicsResult,
    MediaTestConfig,
    MediaTestProtocolReport,
    MediaTestStagePlan,
    SalesChannel,
    ScalePolicy,
    StopLossPolicy,
)


class MediaTestProtocolEngine:
    """
    Selects the campaign objective and builds a controlled media test protocol.

    The engine protects unit economics first, tests one creative variable at a
    time, and blocks scale until delivered orders produce positive profit.
    Platform labels may vary by ad account, so the generated plan records
    readiness and fallbacks instead of silently changing the business goal.
    """

    MIN_MAX_DAYS: Dict[str, Tuple[int, int]] = {
        "Angle Test": (4, 7),
        "Hook Test": (3, 5),
        "Editing Test": (3, 5),
        "Offer & CTA Test": (3, 5),
        "Winner Validation": (5, 7),
    }

    @staticmethod
    def _validate_percent(name: str, value: float) -> None:
        if not 0 < float(value) <= 100:
            raise ValueError(f"{name} must be greater than 0 and no more than 100.")

    @staticmethod
    def _numeric_campaign_metric(
        metrics: Dict[str, Any],
        name: str,
        reasons: List[str],
    ) -> float | None:
        value = metrics.get(name)
        if value is None:
            reasons.append(f"{name} is required by the existing SCALE policy")
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            reasons.append(f"{name} must be numeric for the existing SCALE policy")
            return None

    @classmethod
    def calculate_economics(cls, inputs: MediaEconomicsInput) -> MediaEconomicsResult:
        cls._validate_percent("confirmation_rate_pct", inputs.confirmation_rate_pct)
        cls._validate_percent("delivery_rate_from_confirmed_pct", inputs.delivery_rate_from_confirmed_pct)
        if not 0 <= float(inputs.safety_margin_pct) < 100:
            raise ValueError("safety_margin_pct must be between 0 and less than 100.")

        costs = (
            inputs.product_cost
            + inputs.packaging_cost
            + inputs.company_shipping_cost
            + inputs.collection_fees
            + inputs.expected_return_cost_per_order
            + inputs.variable_operations_cost
        )
        contribution = inputs.selling_price - costs
        if contribution <= 0:
            raise ValueError("Product contribution margin before advertising must be positive.")

        confirmation = inputs.confirmation_rate_pct / 100.0
        delivery = inputs.delivery_rate_from_confirmed_pct / 100.0
        purchase_to_delivery = confirmation * delivery
        target_delivered = contribution * (1.0 - inputs.safety_margin_pct / 100.0)
        target_confirmed = target_delivered * delivery
        target_purchase = target_confirmed * confirmation

        return MediaEconomicsResult(
            contribution_margin_before_ads=round(contribution, 2),
            break_even_delivered_cpa=round(contribution, 2),
            target_delivered_cpa=round(target_delivered, 2),
            target_confirmed_cpa=round(target_confirmed, 2),
            target_purchase_cpa=round(target_purchase, 2),
            confirmation_rate_pct=round(inputs.confirmation_rate_pct, 2),
            delivery_rate_from_confirmed_pct=round(inputs.delivery_rate_from_confirmed_pct, 2),
            expected_purchase_to_delivery_rate_pct=round(purchase_to_delivery * 100.0, 2),
        )

    @staticmethod
    def choose_objective(config: MediaTestConfig) -> CampaignObjectivePlan:
        channel = config.sales_channel
        prerequisites: List[str] = []
        rationale: List[str] = []

        if channel == SalesChannel.WEBSITE:
            prerequisites = [
                "Meta Pixel is installed and firing correctly",
                "Purchase event is configured and deduplicated",
                "Conversions API is recommended for server-side resilience",
                "Checkout and order confirmation flow have been tested",
            ]
            ready = config.pixel_ready and config.purchase_event_configured
            readiness = "READY" if ready else "BLOCKED — fix tracking before purchase testing"
            rationale = [
                "The business outcome is a purchase, so optimization must remain aligned with Purchase.",
                "Traffic or video-view optimization can identify cheap visitors or viewers rather than buyers.",
            ]
            if not config.capi_ready:
                rationale.append("CAPI is not mandatory to generate the plan, but its absence weakens measurement resilience.")
            return CampaignObjectivePlan(
                objective="Sales",
                conversion_location="Website",
                destination="Product / checkout website",
                performance_goal="Maximize number of conversions",
                optimization_event="Purchase",
                readiness=readiness,
                prerequisites=prerequisites,
                rationale=rationale,
            )

        if channel in {SalesChannel.WHATSAPP, SalesChannel.INSTAGRAM_DM, SalesChannel.MESSENGER}:
            app_name = {
                SalesChannel.WHATSAPP: "WhatsApp",
                SalesChannel.INSTAGRAM_DM: "Instagram Direct",
                SalesChannel.MESSENGER: "Messenger",
            }[channel]
            objective = "Sales" if config.sales_messaging_objective_available else "Leads"
            readiness = "READY"
            prerequisites = [
                f"{app_name} account is connected to the Meta business portfolio",
                "A qualification script separates inquiries from qualified leads",
                "Order, confirmation, and delivery statuses are recorded outside Ads Manager",
            ]
            rationale = [
                "Use the messaging objective available in the ad account while keeping the final KPI as delivered orders.",
                "A conversation is not counted as a sale; track qualified lead → order → confirmed → delivered.",
            ]
            return CampaignObjectivePlan(
                objective=objective,
                conversion_location="Messaging apps",
                destination=app_name,
                performance_goal="Maximize number of conversations",
                optimization_event="Qualified conversation with offline order tracking",
                readiness=readiness,
                prerequisites=prerequisites,
                rationale=rationale,
            )

        return CampaignObjectivePlan(
            objective="Leads",
            conversion_location="Instant forms",
            destination="Meta instant form",
            performance_goal="Maximize number of leads",
            optimization_event="Qualified lead",
            readiness="READY",
            prerequisites=[
                "The form includes qualification questions",
                "Lead status is synced to a CRM or order sheet",
                "Confirmed and delivered outcomes are fed back into reporting",
            ],
            rationale=["Use only when website or messaging checkout is not the operational path."],
        )

    @classmethod
    def _stage_days(
        cls,
        stage: str,
        target_spend_per_variant: float,
        budget_per_variant: float,
    ) -> int:
        min_days, max_days = cls.MIN_MAX_DAYS[stage]
        raw_days = math.ceil(target_spend_per_variant / max(1.0, budget_per_variant))
        return max(min_days, min(max_days, raw_days))

    @classmethod
    def _build_stage(
        cls,
        stage: str,
        variable: str,
        variants: int,
        total_daily_budget: float,
        target_purchase_cpa: float,
        spend_multiple: float,
        controlled: List[str],
        gate: List[str],
    ) -> MediaTestStagePlan:
        variants = max(1, int(variants))
        per_variant = total_daily_budget / variants
        target_spend = max(target_purchase_cpa, target_purchase_cpa * spend_multiple)
        days = cls._stage_days(stage, target_spend, per_variant)
        return MediaTestStagePlan(
            stage=stage,
            variable_tested=variable,
            variants=variants,
            recommended_days=days,
            daily_budget_total=round(total_daily_budget, 2),
            daily_budget_per_variant=round(per_variant, 2),
            target_spend_per_variant=round(target_spend, 2),
            estimated_stage_budget=round(total_daily_budget * days, 2),
            controlled_variables=controlled,
            graduation_gate=gate,
        )

    @classmethod
    def build(
        cls,
        economics_input: MediaEconomicsInput,
        config: MediaTestConfig,
        market_evidence: List[MarketSignalEvidence] | None = None,
    ) -> MediaTestProtocolReport:
        if config.total_daily_budget <= 0:
            raise ValueError("total_daily_budget must be positive.")
        economics = cls.calculate_economics(economics_input)
        objective = cls.choose_objective(config)
        market_gate = MarketSignalTriangulationEngine.evaluate(
            market_evidence or [],
            config.decision_stage,
        )

        angle_count = max(2, min(4, int(config.angle_variants)))
        hook_count = max(2, min(4, int(config.hook_variants)))
        editing_count = max(2, min(3, int(config.editing_variants)))
        offer_count = max(2, min(3, int(config.offer_variants)))
        cpa = economics.target_purchase_cpa

        stages = [
            cls._build_stage(
                "Angle Test", "Advertising angle", angle_count, config.total_daily_budget, cpa, 2.0,
                ["Audience", "Offer", "CTA", "Editing style", "Landing page / messaging script"],
                ["At least one conversion-quality signal", "Compare Purchase/qualified-order CPA", "Keep top 1–2 angles"],
            ),
            cls._build_stage(
                "Hook Test", "First 2–3 seconds", hook_count, config.total_daily_budget, cpa, 1.5,
                ["Winning angle", "Body", "Offer", "CTA", "Editing style"],
                ["Hook and hold improve without damaging purchase quality", "Select one winning hook"],
            ),
            cls._build_stage(
                "Editing Test", "Editing / format", editing_count, config.total_daily_budget, cpa, 1.5,
                ["Winning angle", "Winning hook", "Offer", "CTA"],
                ["Choose format by delivered-order economics, not watch time alone"],
            ),
            cls._build_stage(
                "Offer & CTA Test", "Offer or CTA — one at a time", offer_count, config.total_daily_budget, cpa, 1.5,
                ["Winning angle", "Winning hook", "Winning edit", "Audience"],
                ["Improved conversion rate", "Delivered CPA remains within target"],
            ),
            cls._build_stage(
                "Winner Validation", "No new creative variable", 1, config.total_daily_budget, cpa, 4.0,
                ["Creative", "Audience", "Offer", "CTA", "Tracking"],
                ["Delivered profit is positive", "Delivery rate is stable", "Scale gate is met"],
            ),
        ]

        soft_stop = round(cpa, 2)
        hard_stop = round(cpa * 1.75, 2)
        intent_signal = (
            "No Add to Cart / Checkout signal"
            if config.sales_channel == SalesChannel.WEBSITE
            else "No qualified conversation or order signal"
        )
        stop_loss = StopLossPolicy(
            attention_review_impressions=1500,
            hard_review_impressions=2000,
            soft_stop_spend=soft_stop,
            hard_stop_spend=hard_stop,
            soft_stop_conditions=[
                f"Spend reaches about 1× target Purchase CPA ({soft_stop:.2f})",
                intent_signal,
                "Weak outbound CTR and weak early retention together",
            ],
            hard_stop_conditions=[
                f"Spend reaches about 1.75× target Purchase CPA ({hard_stop:.2f}) with no purchase/order",
                "Creative is weak at attention, intent, and conversion layers",
                "No tracking or checkout defect explains the result",
            ],
            diagnostic_checks_before_kill=[
                "Verify website, checkout, form, or WhatsApp destination",
                "Verify Pixel/CAPI and event firing when using a website",
                "Verify price, stock, shipping, and offer clarity",
                "Verify the call-center response time and qualification script",
            ],
        )

        delivered_min = {
            EvidenceMode.LEAN: 5,
            EvidenceMode.STANDARD: 10,
            EvidenceMode.CONSERVATIVE: 20,
        }[config.evidence_mode]
        scale_policy = ScalePolicy(
            minimum_delivered_orders=delivered_min,
            recommended_delivered_orders=max(10, delivered_min),
            minimum_stable_days=3 if config.evidence_mode != EvidenceMode.CONSERVATIVE else 5,
            minimum_delivery_rate_pct=65.0,
            maximum_delivered_cpa=economics.target_delivered_cpa,
            required_conditions=[
                "Delivered profit is positive",
                "Delivered CPA is at or below the target",
                "Delivery rate is at least 65% or the business-specific minimum",
                "Results are stable for the minimum number of days",
                "No operational bottleneck in stock, confirmation, or fulfillment",
            ],
            scaling_method=[
                "Increase budget in controlled steps rather than a single large jump",
                "Keep the proven creative unchanged while validating the higher spend",
                "Continue generating iterations from the winning angle to avoid fatigue",
                "Recalculate CPA thresholds whenever price, cost, or delivery rates change",
            ],
        )

        decision = market_gate.decision.value
        decision_reasons = list(market_gate.reasons)
        scale_threshold_reasons: List[str] = []
        if (
            config.decision_stage is DecisionStage.SCALE
            and market_gate.decision is GateDecision.PASS
        ):
            campaign_snapshots = [
                item
                for item in market_gate.evidence_snapshot
                if item.get("source") == "first_party_campaign"
                and item.get("evaluated_status") == "FRESH"
            ]
            campaign_snapshot = max(
                campaign_snapshots,
                key=lambda item: str(item.get("collected_at") or ""),
            )
            campaign_metrics = dict(campaign_snapshot.get("metrics", {}))
            delivered_orders = cls._numeric_campaign_metric(
                campaign_metrics,
                "delivered_orders",
                scale_threshold_reasons,
            )
            delivered_cpa = cls._numeric_campaign_metric(
                campaign_metrics,
                "delivered_cpa",
                scale_threshold_reasons,
            )
            delivery_rate = cls._numeric_campaign_metric(
                campaign_metrics,
                "delivery_rate_pct",
                scale_threshold_reasons,
            )
            if (
                delivered_orders is not None
                and delivered_orders < scale_policy.minimum_delivered_orders
            ):
                scale_threshold_reasons.append(
                    "delivered_orders is below the existing minimum of "
                    f"{scale_policy.minimum_delivered_orders}"
                )
            if (
                delivered_cpa is not None
                and delivered_cpa > scale_policy.maximum_delivered_cpa
            ):
                scale_threshold_reasons.append(
                    "delivered_cpa exceeds the existing maximum of "
                    f"{scale_policy.maximum_delivered_cpa:.2f}"
                )
            if (
                delivery_rate is not None
                and delivery_rate < scale_policy.minimum_delivery_rate_pct
            ):
                scale_threshold_reasons.append(
                    "delivery_rate_pct is below the existing minimum of "
                    f"{scale_policy.minimum_delivery_rate_pct:.2f}"
                )
            if scale_threshold_reasons:
                decision = GateDecision.BLOCK_SCALE.value
                decision_reasons.extend(scale_threshold_reasons)
            else:
                decision_reasons.append(
                    "Existing delivered-order, Delivered CPA, and delivery-rate SCALE thresholds pass."
                )

        warnings: List[str] = []
        if objective.readiness.startswith("BLOCKED"):
            warnings.append("Website purchase testing is blocked until tracking and the Purchase event are ready.")
        if config.sales_channel == SalesChannel.WEBSITE and not config.capi_ready:
            warnings.append("CAPI is not ready; measurement may be less resilient than Pixel + CAPI together.")
        angle_budget_per_variant = config.total_daily_budget / angle_count
        if angle_budget_per_variant < cpa:
            warnings.append(
                "Daily budget per angle is below 1× target Purchase CPA. Test angles in waves or expect the maximum duration."
            )
        if config.total_daily_budget < cpa * 2:
            warnings.append("Total daily budget is low relative to target CPA; avoid testing too many variables simultaneously.")
        if config.sales_channel != SalesChannel.WEBSITE:
            warnings.append("Ads Manager conversations/leads are intermediate signals; the final winner must use confirmed and delivered orders.")
        if market_gate.decision is GateDecision.HOLD_FOR_RESEARCH:
            warnings.append(
                "Market research is held until fresh Google Trends, Meta Ad Library, and marketplace evidence is supplied."
            )
        elif market_gate.decision is GateDecision.BLOCK_SCALE:
            warnings.append(
                "Scale is blocked until the market gate and fresh first-party delivered-profit evidence pass."
            )
        if scale_threshold_reasons:
            warnings.append(
                "Market evidence is complete, but the independent Media Test Protocol SCALE thresholds block expansion."
            )

        campaign_structure = {
            "naming": "[PRODUCT]_[VARIABLE]_TEST_[OBJECTIVE]",
            "budget_method": config.budget_mode.value,
            "ad_sets": "One identical ad set per variant during controlled testing",
            "ads_per_ad_set": 1,
            "audience": config.audience_description,
            "country": config.country,
            "placements": "Advantage+ placements unless a placement-specific hypothesis is being tested",
            "exclusions": f"Exclude existing customers/purchasers for {config.exclude_existing_customers_days} days where data is available",
            "change_control": "Change one variable only in each stage",
            "final_kpi": "Delivered profit and Delivered CPA",
        }

        return MediaTestProtocolReport(
            decision=decision,
            decision_reasons=decision_reasons,
            market_signal_gate=market_gate,
            objective_plan=objective,
            economics=economics,
            campaign_structure=campaign_structure,
            stages=stages,
            stop_loss=stop_loss,
            scale_policy=scale_policy,
            warnings=warnings,
        )
