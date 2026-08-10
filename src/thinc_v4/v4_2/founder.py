# -*- coding: utf-8 -*-
"""Founder OS layer.

THINC™ v4.2 — Invented by Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 Dr. Ehab Taha — Egy-Pioneers Academy.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List


@dataclass
class FounderOS:
    execution_score: float = 5.0
    discipline_score: float = 5.0
    learning_speed_score: float = 5.0
    resilience_score: float = 5.0
    focus_score: float = 5.0
    financial_discipline_score: float = 5.0

    def __post_init__(self) -> None:
        for name, value in asdict(self).items():
            if not 0 <= value <= 10:
                raise ValueError(f"{name} must be between 0 and 10")

    def founder_readiness(self) -> Dict[str, Any]:
        weights = {
            "execution_score": 0.25,
            "discipline_score": 0.20,
            "learning_speed_score": 0.15,
            "resilience_score": 0.15,
            "focus_score": 0.15,
            "financial_discipline_score": 0.10,
        }
        data = asdict(self)
        score = sum(data[k] * w for k, w in weights.items())
        if score >= 8:
            verdict = "جاهز للتوسع"
        elif score >= 6.5:
            verdict = "جاهز للاختبار مع متابعة"
        elif score >= 5:
            verdict = "يحتاج ضبط تنفيذ"
        else:
            verdict = "خطر تعثر مرتفع — ابدأ بخطة التزام قصيرة"
        return {"score": round(score, 2), "verdict": verdict}

    def coaching_recommendations(self) -> List[str]:
        data = asdict(self)
        tips: List[str] = []
        if data["execution_score"] < 6:
            tips.append("قسّم التنفيذ لمهام يومية صغيرة قابلة للقياس.")
        if data["discipline_score"] < 6:
            tips.append("استخدم متابعة أسبوعية وإلزام بتسليمات محددة.")
        if data["resilience_score"] < 6:
            tips.append("اعمل Reality Validation مبكرًا لتقليل الإحباط من النتائج الأولية.")
        if data["financial_discipline_score"] < 6:
            tips.append("لا تسمح للطالب بإطلاق حملة قبل فهم Break-even CPA.")
        return tips or ["المؤشرات جيدة؛ ركّز على التوسع التدريجي."]
