# -*- coding: utf-8 -*-
"""API routes for THINC Adaptive Market Learning."""
from __future__ import annotations

from enum import Enum

from typing import Dict, List, TypeVar

from fastapi import APIRouter
from pydantic import BaseModel, Field

from thinc_v4.adaptive_market_learning import (
    ActualOutcomeSnapshot,
    AdaptiveMarketLearningEngine,
    LearningInput,
    LearningOutput,
    LearningSeverity,
    MarketSignal,
    MarketSignalType,
    PredictionSnapshot,
)

router = APIRouter(prefix="/api/adaptive-learning", tags=["Adaptive Learning"])


class PredictionSnapshotRequest(BaseModel):
    expected_score: float = Field(..., ge=0, le=10)
    expected_real_cpa: float | None = Field(None, ge=0)
    expected_conversion_rate: float | None = Field(None, ge=0)
    expected_delivery_rate: float | None = Field(None, ge=0)
    expected_net_profit: float | None = None
    expected_objections: List[str] = Field(default_factory=list)


class ActualOutcomeSnapshotRequest(BaseModel):
    actual_score: float | None = Field(None, ge=0, le=10)
    actual_real_cpa: float | None = Field(None, ge=0)
    actual_conversion_rate: float | None = Field(None, ge=0)
    actual_delivery_rate: float | None = Field(None, ge=0)
    actual_net_profit: float | None = None
    observed_objections: List[str] = Field(default_factory=list)
    comments_sentiment: str | None = None
    repeat_purchase_rate: float | None = Field(None, ge=0)
    refund_or_return_rate: float | None = Field(None, ge=0)


class MarketSignalRequest(BaseModel):
    signal_type: str
    description: str
    evidence: str
    severity: str = LearningSeverity.MEDIUM.value
    affected_layer: str = "general"
    suggested_shift: str = "unknown"


class LearningRequest(BaseModel):
    context_name: str
    prediction: PredictionSnapshotRequest
    actual: ActualOutcomeSnapshotRequest
    signals: List[MarketSignalRequest] = Field(default_factory=list)
    current_weights: Dict[str, float] = Field(default_factory=dict)


EnumT = TypeVar("EnumT", bound=Enum)


def _enum_from_value(enum_cls: type[EnumT], value: str) -> EnumT:
    for item in enum_cls:
        if value in {item.name, item.value}:
            return item
    valid = ", ".join([f"{item.name} / {item.value}" for item in enum_cls])
    raise ValueError(f"Invalid value '{value}'. Valid values: {valid}")


@router.get("/options")
def adaptive_learning_options() -> dict[str, list[str] | dict[str, float]]:
    return {
        "signal_types": [item.value for item in MarketSignalType],
        "severities": [item.value for item in LearningSeverity],
        "default_weights": AdaptiveMarketLearningEngine.DEFAULT_WEIGHTS,
    }


@router.post("/evaluate")
def evaluate_learning(payload: LearningRequest) -> LearningOutput:
    prediction = PredictionSnapshot(
        expected_score=payload.prediction.expected_score,
        expected_real_cpa=payload.prediction.expected_real_cpa,
        expected_conversion_rate=payload.prediction.expected_conversion_rate,
        expected_delivery_rate=payload.prediction.expected_delivery_rate,
        expected_net_profit=payload.prediction.expected_net_profit,
        expected_objections=payload.prediction.expected_objections,
    )
    actual = ActualOutcomeSnapshot(
        actual_score=payload.actual.actual_score,
        actual_real_cpa=payload.actual.actual_real_cpa,
        actual_conversion_rate=payload.actual.actual_conversion_rate,
        actual_delivery_rate=payload.actual.actual_delivery_rate,
        actual_net_profit=payload.actual.actual_net_profit,
        observed_objections=payload.actual.observed_objections,
        comments_sentiment=payload.actual.comments_sentiment,
        repeat_purchase_rate=payload.actual.repeat_purchase_rate,
        refund_or_return_rate=payload.actual.refund_or_return_rate,
    )
    signals = [
        MarketSignal(
            signal_type=_enum_from_value(MarketSignalType, signal.signal_type),
            description=signal.description,
            evidence=signal.evidence,
            severity=_enum_from_value(LearningSeverity, signal.severity),
            affected_layer=signal.affected_layer,
        )
        for signal in payload.signals
    ]
    learning_input = LearningInput(
        context_name=payload.context_name,
        prediction=prediction,
        actual=actual,
        signals=signals,
        current_weights=payload.current_weights,
    )
    return AdaptiveMarketLearningEngine.evaluate_learning(learning_input)
