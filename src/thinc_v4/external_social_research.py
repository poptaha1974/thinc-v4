# -*- coding: utf-8 -*-
"""External Social Research & Daily Intelligence Engine for THINC v4.0.

This module gives THINC a structured way to ingest and evaluate public research,
news, economic/social analysis, price-direction signals, search trends, and daily
events affecting Egyptian society.

It does not scrape Google or news websites directly. Instead, it defines the
canonical data contract for approved connectors such as:

- Google Programmable Search / SerpAPI / other compliant search APIs,
- Google Trends or trend-export workflows,
- RSS/news APIs,
- official statistics sources,
- analyst reports,
- manually reviewed research notes,
- internal WhatsApp/call-center observations,
- and price-monitoring feeds.

Important cautions:
    1. Political signals are context signals, not persuasion instructions.
    2. Sources must be cited and scored for reliability.
    3. Human review is required before changing strategic rules.
    4. This engine produces decision-support intelligence, not certainty.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Dict, List


class ResearchSourceType(Enum):
    OFFICIAL_STATISTICS = "official_statistics"
    CENTRAL_BANK = "central_bank"
    GOVERNMENT_RELEASE = "government_release"
    NEWS = "news"
    ECONOMIC_ANALYSIS = "economic_analysis"
    SOCIAL_ANALYSIS = "social_analysis"
    SEARCH_TRENDS = "search_trends"
    PRICE_MONITORING = "price_monitoring"
    SOCIAL_MEDIA_TREND = "social_media_trend"
    THINK_TANK = "think_tank"
    INTERNATIONAL_ORG = "international_org"
    INTERNAL_OBSERVATION = "internal_observation"
    MANUAL_RESEARCH_NOTE = "manual_research_note"


class EgyptResearchDomain(Enum):
    INFLATION_PRICES = "inflation_prices"
    EXCHANGE_RATE = "exchange_rate"
    INTEREST_RATES = "interest_rates"
    EMPLOYMENT_INCOME = "employment_income"
    CONSUMER_CONFIDENCE = "consumer_confidence"
    FAMILY_SOCIAL_NORMS = "family_social_norms"
    RELIGIOUS_SEASONALITY = "religious_seasonality"
    POLITICAL_CONTEXT = "political_context"
    REGULATION_LAW = "regulation_law"
    COMPETITOR_MARKET = "competitor_market"
    PRODUCT_CATEGORY_TREND = "product_category_trend"
    CHANNEL_BEHAVIOR = "channel_behavior"
    CULTURAL_MOMENT = "cultural_moment"
    SUPPLY_CHAIN = "supply_chain"
    GENERAL_SENTIMENT = "general_sentiment"


class SignalDirection(Enum):
    UP = "up"
    DOWN = "down"
    STABLE = "stable"
    MIXED = "mixed"
    SHOCK = "shock"
    UNKNOWN = "unknown"


class EvidenceStrength(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERIFIED = "verified"


class MarketImpact(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CommercialImplication(Enum):
    PRICE_SENSITIVITY = "price_sensitivity"
    TRUST_REQUIREMENT = "trust_requirement"
    DELIVERY_RISK = "delivery_risk"
    OFFER_REPOSITIONING = "offer_repositioning"
    CATEGORY_DEMAND_UP = "category_demand_up"
    CATEGORY_DEMAND_DOWN = "category_demand_down"
    CHANNEL_SHIFT = "channel_shift"
    CASHFLOW_PRESSURE = "cashflow_pressure"
    SOCIAL_RISK = "social_risk"
    BRAND_TONE_ADJUSTMENT = "brand_tone_adjustment"
    NO_ACTION = "no_action"


@dataclass(frozen=True)
class ResearchSource:
    title: str
    source_name: str
    source_type: ResearchSourceType
    url: str | None = None
    published_at: datetime | None = None
    retrieved_at: datetime | None = None
    author: str | None = None
    citation: str | None = None
    reliability_score: float = 5.0


@dataclass(frozen=True)
class ResearchObservation:
    domain: EgyptResearchDomain
    summary: str
    evidence: str
    direction: SignalDirection = SignalDirection.UNKNOWN
    evidence_strength: EvidenceStrength = EvidenceStrength.MEDIUM
    market_impact: MarketImpact = MarketImpact.MEDIUM
    commercial_implications: List[CommercialImplication] = field(default_factory=list)
    affected_segments: List[str] = field(default_factory=list)
    affected_categories: List[str] = field(default_factory=list)
    source: ResearchSource | None = None


@dataclass(frozen=True)
class DailyEgyptIntelligenceInput:
    intelligence_date: date
    observations: List[ResearchObservation]
    baseline_weights: Dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class DailyEgyptIntelligenceOutput:
    intelligence_date: date
    confidence_score: float
    top_signals: List[str]
    behavior_shifts: List[str]
    commercial_risks: List[str]
    commercial_opportunities: List[str]
    recommended_weight_updates: Dict[str, float]
    campaign_guidance: List[str]
    research_gaps: List[str]
    required_human_review: List[str]
    source_audit: List[str]


class ExternalSocialResearchEngine:
    """Aggregates external Egypt signals into commercial learning updates."""

    DEFAULT_WEIGHTS: Dict[str, float] = {
        "price_sensitivity": 1.0,
        "trust_requirement": 1.0,
        "delivery_risk": 1.0,
        "offer_value_framing": 1.0,
        "social_risk": 1.0,
        "political_context_caution": 1.0,
        "seasonality": 1.0,
        "search_trend_momentum": 1.0,
        "category_demand": 1.0,
        "brand_tone_sensitivity": 1.0,
    }

    OFFICIAL_SOURCE_NAMES = {
        "CAPMAS",
        "Central Bank of Egypt",
        "CBE",
        "Ministry of Finance",
        "IMF",
        "World Bank",
        "FAO",
        "UNDP",
    }

    @staticmethod
    def _bounded(value: float, lower: float = 0.1, upper: float = 3.0) -> float:
        return round(max(lower, min(upper, value)), 3)

    @staticmethod
    def source_audit(observation: ResearchObservation) -> str:
        if observation.source is None:
            return "Missing source: observation requires citation or internal note reference."
        source = observation.source
        warnings: List[str] = []
        if not source.url and source.source_type not in {ResearchSourceType.INTERNAL_OBSERVATION, ResearchSourceType.MANUAL_RESEARCH_NOTE}:
            warnings.append("missing_url")
        if source.reliability_score < 5:
            warnings.append("low_reliability")
        if observation.domain == EgyptResearchDomain.POLITICAL_CONTEXT and observation.evidence_strength != EvidenceStrength.VERIFIED:
            warnings.append("political_signal_requires_verified_or_multi_source_confirmation")
        if not warnings:
            return f"OK: {source.source_name} | {source.source_type.value} | reliability={source.reliability_score}"
        return f"Review: {source.source_name} | " + ", ".join(warnings)

    @staticmethod
    def confidence_score(observations: List[ResearchObservation]) -> float:
        if not observations:
            return 0.0
        total = 0.0
        for obs in observations:
            source_score = obs.source.reliability_score if obs.source else 2.0
            strength_score = {
                EvidenceStrength.LOW: 3.0,
                EvidenceStrength.MEDIUM: 5.5,
                EvidenceStrength.HIGH: 7.5,
                EvidenceStrength.VERIFIED: 9.0,
            }[obs.evidence_strength]
            total += (source_score * 0.55) + (strength_score * 0.45)
        return round(min(10.0, total / len(observations)), 2)

    @staticmethod
    def summarize_top_signals(observations: List[ResearchObservation]) -> List[str]:
        ranked = sorted(
            observations,
            key=lambda obs: (
                {MarketImpact.LOW: 1, MarketImpact.MEDIUM: 2, MarketImpact.HIGH: 3, MarketImpact.CRITICAL: 4}[obs.market_impact],
                obs.source.reliability_score if obs.source else 0,
            ),
            reverse=True,
        )
        return [f"{obs.domain.value}: {obs.summary}" for obs in ranked[:8]] or ["No external signal available."]

    @staticmethod
    def infer_behavior_shifts(observations: List[ResearchObservation]) -> List[str]:
        shifts: List[str] = []
        for obs in observations:
            if obs.domain == EgyptResearchDomain.INFLATION_PRICES and obs.direction in {SignalDirection.UP, SignalDirection.SHOCK}:
                shifts.append("Higher price sensitivity and stronger demand for value justification.")
            if obs.domain == EgyptResearchDomain.EXCHANGE_RATE and obs.direction in {SignalDirection.UP, SignalDirection.SHOCK, SignalDirection.MIXED}:
                shifts.append("Imported product price anxiety and supplier repricing risk.")
            if obs.domain == EgyptResearchDomain.POLITICAL_CONTEXT:
                shifts.append("Public mood may become more cautious; avoid aggressive or polarizing messaging.")
            if obs.domain == EgyptResearchDomain.CONSUMER_CONFIDENCE and obs.direction == SignalDirection.DOWN:
                shifts.append("Customers may delay discretionary purchases unless offer value is clear.")
            if obs.domain == EgyptResearchDomain.SEARCH_TRENDS and obs.direction == SignalDirection.UP:
                shifts.append("Search intent is rising; test category-specific landing or content angles.")
            if obs.domain == EgyptResearchDomain.CHANNEL_BEHAVIOR:
                shifts.append("Channel behavior is changing; creative/message fit should be retested.")
            if obs.domain == EgyptResearchDomain.FAMILY_SOCIAL_NORMS:
                shifts.append("Social approval and family decision influence should be weighted higher.")
        unique: List[str] = []
        for shift in shifts:
            if shift not in unique:
                unique.append(shift)
        return unique or ["No clear behavior shift detected yet."]

    @staticmethod
    def update_weights(observations: List[ResearchObservation], baseline: Dict[str, float]) -> Dict[str, float]:
        weights = dict(ExternalSocialResearchEngine.DEFAULT_WEIGHTS)
        weights.update(baseline or {})

        for obs in observations:
            impact_multiplier = {
                MarketImpact.LOW: 0.03,
                MarketImpact.MEDIUM: 0.07,
                MarketImpact.HIGH: 0.13,
                MarketImpact.CRITICAL: 0.22,
            }[obs.market_impact]

            if CommercialImplication.PRICE_SENSITIVITY in obs.commercial_implications:
                weights["price_sensitivity"] = ExternalSocialResearchEngine._bounded(weights["price_sensitivity"] + impact_multiplier)
            if CommercialImplication.TRUST_REQUIREMENT in obs.commercial_implications:
                weights["trust_requirement"] = ExternalSocialResearchEngine._bounded(weights["trust_requirement"] + impact_multiplier)
            if CommercialImplication.DELIVERY_RISK in obs.commercial_implications:
                weights["delivery_risk"] = ExternalSocialResearchEngine._bounded(weights["delivery_risk"] + impact_multiplier)
            if CommercialImplication.OFFER_REPOSITIONING in obs.commercial_implications:
                weights["offer_value_framing"] = ExternalSocialResearchEngine._bounded(weights["offer_value_framing"] + impact_multiplier)
            if CommercialImplication.SOCIAL_RISK in obs.commercial_implications:
                weights["social_risk"] = ExternalSocialResearchEngine._bounded(weights["social_risk"] + impact_multiplier)
            if CommercialImplication.BRAND_TONE_ADJUSTMENT in obs.commercial_implications:
                weights["brand_tone_sensitivity"] = ExternalSocialResearchEngine._bounded(weights["brand_tone_sensitivity"] + impact_multiplier)
            if obs.domain == EgyptResearchDomain.POLITICAL_CONTEXT:
                weights["political_context_caution"] = ExternalSocialResearchEngine._bounded(weights["political_context_caution"] + impact_multiplier)
            if obs.domain == EgyptResearchDomain.RELIGIOUS_SEASONALITY:
                weights["seasonality"] = ExternalSocialResearchEngine._bounded(weights["seasonality"] + impact_multiplier)
            if obs.domain == EgyptResearchDomain.SEARCH_TRENDS:
                weights["search_trend_momentum"] = ExternalSocialResearchEngine._bounded(weights["search_trend_momentum"] + impact_multiplier)
            if obs.domain == EgyptResearchDomain.PRODUCT_CATEGORY_TREND:
                weights["category_demand"] = ExternalSocialResearchEngine._bounded(weights["category_demand"] + impact_multiplier)
        return weights

    @staticmethod
    def commercial_risks(observations: List[ResearchObservation]) -> List[str]:
        risks: List[str] = []
        for obs in observations:
            if obs.market_impact in {MarketImpact.HIGH, MarketImpact.CRITICAL}:
                if obs.domain == EgyptResearchDomain.INFLATION_PRICES:
                    risks.append("Price shocks may reduce conversion unless value, bundle, or installment framing is improved.")
                elif obs.domain == EgyptResearchDomain.EXCHANGE_RATE:
                    risks.append("FX movement may affect imported product costs and supplier pricing.")
                elif obs.domain == EgyptResearchDomain.POLITICAL_CONTEXT:
                    risks.append("Political/social tension requires cautious brand tone and non-polarizing creatives.")
                elif obs.domain == EgyptResearchDomain.SUPPLY_CHAIN:
                    risks.append("Supply chain signal may affect stock availability, delivery, or product quality consistency.")
                else:
                    risks.append(f"High-impact signal in {obs.domain.value}: {obs.summary}")
        return risks or ["No high-impact external commercial risk detected from provided observations."]

    @staticmethod
    def commercial_opportunities(observations: List[ResearchObservation]) -> List[str]:
        opportunities: List[str] = []
        for obs in observations:
            if obs.direction == SignalDirection.UP:
                if obs.domain == EgyptResearchDomain.SEARCH_TRENDS:
                    opportunities.append("Rising search intent: create topical content, landing page, or category-specific offer test.")
                if obs.domain == EgyptResearchDomain.PRODUCT_CATEGORY_TREND:
                    opportunities.append("Category momentum detected: test controlled budget before competitors saturate the angle.")
                if obs.domain == EgyptResearchDomain.RELIGIOUS_SEASONALITY:
                    opportunities.append("Seasonal context rising: prepare occasion-based offers and inventory earlier.")
        return opportunities or ["No clear external opportunity detected from provided observations."]

    @staticmethod
    def campaign_guidance(observations: List[ResearchObservation]) -> List[str]:
        guidance: List[str] = []
        domains = {obs.domain for obs in observations}
        implications = {imp for obs in observations for imp in obs.commercial_implications}

        if EgyptResearchDomain.INFLATION_PRICES in domains or CommercialImplication.PRICE_SENSITIVITY in implications:
            guidance.append("Avoid cheap positioning; frame offers as smart value, savings, durability, and practical use.")
        if CommercialImplication.TRUST_REQUIREMENT in implications:
            guidance.append("Move reviews, real photos, exchange policy, and delivery proof earlier in the creative and WhatsApp script.")
        if CommercialImplication.BRAND_TONE_ADJUSTMENT in implications or EgyptResearchDomain.POLITICAL_CONTEXT in domains:
            guidance.append("Use calm, non-polarizing language; avoid aggressive urgency when public mood is sensitive.")
        if EgyptResearchDomain.SEARCH_TRENDS in domains:
            guidance.append("Use search trend terms as hooks, SEO content, and Meta interest tests, but validate with conversion data.")
        if EgyptResearchDomain.SUPPLY_CHAIN in domains:
            guidance.append("Do not scale before confirming supplier price, stock, replacement options, and delivery capacity.")
        return guidance or ["Continue normal testing; no major campaign adjustment required from external research yet."]

    @staticmethod
    def research_gaps(observations: List[ResearchObservation]) -> List[str]:
        domains = {obs.domain for obs in observations}
        gaps: List[str] = []
        required = {
            EgyptResearchDomain.INFLATION_PRICES: "daily/weekly price and inflation context",
            EgyptResearchDomain.CONSUMER_CONFIDENCE: "consumer confidence or purchase-intent proxy",
            EgyptResearchDomain.SEARCH_TRENDS: "search trend momentum",
            EgyptResearchDomain.COMPETITOR_MARKET: "competitor movement",
            EgyptResearchDomain.CHANNEL_BEHAVIOR: "channel behavior shift",
        }
        for domain, label in required.items():
            if domain not in domains:
                gaps.append(f"Missing {label} signal.")
        return gaps or ["Core external research coverage is acceptable for today."]

    @staticmethod
    def human_review_required(observations: List[ResearchObservation]) -> List[str]:
        review: List[str] = []
        for obs in observations:
            if obs.domain == EgyptResearchDomain.POLITICAL_CONTEXT:
                review.append("Political context signal requires human review and neutral, non-persuasive handling.")
            if obs.source and obs.source.reliability_score < 5:
                review.append(f"Low reliability source requires review: {obs.source.source_name}")
            if obs.market_impact == MarketImpact.CRITICAL:
                review.append(f"Critical market signal requires review: {obs.summary}")
        return review or ["No mandatory human review triggered, but sampling review is still recommended."]

    @staticmethod
    def evaluate_daily_intelligence(payload: DailyEgyptIntelligenceInput) -> DailyEgyptIntelligenceOutput:
        return DailyEgyptIntelligenceOutput(
            intelligence_date=payload.intelligence_date,
            confidence_score=ExternalSocialResearchEngine.confidence_score(payload.observations),
            top_signals=ExternalSocialResearchEngine.summarize_top_signals(payload.observations),
            behavior_shifts=ExternalSocialResearchEngine.infer_behavior_shifts(payload.observations),
            commercial_risks=ExternalSocialResearchEngine.commercial_risks(payload.observations),
            commercial_opportunities=ExternalSocialResearchEngine.commercial_opportunities(payload.observations),
            recommended_weight_updates=ExternalSocialResearchEngine.update_weights(payload.observations, payload.baseline_weights),
            campaign_guidance=ExternalSocialResearchEngine.campaign_guidance(payload.observations),
            research_gaps=ExternalSocialResearchEngine.research_gaps(payload.observations),
            required_human_review=ExternalSocialResearchEngine.human_review_required(payload.observations),
            source_audit=[ExternalSocialResearchEngine.source_audit(obs) for obs in payload.observations],
        )
