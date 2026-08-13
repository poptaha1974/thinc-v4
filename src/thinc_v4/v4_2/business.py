# -*- coding: utf-8 -*-
"""Business architecture layer.

THINC™ v4.2 — Invented by Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 Dr. Ehab Taha — Egy-Pioneers Academy.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class BusinessArchitecture:
    revenue_model: str = "فرق سعر الجملة والتجزئة + Upsells + Repeat Purchase"
    fulfillment_model: str = "Academy-supported fulfillment: sourcing, storage, packaging, shipping, collection"
    offline_trust_point: str = "عنوان معرض/محل فعلي يزيد ثقة العميل ويغطي ضعف الأونلاين"
    required_sops: List[str] = field(default_factory=lambda: [
        "Product approval SOP",
        "Supplier onboarding SOP",
        "Creative production SOP",
        "Campaign launch SOP",
        "Order confirmation SOP",
        "Shipping & delivery SOP",
        "Returns and exchange SOP",
        "Student profit settlement SOP",
    ])
    risk_controls: List[str] = field(default_factory=lambda: [
        "لا إطلاق بدون حساب Unit Economics",
        "لا Scale بدون Delivered Orders",
        "Purchase Event لا يرسل إلا بعد التسليم والدفع",
        "توضيح مسؤوليات الطالب والأكاديمية في سياسة مكتوبة",
    ])

    def readiness_score(self) -> float:
        checks = [
            bool(self.revenue_model),
            bool(self.fulfillment_model),
            bool(self.offline_trust_point),
            len(self.required_sops) >= 6,
            len(self.risk_controls) >= 3,
        ]
        return round(sum(checks) / len(checks) * 10, 2)
