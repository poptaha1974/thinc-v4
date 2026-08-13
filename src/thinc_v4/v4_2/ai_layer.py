# -*- coding: utf-8 -*-
"""AI operating layer.

THINC™ v4.2 — Invented by Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 Dr. Ehab Taha — Egy-Pioneers Academy.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class AITaskType(Enum):
    STRATEGY = "Strategy"
    RESEARCH = "Research"
    COPYWRITING = "Copywriting"
    DESIGN = "Design"
    VIDEO = "Video"
    VOICEOVER = "Voiceover"
    CODING = "Coding"
    ANALYTICS = "Analytics"
    AUTOMATION = "Automation"


@dataclass(frozen=True)
class AIToolSpec:
    name: str
    task_types: List[AITaskType]
    free_vs_paid_note: str
    best_for: str
    caution: str = "راجع شروط الاستخدام التجاري وحقوق الملكية قبل النشر."


class AIOperatingLayer:
    @staticmethod
    def default_tools() -> List[AIToolSpec]:
        T = AITaskType
        return [
            AIToolSpec("ChatGPT Plus/Pro", [T.STRATEGY, T.COPYWRITING, T.ANALYTICS, T.RESEARCH], "المدفوع أسرع وأقوى في الملفات والتحليل والسياق", "الاستراتيجية، صياغة الرسائل، تحليل البيانات"),
            AIToolSpec("Codex", [T.CODING, T.AUTOMATION, T.ANALYTICS], "مفيد جدًا في بناء الكود والاختبارات وإعادة الهيكلة", "تحويل THINC إلى منصة وأدوات تشغيل"),
            AIToolSpec("Claude", [T.RESEARCH, T.COPYWRITING, T.STRATEGY], "قوي في قراءة الملفات الطويلة والصياغة", "تحليل وثائق ومناهج طويلة"),
            AIToolSpec("Gemini", [T.RESEARCH, T.ANALYTICS, T.STRATEGY], "قوي في البحث والتكامل مع منظومة Google", "بحث وتلخيص وربط معلومات"),
            AIToolSpec("Canva Pro", [T.DESIGN], "المدفوع يفتح قوالب وعناصر Brand Kit وخصائص أقوى", "بوستات وسوشيال ميديا وبروشورات"),
            AIToolSpec("CapCut Pro", [T.VIDEO], "المدفوع يفتح مؤثرات وقوالب وخصائص تصدير أقوى", "Reels وTikTok Ads"),
            AIToolSpec("ElevenLabs", [T.VOICEOVER], "المدفوع يعطي جودة صوت واستخدام أكبر", "تعليق صوتي للإعلانات"),
            AIToolSpec("Freepik Premium/AI", [T.DESIGN, T.VIDEO], "المدفوع يعطي أصول أكثر وحقوق استخدام أوسع حسب الخطة", "صور منتجات، خلفيات، Mockups"),
            AIToolSpec("Looker Studio / Sheets", [T.ANALYTICS], "مجانية غالبًا لكن تحتاج إعداد جيد", "لوحات متابعة الحملة والطلاب"),
        ]

    @staticmethod
    def recommend_stack(task: AITaskType) -> List[AIToolSpec]:
        return [tool for tool in AIOperatingLayer.default_tools() if task in tool.task_types]

    @staticmethod
    def cost_saving_message(monthly_club_fee_egp: float, estimated_individual_cost_egp: float) -> str:
        if monthly_club_fee_egp <= 0:
            raise ValueError("Club fee must be > 0")
        saving = estimated_individual_cost_egp - monthly_club_fee_egp
        pct = saving / estimated_individual_cost_egp * 100 if estimated_individual_cost_egp else 0
        return (
            f"لو اشتركت في الأدوات منفردًا قد تدفع تقريبًا {estimated_individual_cost_egp:,.0f} جنيه شهريًا. "
            f"داخل النادي تدفع اشتراكًا رمزيًا {monthly_club_fee_egp:,.0f} جنيه وفق سياسة الاستخدام، "
            f"بفرق توفير تقريبي {saving:,.0f} جنيه ({pct:.1f}%)."
        )
