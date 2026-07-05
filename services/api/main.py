# -*- coding: utf-8 -*-
"""FastAPI service for THINC v4.

This service is the integration bridge between:
- thinc-v4: proprietary scoring and decision-support engine.
- admatch-insights: React/TanStack dashboard frontend.

Run locally:
    uvicorn services.api.main:app --reload
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.api.schemas import (
    CampaignAnalysisRequest,
    CampaignAnalysisResponse,
    Decision,
    FounderReadinessRequest,
    FounderReadinessResponse,
    HealthResponse,
    IntegrationMode,
    IntegrationStatusItem,
    IntegrationStatusResponse,
    RiskLevel,
    TheorySummaryResponse,
)
from thinc_v4.framework import FounderOS, ScientificTheoryRegistry, get_watermark

app = FastAPI(
    title="THINC v4 API",
    description="Decision-support API for THINC Intelligence OS and AdMatch Insights.",
    version="1.0.0-mvp",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:8787"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _safe_div(numerator: float, denominator: float) -> float | None:
    if denominator <= 0:
        return None
    return numerator / denominator


def _pct(numerator: float, denominator: float) -> float:
    if denominator <= 0:
        return 0.0
    return round(numerator / denominator * 100, 2)


def _round(value: float | None, digits: int = 2) -> float | None:
    if value is None:
        return None
    return round(value, digits)


def _score_campaign(
    *,
    net_profit: float,
    real_cpa: float | None,
    safe_cpa_ceiling: float,
    confirmation_rate: float,
    delivery_rate: float,
    attribution_gap_pct: float | None,
    inventory_units: int,
    delivered_orders: int,
) -> tuple[float, Decision, RiskLevel, list[str], list[str]]:
    """Return a simple MVP score and decision.

    This is deliberately transparent and conservative. Later versions can call
    deeper THINC scoring classes, but the API contract should remain stable.
    """
    score = 5.0
    blind_spots: list[str] = []
    recommendations: list[str] = []

    if net_profit > 0:
        score += 1.5
    else:
        score -= 2.0
        blind_spots.append("Campaign is not profitable after operational costs.")
        recommendations.append("Do not scale before fixing margin, CPA, or delivery economics.")

    if real_cpa is not None and real_cpa <= safe_cpa_ceiling:
        score += 1.0
    else:
        score -= 1.0
        blind_spots.append("Real CPA is above the safe CPA ceiling or cannot be calculated.")
        recommendations.append("Lower CPA or increase contribution margin before scaling.")

    if confirmation_rate >= 70:
        score += 0.8
    elif confirmation_rate >= 45:
        score -= 0.3
        blind_spots.append("Confirmation rate is acceptable but not strong enough for aggressive scaling.")
        recommendations.append("Improve call center script and WhatsApp confirmation follow-up.")
    else:
        score -= 1.2
        blind_spots.append("Confirmation rate is below the safe threshold.")
        recommendations.append("Fix lead quality, offer clarity, and confirmation process.")

    if delivery_rate >= 75:
        score += 0.7
    elif delivery_rate >= 55:
        score -= 0.2
        blind_spots.append("Delivery rate is moderate; returns or failed delivery may damage profit.")
        recommendations.append("Review shipping provider, confirmation quality, and address validation.")
    else:
        score -= 1.2
        blind_spots.append("Delivery rate is weak enough to distort Meta CPA.")
        recommendations.append("Do not judge campaign quality from Meta dashboard alone.")

    if attribution_gap_pct is not None and attribution_gap_pct > 150:
        score -= 0.8
        blind_spots.append("Meta CPA is materially lower than Real CPA.")
        recommendations.append("Use Real CPA as the main scaling metric, not Meta CPA.")

    if delivered_orders > 0 and inventory_units > 0:
        inventory_days = inventory_units / delivered_orders
        if inventory_days < 7:
            score -= 0.4
            blind_spots.append("Inventory may not support scaling.")
            recommendations.append("Secure inventory before increasing spend.")

    score = round(max(0.0, min(10.0, score)), 2)

    if score >= 7.5 and net_profit > 0 and real_cpa is not None and real_cpa <= safe_cpa_ceiling and delivery_rate >= 70:
        decision = Decision.SCALE
        risk = RiskLevel.LOW
        recommendations.append("Scale gradually and keep monitoring Real CPA and delivery rate.")
    elif score < 4.0 or net_profit < 0:
        decision = Decision.KILL
        risk = RiskLevel.CRITICAL if net_profit < 0 else RiskLevel.HIGH
        recommendations.append("Stop or heavily restrict spend until the core economics are repaired.")
    else:
        decision = Decision.FIX
        risk = RiskLevel.MEDIUM
        recommendations.append("Run a fix sprint before scaling: offer, creative, confirmation, and delivery.")

    if not blind_spots:
        blind_spots.append("No critical blind spot detected in the provided MVP data.")
    if not recommendations:
        recommendations.append("Maintain controlled scaling and keep validating the data.")

    return score, decision, risk, blind_spots, recommendations


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="thinc-api", engine="THINC v4.0", mode="development")


@app.get("/api/theories/summary", response_model=TheorySummaryResponse)
def theory_summary() -> TheorySummaryResponse:
    return TheorySummaryResponse(
        count=ScientificTheoryRegistry.count(),
        domains=ScientificTheoryRegistry.by_domain(),
        watermark=get_watermark(),
    )


@app.post("/api/campaign/analyze", response_model=CampaignAnalysisResponse)
def analyze_campaign(payload: CampaignAnalysisRequest) -> CampaignAnalysisResponse:
    product = payload.product
    campaign = payload.campaign
    economics = payload.economics

    meta_cpa = _safe_div(campaign.spend, campaign.meta_leads)
    real_cpa = _safe_div(campaign.spend, campaign.delivered_orders)
    confirmation_rate = _pct(campaign.confirmed_orders, campaign.meta_leads)
    delivery_rate = _pct(campaign.delivered_orders, campaign.confirmed_orders)

    if meta_cpa is None or real_cpa is None or meta_cpa <= 0:
        attribution_gap_pct = None
    else:
        attribution_gap_pct = (real_cpa / meta_cpa - 1) * 100

    revenue = campaign.delivered_orders * product.price
    cogs = campaign.delivered_orders * product.cost
    failed_confirmed = max(campaign.confirmed_orders - campaign.delivered_orders, 0)
    shipping_cost = (
        campaign.delivered_orders * economics.shipping_success_cost
        + failed_confirmed * economics.shipping_return_cost
    )
    packaging_cost = campaign.confirmed_orders * economics.packaging_cost_per_order
    taxable_base = max(revenue - cogs, 0)
    tax = taxable_base * economics.vat_rate
    total_expenses = cogs + campaign.spend + shipping_cost + packaging_cost + economics.overhead + tax
    net_profit = revenue - total_expenses
    roas = campaign.spend and revenue / campaign.spend or 0.0
    roi = total_expenses and net_profit / total_expenses or 0.0

    contribution_margin = product.price - product.cost - economics.shipping_success_cost - economics.packaging_cost_per_order
    safe_cpa_ceiling = max(0.0, contribution_margin * 0.65)

    thinc_score, decision, risk_level, blind_spots, recommendations = _score_campaign(
        net_profit=net_profit,
        real_cpa=real_cpa,
        safe_cpa_ceiling=safe_cpa_ceiling,
        confirmation_rate=confirmation_rate,
        delivery_rate=delivery_rate,
        attribution_gap_pct=attribution_gap_pct,
        inventory_units=product.inventory_units,
        delivered_orders=campaign.delivered_orders,
    )

    return CampaignAnalysisResponse(
        campaign_name=campaign.name,
        product_name=product.name,
        meta_cpa=_round(meta_cpa),
        real_cpa=_round(real_cpa),
        confirmation_rate=confirmation_rate,
        delivery_rate=delivery_rate,
        attribution_gap_pct=_round(attribution_gap_pct),
        revenue=round(revenue, 2),
        cogs=round(cogs, 2),
        shipping_cost=round(shipping_cost, 2),
        packaging_cost=round(packaging_cost, 2),
        tax=round(tax, 2),
        total_expenses=round(total_expenses, 2),
        net_profit=round(net_profit, 2),
        roas=round(roas, 2),
        roi=round(roi, 2),
        thinc_score=thinc_score,
        decision=decision,
        risk_level=risk_level,
        blind_spots=blind_spots,
        recommendations=recommendations,
    )


@app.post("/api/founder/readiness", response_model=FounderReadinessResponse)
def founder_readiness(payload: FounderReadinessRequest) -> FounderReadinessResponse:
    founder = FounderOS(
        execution_score=payload.execution_score,
        discipline_score=payload.discipline_score,
        learning_speed_score=payload.learning_speed_score,
        resilience_score=payload.resilience_score,
        focus_score=payload.focus_score,
        financial_discipline_score=payload.financial_discipline_score,
    )
    readiness = founder.founder_readiness()
    return FounderReadinessResponse(
        score=float(readiness["score"]),
        verdict=str(readiness["verdict"]),
        recommendations=founder.coaching_recommendations(),
    )


@app.get("/api/integrations/status", response_model=IntegrationStatusResponse)
def integration_status() -> IntegrationStatusResponse:
    items = [
        IntegrationStatusItem(
            integration="Meta Ads API",
            mode=IntegrationMode.DEMO,
            connected=False,
            message="Demo data only. Live OAuth integration is pending.",
        ),
        IntegrationStatusItem(
            integration="WhatsApp Business API",
            mode=IntegrationMode.DEMO,
            connected=False,
            message="Demo status only. Production credentials are not configured.",
        ),
        IntegrationStatusItem(
            integration="Shopify",
            mode=IntegrationMode.DEMO,
            connected=False,
            message="Demo status only. Live Shopify integration is pending.",
        ),
        IntegrationStatusItem(
            integration="Shipping Provider",
            mode=IntegrationMode.DEMO,
            connected=False,
            message="Demo status only. Delivery source integration is pending.",
        ),
    ]
    return IntegrationStatusResponse(items=items)
