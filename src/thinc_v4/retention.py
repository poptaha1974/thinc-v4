# -*- coding: utf-8 -*-
"""THINC v4.1 — Cohort Retention Engine (Phase 6 of the calibration plan).

مقياسان منفصلان:
1) احتفاظ الطلاب: استمرارية التنفيذ عبر شهور البرنامج (من Outcome Log).
2) احتفاظ عملاء مشاريع الطلاب: إعادة الشراء (Repeat Purchase) لكل مشروع.

قاعدة القرار: منتج قابل للتكرار لا يأخذ قرار Scale بدون بيانات إعادة شراء.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 Dr. Ehab Taha — Egy-Pioneers Academy. All rights reserved.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List

from .outcomes import OutcomeRegistry


@dataclass(frozen=True)
class RepeatPurchaseSnapshot:
    """لقطة إعادة شراء لمشروع طالب واحد خلال فترة."""

    prediction_id: str
    period_label: str  # مثال: "month_1"
    unique_customers: int
    returning_customers: int

    def __post_init__(self) -> None:
        if self.unique_customers < 0 or self.returning_customers < 0:
            raise ValueError("Customer counts must be >= 0")
        if self.returning_customers > self.unique_customers:
            raise ValueError("Returning customers cannot exceed unique customers")

    @property
    def repeat_rate(self) -> float:
        if self.unique_customers == 0:
            return 0.0
        return round(self.returning_customers / self.unique_customers, 3)


class RetentionEngine:
    """يحسب منحنيات الاحتفاظ لكل دفعة من سجل النتائج."""

    def __init__(self, registry: OutcomeRegistry):
        self.registry = registry

    def student_retention_by_cohort(self) -> Dict[str, Dict[str, Any]]:
        """نسبة الطلاب النشطين لكل دفعة عند كل نافذة قياس (30/60/90)."""
        cohort_of: Dict[str, str] = {
            p["prediction_id"]: p["cohort_id"] for p in self.registry.predictions()
        }
        buckets: Dict[str, Dict[int, List[bool]]] = defaultdict(lambda: defaultdict(list))
        for o in self.registry.outcomes():
            cohort = cohort_of.get(o["prediction_id"], "unknown")
            active = str(o["student_still_active"]).strip().lower() == "true"
            buckets[cohort][int(o["window_days"])].append(active)

        report: Dict[str, Dict[str, Any]] = {}
        for cohort, windows in sorted(buckets.items()):
            curve = {}
            for window in sorted(windows):
                values = windows[window]
                curve[f"day_{window}"] = {
                    "n": len(values),
                    "active_rate": round(sum(values) / len(values), 3),
                }
            report[cohort] = curve
        return report

    @staticmethod
    def project_repeat_purchase(snapshots: List[RepeatPurchaseSnapshot]) -> Dict[str, Any]:
        """ملخص إعادة الشراء لمشروع واحد عبر الفترات."""
        if not snapshots:
            return {"periods": {}, "overall_repeat_rate": 0.0, "scale_gate_open": False}
        periods = {
            s.period_label: {
                "unique_customers": s.unique_customers,
                "returning_customers": s.returning_customers,
                "repeat_rate": s.repeat_rate,
            }
            for s in snapshots
        }
        total_unique = sum(s.unique_customers for s in snapshots)
        total_returning = sum(s.returning_customers for s in snapshots)
        overall = round(total_returning / total_unique, 3) if total_unique else 0.0
        return {
            "periods": periods,
            "overall_repeat_rate": overall,
            # بوابة القرار: Scale لمنتج متكرر يتطلب بيانات إعادة شراء فعلية
            "scale_gate_open": total_unique >= 30 and overall > 0,
        }

    @staticmethod
    def scale_decision_gate(
        is_repeatable_product: bool,
        repeat_summary: Dict[str, Any],
    ) -> Dict[str, Any]:
        """قاعدة v4.1: قرار Scale يشترط بيانات إعادة شراء للمنتجات القابلة للتكرار."""
        if not is_repeatable_product:
            return {"scale_allowed": True, "reason": "منتج غير متكرر — بوابة إعادة الشراء لا تنطبق."}
        if repeat_summary.get("scale_gate_open"):
            return {
                "scale_allowed": True,
                "reason": f"إعادة شراء موثقة بمعدل {repeat_summary['overall_repeat_rate']:.1%}.",
            }
        return {
            "scale_allowed": False,
            "reason": "منتج قابل للتكرار بدون بيانات إعادة شراء كافية (≥30 عميل) — اجمع بيانات قبل التوسع.",
        }
