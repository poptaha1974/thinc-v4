# -*- coding: utf-8 -*-
"""Egyptianization and generational language engine.

THINC™ v4.2 — Invented by Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 Dr. Ehab Taha — Egy-Pioneers Academy.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List
from .identity import PROGRAM_POSITIONING


class EgyptianAudienceGeneration(Enum):
    GEN_X = "Gen X Egyptian — 1965-1980"
    MILLENNIAL = "Millennial Egyptian — 1981-1996"
    GEN_Z = "Gen Z Egyptian — 1997-2012"
    MIXED = "Mixed Egyptian Audience"


class AudienceSkillLevel(Enum):
    BEGINNER = "مبتدئ"
    EXPERIENCED_COURSE_BUYER = "جرّب كورسات قبل كده"
    WORKING_PRACTITIONER = "شغال بالفعل في المجال"
    ADVANCED = "محترف"


@dataclass
class EgyptianLanguageProfile:
    generation: EgyptianAudienceGeneration
    skill_level: AudienceSkillLevel
    tone: str
    preferred_words: List[str]
    avoided_words: List[str]
    trust_builders: List[str]
    pain_words: List[str]
    aspiration_words: List[str]
    sample_hook: str


class EgyptianizationEngine:
    """Turns scientific outputs into Egyptian Arabic adapted by generation and skill level."""

    @staticmethod
    def build_profile(
        generation: EgyptianAudienceGeneration,
        skill_level: AudienceSkillLevel,
    ) -> EgyptianLanguageProfile:
        base: Dict[str, Any] = {
            EgyptianAudienceGeneration.GEN_Z: {
                "tone": "سريع، مباشر، بصري، بدون تنظير",
                "preferred": ["فلوس", "شغل حقيقي", "مش كلام", "تجربة", "سكيل", "تبدأ صح", "تاخد خطوة"],
                "avoided": ["محاضرات أكاديمية طويلة", "نظريات معقدة", "شهادة فقط"],
                "pain": ["تايه", "مش عارف تبدأ", "خايف تضيع فلوس", "كل حاجة على النت متلخبطة"],
                "aspiration": ["أول ربح", "دخل من الموبايل", "مشروعك", "تشتغل بإيدك"],
                "hook": "بدل ما تتفرج على فيديوهات طول السنة… ادخل تجربة تبيع فيها بجد وإنت لسه بتتعلم.",
            },
            EgyptianAudienceGeneration.MILLENNIAL: {
                "tone": "عملي، مطمئن، يركز على الدخل وتقليل المخاطرة",
                "preferred": ["دخل إضافي", "أمان", "نظام", "خطوة بخطوة", "أقل مخاطرة", "مشروع حقيقي"],
                "avoided": ["ثراء سريع", "وعود مبالغ فيها", "كلام تحفيزي فارغ"],
                "pain": ["محتاج تزود دخلك", "خايف تجرب لوحدك", "جربت كورسات ومطبقتش"],
                "aspiration": ["دخل مستقر", "مشروع جانبي", "أول عملية بيع", "نظام يمشيك"],
                "hook": "لو جربت تتعلم قبل كده وموقفتش عند أول خطوة تنفيذ… البرنامج ده معمول علشان يحول المعرفة لشغل حقيقي.",
            },
            EgyptianAudienceGeneration.GEN_X: {
                "tone": "رصين، موثوق، يركز على الأمان والسمعة",
                "preferred": ["مصدر دخل", "أمان", "ثقة", "مكان فعلي", "نظام واضح", "إشراف متخصص"],
                "avoided": ["تريند", "هوجة", "مغامرة غير محسوبة"],
                "pain": ["خايف من المخاطرة", "عايز حاجة مضمونة أكتر", "مش واثق في الأونلاين وحده"],
                "aspiration": ["مشروع محترم", "دخل إضافي آمن", "ثقة العملاء", "استمرارية"],
                "hook": "ابدأ تجارة إلكترونية بنظام واضح، دعم فعلي، ومكان حقيقي يزود ثقة العملاء فيك.",
            },
            EgyptianAudienceGeneration.MIXED: {
                "tone": "واضح، بسيط، يجمع بين الأمان والنتيجة",
                "preferred": ["مشروع حقيقي", "تطبيق عملي", "دعم كامل", "أول عملية بيع", "أقل مخاطرة"],
                "avoided": ["وعود خيالية", "كلام نظري", "مصطلحات صعبة"],
                "pain": ["تايه", "خايف تخسر", "اتعلمت كتير ومطبقتش"],
                "aspiration": ["تتعلم وتطبق وتبيع", "تبني مشروع", "تشوف نتيجة"],
                "hook": "مش كورس نظري… ده برنامج يبني معاك مشروع تجارة إلكترونية من أول فكرة لأول عملية بيع.",
            },
        }[generation]

        skill_modifiers: Dict[str, Any] = {
            AudienceSkillLevel.BEGINNER: {
                "trust": ["شرح من الصفر", "خطوات واضحة", "مفيش خبرة مطلوبة", "حد ماسك إيدك"],
                "extra": ["ببساطة", "من غير تعقيد"],
            },
            AudienceSkillLevel.EXPERIENCED_COURSE_BUYER: {
                "trust": ["تطبيق حقيقي", "مش محتوى مسجل وخلاص", "متابعة تنفيذ", "نتائج قابلة للقياس"],
                "extra": ["مش معلومات زيادة", "تنفيذ فعلي"],
            },
            AudienceSkillLevel.WORKING_PRACTITIONER: {
                "trust": ["تحليل حملات", "تحسين CPA", "قرار Kill/Fix/Scale", "نظام توسع"],
                "extra": ["تحسين الأداء", "توسيع محسوب"],
            },
            AudienceSkillLevel.ADVANCED: {
                "trust": ["Framework قابل للتكرار", "Decision Engine", "Reality Validation", "Unit Economics"],
                "extra": ["نظام تشغيل", "منهجية قابلة للتوسع"],
            },
        }[skill_level]

        return EgyptianLanguageProfile(
            generation=generation,
            skill_level=skill_level,
            tone=base["tone"],
            preferred_words=base["preferred"] + skill_modifiers["extra"],
            avoided_words=base["avoided"],
            trust_builders=skill_modifiers["trust"],
            pain_words=base["pain"],
            aspiration_words=base["aspiration"],
            sample_hook=base["hook"],
        )

    @staticmethod
    def generate_offer_message(profile: EgyptianLanguageProfile) -> str:
        words = ", ".join(profile.preferred_words[:5])
        trust = ", ".join(profile.trust_builders[:4])
        pains = ", ".join(profile.pain_words[:3])
        aspirations = ", ".join(profile.aspiration_words[:3])
        return (
            f"{profile.sample_hook}\n\n"
            f"لو أنت {profile.skill_level.value} وبتواجه: {pains}، "
            f"فبرنامج \"{PROGRAM_POSITIONING}\" بيشتغل معاك بنظام واضح: {trust}.\n\n"
            f"النتيجة اللي بنبنيها معاك: {aspirations}.\n"
            f"المفردات المناسبة للجمهور ده: {words}."
        )
