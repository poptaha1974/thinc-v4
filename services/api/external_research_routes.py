# -*- coding: utf-8 -*-
"""API routes for THINC External Social Research & Daily Intelligence."""
from __future__ import annotations

from enum import Enum

from datetime import date, datetime
from typing import Dict, List, TypeVar

from fastapi import APIRouter
from pydantic import BaseModel, Field

from thinc_v4.external_social_research import (
    CommercialImplication,
    DailyEgyptIntelligenceInput,
    DailyEgyptIntelligenceOutput,
    EgyptResearchDomain,
    EvidenceStrength,
    ExternalSocialResearchEngine,
    MarketImpact,
    ResearchObservation,
    ResearchSource,
    ResearchSourceType,
    SignalDirection,
)

router = APIRouter(prefix="/api/external-research", tags=["External Research"])


class ResearchSourceRequest(BaseModel):
    title: str
    source_name: str
    source_type: str
    url: str | None = None
    published_at: datetime | None = None
    retrieved_at: datetime | None = None
    author: str | None = None
    citation: str | None = None
    reliability_score: float = Field(5.0, ge=0, le=10)


class ResearchObservationRequest(BaseModel):
    domain: str
    summary: str
    evidence: str
    direction: str = SignalDirection.UNKNOWN.value
    evidence_strength: str = EvidenceStrength.MEDIUM.value
    market_impact: str = MarketImpact.MEDIUM.value
    commercial_implications: List[str] = Field(default_factory=list)
    affected_segments: List[str] = Field(default_factory=list)
    affected_categories: List[str] = Field(default_factory=list)
    source: ResearchSourceRequest | None = None


class DailyEgyptIntelligenceRequest(BaseModel):
    intelligence_date: date
    observations: List[ResearchObservationRequest]
    baseline_weights: Dict[str, float] = Field(default_factory=dict)


EnumT = TypeVar("EnumT", bound=Enum)


def _enum_from_value(enum_cls: type[EnumT], value: str) -> EnumT:
    for item in enum_cls:
        if value in {item.name, item.value}:
            return item
    valid = ", ".join([f"{item.name} / {item.value}" for item in enum_cls])
    raise ValueError(f"Invalid value '{value}'. Valid values: {valid}")


def _source(payload: ResearchSourceRequest | None) -> ResearchSource | None:
    if payload is None:
        return None
    return ResearchSource(
        title=payload.title,
        source_name=payload.source_name,
        source_type=_enum_from_value(ResearchSourceType, payload.source_type),
        url=payload.url,
        published_at=payload.published_at,
        retrieved_at=payload.retrieved_at,
        author=payload.author,
        citation=payload.citation,
        reliability_score=payload.reliability_score,
    )


@router.get("/options")
def external_research_options() -> dict[str, list[str] | dict[str, float]]:
    return {
        "source_types": [item.value for item in ResearchSourceType],
        "domains": [item.value for item in EgyptResearchDomain],
        "directions": [item.value for item in SignalDirection],
        "evidence_strengths": [item.value for item in EvidenceStrength],
        "market_impacts": [item.value for item in MarketImpact],
        "commercial_implications": [item.value for item in CommercialImplication],
        "default_weights": ExternalSocialResearchEngine.DEFAULT_WEIGHTS,
    }


@router.post("/daily-egypt-intelligence")
def evaluate_daily_egypt_intelligence(payload: DailyEgyptIntelligenceRequest) -> DailyEgyptIntelligenceOutput:
    observations = [
        ResearchObservation(
            domain=_enum_from_value(EgyptResearchDomain, obs.domain),
            summary=obs.summary,
            evidence=obs.evidence,
            direction=_enum_from_value(SignalDirection, obs.direction),
            evidence_strength=_enum_from_value(EvidenceStrength, obs.evidence_strength),
            market_impact=_enum_from_value(MarketImpact, obs.market_impact),
            commercial_implications=[_enum_from_value(CommercialImplication, item) for item in obs.commercial_implications],
            affected_segments=obs.affected_segments,
            affected_categories=obs.affected_categories,
            source=_source(obs.source),
        )
        for obs in payload.observations
    ]
    daily_input = DailyEgyptIntelligenceInput(
        intelligence_date=payload.intelligence_date,
        observations=observations,
        baseline_weights=payload.baseline_weights,
    )
    return ExternalSocialResearchEngine.evaluate_daily_intelligence(daily_input)
