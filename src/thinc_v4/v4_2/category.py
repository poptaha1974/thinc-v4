# -*- coding: utf-8 -*-
"""Category design layer.

THINC™ v4.2 — Invented by Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 Dr. Ehab Taha — Egy-Pioneers Academy.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List
from .identity import PROGRAM_POSITIONING


@dataclass
class CategoryDesign:
    old_category: str = "كورس تجارة إلكترونية / كورس دروبشيبينج"
    new_category: str = "برنامج بناء مشروع تجارة إلكترونية مدعوم بالكامل"
    enemy: str = "الكورسات النظرية التي تبيع معلومات بدون تشغيل حقيقي"
    point_of_view: str = (
        "المشكلة ليست نقص المعلومات، بل غياب بيئة التشغيل التي تحول التعلم إلى بيع حقيقي."
    )
    category_promise: str = PROGRAM_POSITIONING
    category_proof: List[str] = field(default_factory=lambda: [
        "منتجات وموردين",
        "تخزين وشحن وتحصيل",
        "مكان فعلي للثقة",
        "فريق دعم من خريجي الأكاديمية",
        "ورش أسبوعية للجادين",
        "نادي تجار العرب",
        "أدوات ذكاء اصطناعي مدفوعة باشتراك رمزي",
    ])

    def category_strength(self) -> float:
        proof = len([p for p in self.category_proof if p.strip()])
        score = 4 + min(proof, 8) * 0.65
        if "مدعوم" in self.new_category:
            score += 0.8
        if "تشغيل" in self.point_of_view:
            score += 0.8
        return round(min(10, score), 2)
