# -*- coding: utf-8 -*-
"""API routes for THINC Gift Decision Intelligence."""
from __future__ import annotations

from enum import Enum

from typing import Any, TypeVar

from fastapi import APIRouter
from pydantic import BaseModel, Field

from thinc_v4.egyptian_social_culture import GiftOccasion, PriceBand
from thinc_v4.gift_decision_intelligence import (
    BuyerRole,
    DeliveryUrgency,
    EgyptianGeoSegment,
    GiftDecisionInput,
    GiftDecisionIntelligenceEngine,
    GiftSafetyClass,
    ProductCategory,
    RecipientGenderContext,
    RelationshipContext,
    SeasonalityMoment,
    SocialClassSignal,
    GiftProductProfile,
)

router = APIRouter(prefix="/api/gift-intelligence", tags=["Gift Intelligence"])


class GiftProductProfileRequest(BaseModel):
    name: str = Field(..., min_length=1)
    category: str
    price_band: str
    safety_class: str
    perceived_value_score: float = Field(..., ge=0, le=10)
    practicality_score: float = Field(..., ge=0, le=10)
    packaging_score: float = Field(..., ge=0, le=10)
    trust_score: float = Field(..., ge=0, le=10)
    margin_score: float = Field(..., ge=0, le=10)
    stock_ready: bool = True


class GiftDecisionRequest(BaseModel):
    product: GiftProductProfileRequest
    occasion: str
    relationship: str
    recipient_gender: str
    geo_segment: str = EgyptianGeoSegment.MIXED_NATIONAL.value
    social_class_signal: str = SocialClassSignal.MIDDLE_MAINSTREAM.value
    buyer_role: str = BuyerRole.BUYER.value
    seasonality: str = SeasonalityMoment.ALWAYS_ON.value
    delivery_urgency: str = DeliveryUrgency.TWO_TO_THREE_DAYS.value
    has_exchange_policy: bool = False
    has_real_photos: bool = False
    has_reviews: bool = False
    can_personalize: bool = False
    buyer_knows_recipient_taste: bool = False


class GiftDecisionResponse(BaseModel):
    score: float
    risk_level: str
    product_occasion_fit: float
    safety_verdict: str
    positioning: str
    recommended_angle: str
    blind_spots: list[str]
    recommendations: list[str]
    objections: list[str]
    whatsapp_replies: list[str]
    crm_followups: list[str]
    next_best_actions: list[str]


EnumT = TypeVar("EnumT", bound=Enum)


def _enum_from_value(enum_cls: type[EnumT], value: str) -> EnumT:
    for item in enum_cls:
        if value in {item.name, item.value}:
            return item
    valid = ", ".join([f"{item.name} / {item.value}" for item in enum_cls])
    raise ValueError(f"Invalid value '{value}'. Valid values: {valid}")


@router.get("/options")
def gift_intelligence_options() -> dict[str, list[str]]:
    options = GiftDecisionIntelligenceEngine.options()
    options.update(
        {
            "occasions": [item.value for item in GiftOccasion],
            "price_bands": [item.value for item in PriceBand],
            "completeness_checklist": GiftDecisionIntelligenceEngine.completeness_checklist(),
        }
    )
    return options


@router.post("/evaluate", response_model=GiftDecisionResponse)
def evaluate_gift_decision(payload: GiftDecisionRequest) -> GiftDecisionResponse:
    product = GiftProductProfile(
        name=payload.product.name,
        category=_enum_from_value(ProductCategory, payload.product.category),
        price_band=_enum_from_value(PriceBand, payload.product.price_band),
        safety_class=_enum_from_value(GiftSafetyClass, payload.product.safety_class),
        perceived_value_score=payload.product.perceived_value_score,
        practicality_score=payload.product.practicality_score,
        packaging_score=payload.product.packaging_score,
        trust_score=payload.product.trust_score,
        margin_score=payload.product.margin_score,
        stock_ready=payload.product.stock_ready,
    )
    decision_input = GiftDecisionInput(
        product=product,
        occasion=_enum_from_value(GiftOccasion, payload.occasion),
        relationship=_enum_from_value(RelationshipContext, payload.relationship),
        recipient_gender=_enum_from_value(RecipientGenderContext, payload.recipient_gender),
        geo_segment=_enum_from_value(EgyptianGeoSegment, payload.geo_segment),
        social_class_signal=_enum_from_value(SocialClassSignal, payload.social_class_signal),
        buyer_role=_enum_from_value(BuyerRole, payload.buyer_role),
        seasonality=_enum_from_value(SeasonalityMoment, payload.seasonality),
        delivery_urgency=_enum_from_value(DeliveryUrgency, payload.delivery_urgency),
        has_exchange_policy=payload.has_exchange_policy,
        has_real_photos=payload.has_real_photos,
        has_reviews=payload.has_reviews,
        can_personalize=payload.can_personalize,
        buyer_knows_recipient_taste=payload.buyer_knows_recipient_taste,
    )
    result = GiftDecisionIntelligenceEngine.evaluate(decision_input)
    return GiftDecisionResponse(
        score=result.score,
        risk_level=result.risk_level.value,
        product_occasion_fit=result.product_occasion_fit,
        safety_verdict=result.safety_verdict,
        positioning=result.positioning,
        recommended_angle=result.recommended_angle,
        blind_spots=result.blind_spots,
        recommendations=result.recommendations,
        objections=result.objections,
        whatsapp_replies=result.whatsapp_replies,
        crm_followups=result.crm_followups,
        next_best_actions=result.next_best_actions,
    )
