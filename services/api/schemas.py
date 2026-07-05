# -*- coding: utf-8 -*-
"""Pydantic schemas for the THINC API service.

These models define the stable contract between the THINC v4 core engine and
external clients such as AdMatch Insights.
"""
from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class Decision(str, Enum):
    KILL = "KILL"
    FIX = "FIX"
    SCALE = "SCALE"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IntegrationMode(str, Enum):
    DEMO = "demo"
    MANUAL_CSV = "manual_csv"
    LIVE_API = "live_api"
    ERROR = "error"


class ProductInput(BaseModel):
    name: str = Field(..., min_length=1)
    cost: float = Field(..., gt=0)
    price: float = Field(..., gt=0)
    inventory_units: int = Field(0, ge=0)
    category: str | None = None
    positioning: str | None = None
    target_market: str = "Egypt"


class CampaignInput(BaseModel):
    name: str = Field(..., min_length=1)
    spend: float = Field(..., ge=0)
    meta_leads: int = Field(..., ge=0)
    confirmed_orders: int = Field(..., ge=0)
    delivered_orders: int = Field(..., ge=0)
    returned_orders: int = Field(0, ge=0)
    time_window_days: int = Field(30, ge=1)
    channel: str = "Meta Ads"
    objective: str | None = None

    @model_validator(mode="after")
    def validate_order_flow(self) -> "CampaignInput":
        if self.confirmed_orders > self.meta_leads and self.meta_leads > 0:
            raise ValueError("confirmed_orders cannot exceed meta_leads unless a source mismatch model is added")
        if self.delivered_orders > self.confirmed_orders and self.confirmed_orders > 0:
            raise ValueError("delivered_orders cannot exceed confirmed_orders")
        if self.returned_orders > self.delivered_orders and self.delivered_orders > 0:
            raise ValueError("returned_orders cannot exceed delivered_orders")
        return self


class EconomicsInput(BaseModel):
    shipping_success_cost: float = Field(45, ge=0)
    shipping_return_cost: float = Field(25, ge=0)
    packaging_cost_per_order: float = Field(15, ge=0)
    overhead: float = Field(0, ge=0)
    vat_rate: float = Field(0.14, ge=0, le=1)


class CampaignAnalysisRequest(BaseModel):
    product: ProductInput
    campaign: CampaignInput
    economics: EconomicsInput = Field(default_factory=EconomicsInput)


class CampaignAnalysisResponse(BaseModel):
    campaign_name: str
    product_name: str
    meta_cpa: float | None
    real_cpa: float | None
    confirmation_rate: float
    delivery_rate: float
    attribution_gap_pct: float | None
    revenue: float
    cogs: float
    shipping_cost: float
    packaging_cost: float
    tax: float
    total_expenses: float
    net_profit: float
    roas: float
    roi: float
    thinc_score: float
    decision: Decision
    risk_level: RiskLevel
    blind_spots: list[str]
    recommendations: list[str]
    mode: Literal["decision_support"] = "decision_support"


class FounderReadinessRequest(BaseModel):
    execution_score: float = Field(..., ge=0, le=10)
    discipline_score: float = Field(..., ge=0, le=10)
    learning_speed_score: float = Field(..., ge=0, le=10)
    resilience_score: float = Field(..., ge=0, le=10)
    focus_score: float = Field(..., ge=0, le=10)
    financial_discipline_score: float = Field(..., ge=0, le=10)


class FounderReadinessResponse(BaseModel):
    score: float
    verdict: str
    recommendations: list[str]


class IntegrationStatusItem(BaseModel):
    integration: str
    mode: IntegrationMode
    connected: bool
    last_sync_at: str | None = None
    message: str


class IntegrationStatusResponse(BaseModel):
    items: list[IntegrationStatusItem]


class TheorySummaryResponse(BaseModel):
    count: int
    domains: dict[str, int]
    watermark: str


class HealthResponse(BaseModel):
    status: str
    service: str
    engine: str
    mode: str


class SocialCultureProfileRequest(BaseModel):
    cohort: str
    life_stage: str


class SocialCultureProfileResponse(BaseModel):
    cohort: str
    life_stage: str
    dominant_mindset: str
    interests: list[str]
    buying_style: str
    family_influence: str
    status_sensitivity: str
    embarrassment_triggers: list[str]
    trust_signals: list[str]
    preferred_channels: list[str]
    words_to_use: list[str]
    words_to_avoid: list[str]
    notes: list[str]


class GiftSocialFitRequest(BaseModel):
    cohort: str
    life_stage: str
    occasion: str
    price_band: str
    has_packaging: bool = False
    has_exchange_policy: bool = False
    has_social_proof: bool = False
    is_practical: bool = True
    looks_more_expensive_than_price: bool = False
    has_clear_use_case: bool = False


class GiftSocialFitResponse(BaseModel):
    score: float
    risk_level: str
    positioning_sentence: str
    blind_spots: list[str]
    recommendations: list[str]
    suggested_hooks: list[str]


class SocialCultureOptionsResponse(BaseModel):
    cohorts: list[str]
    life_stages: list[str]
    occasions: list[str]
    price_bands: list[str]
    blind_spot_checklist: list[str]
