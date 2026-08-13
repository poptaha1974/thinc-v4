# -*- coding: utf-8 -*-
"""Competitive intelligence layer.

THINC™ v4.2 — Invented by Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 Dr. Ehab Taha — Egy-Pioneers Academy.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List
from .identity import PROGRAM_POSITIONING


@dataclass
class CompetitorProfile:
    name: str
    positioning: str = ""
    price_range: str = ""
    offer_strength: float = 5.0
    creative_strength: float = 5.0
    trust_strength: float = 5.0
    operational_strength: float = 5.0
    weakness: str = ""

    def __post_init__(self) -> None:
        for name in ["offer_strength", "creative_strength", "trust_strength", "operational_strength"]:
            val = getattr(self, name)
            if not 0 <= val <= 10:
                raise ValueError(f"{name} must be between 0 and 10")


@dataclass
class CompetitiveIntelligence:
    competitors: List[CompetitorProfile] = field(default_factory=list)
    market_gap: str = ""
    recommended_positioning: str = PROGRAM_POSITIONING

    def average_competitor_strength(self) -> float:
        if not self.competitors:
            return 0.0
        scores = []
        for c in self.competitors:
            scores.append((c.offer_strength + c.creative_strength + c.trust_strength + c.operational_strength) / 4)
        return round(sum(scores) / len(scores), 2)

    def differentiation_score(self) -> float:
        if not self.competitors:
            return 7.0
        unique_assets = 0
        text = (self.market_gap + " " + self.recommended_positioning).lower()
        for kw in ["مدعوم", "تشغيل", "مكان فعلي", "أول عملية بيع", "نادي", "ai", "ذكاء"]:
            if kw.lower() in text:
                unique_assets += 1
        base = 5 + unique_assets * 0.8 - max(0, self.average_competitor_strength() - 7) * 0.5
        return round(max(1, min(10, base)), 2)
