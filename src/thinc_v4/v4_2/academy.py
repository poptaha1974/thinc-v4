# -*- coding: utf-8 -*-
"""Academy operating system layer.

THINC™ v4.2 — Invented by Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 Dr. Ehab Taha — Egy-Pioneers Academy.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List
from .identity import PROGRAM_POSITIONING


@dataclass
class AcademyOperatingSystem:
    program_name: str = "THINC Commerce Builder System™"
    positioning: str = PROGRAM_POSITIONING
    workshops_weekly: bool = True
    club_name: str = "نادي تجار العرب | Merchants Arabia"
    ai_tools_access: bool = True
    medical_insurance_available: bool = True
    job_opportunity_for_top_students: bool = True
    offline_location_available: bool = True
    student_outputs: List[str] = field(default_factory=lambda: [
        "منتج مختار ومعتمد",
        "Persona كاملة",
        "عرض بيعي واضح",
        "كرياتيف إعلاني",
        "حملة اختبار",
        "تقرير Reality Validation",
        "قرار Kill/Fix/Scale",
        "خطة تحسين أو توسع",
    ])

    def value_stack_score(self) -> float:
        features = [
            self.workshops_weekly,
            bool(self.club_name),
            self.ai_tools_access,
            self.medical_insurance_available,
            self.job_opportunity_for_top_students,
            self.offline_location_available,
            len(self.student_outputs) >= 7,
        ]
        return round(sum(features) / len(features) * 10, 2)

    def public_summary(self) -> str:
        return (
            f"{self.program_name}\n"
            f"{self.positioning}\n\n"
            f"البرنامج لا يكتفي بالتعليم؛ بل يربط التدريب بالتطبيق والتشغيل والمجتمع. "
            f"يحصل الطالب على ورش أسبوعية للجادين، عضوية في {self.club_name}، "
            f"استفادة من أدوات AI وفق سياسة الاستخدام، دعم بمكان فعلي للثقة، "
            f"وفرص عمل أو تعاون للمتميزين."
        )
