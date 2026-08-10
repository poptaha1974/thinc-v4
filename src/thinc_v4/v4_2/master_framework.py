# -*- coding: utf-8 -*-
"""
THINC™ v4.2 — Adaptive Commerce Intelligence & Venture Building System
نظام طه المتكيف للذكاء التجاري وبناء المشاريع

© 2026 الدكتور إيهاب طه — EgyPioneers / Egy-Pioneers Academy

هذا الملف يمثل طبقة v4.2 فوق THINC v3.1.
- يحتفظ بمحركات v3.1: Persona, CNCR, Profit, Reality Validation, Decision Engine.
- يضيف طبقات v4.0: Scientific Theory Registry, Egyptianization, Business Architecture,
  Competitive Intelligence, Category Design, Founder OS, AI Operating Layer,
  Academy Operating System, Creative Intelligence & Experimental Advertising,
  Media Test Protocol Engine.

تشغيل الاختبارات:
    python -m thinc_v4.v4_2.master_framework --test

تشغيل مثال:
    python -m thinc_v4.v4_2.master_framework --example
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .market_signals import (
    AutomatedProvider,
    CollectionMethod,
    DecisionStage,
    EvidenceStatus as MarketEvidenceStatus,
    GateDecision,
    MarketSignalEvidence,
    MarketSignalGateResult,
    MarketSignalSource,
    MarketSignalTriangulationEngine,
)

# =============================================================================
# Compatibility with THINC v3.1
# =============================================================================

APP_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = APP_DIR.parent
REPO_ROOT = PACKAGE_DIR.parents[1]
LEGACY_DIR = REPO_ROOT / "thinc_v4_0_final_verified_20260620" / "thinc_v4_final"
for import_dir in (APP_DIR, REPO_ROOT, LEGACY_DIR):
    if import_dir.exists() and str(import_dir) not in sys.path:
        sys.path.insert(0, str(import_dir))

_V3_IMPORT_ERROR: Exception | None = None
try:  # preferred if the canonical name exists
    from THINC_v3_1_Master_Framework import (
        CampaignPerformanceData,
        CNCROverlay,
        CompositeScoreV3,
        DecisionEngine,
        GoldenEquation,
        HooksEngine,
        HookType,
        IntegratedPersona,
        Neurochemical,
        PersonaLayer,
        ProfitIntelligence,
        RealityValidationTest,
        TahaIndex,
        UnitEconomics,
        get_watermark as get_v3_watermark,
        run_all_tests as run_v3_tests,
    )
except Exception:  # fallback to the uploaded filename
    try:
        from THINC_v3_1_Master_Framework_Chatgpt import (
            CampaignPerformanceData,
            CNCROverlay,
            CompositeScoreV3,
            DecisionEngine,
            GoldenEquation,
            HooksEngine,
            HookType,
            IntegratedPersona,
            Neurochemical,
            PersonaLayer,
            ProfitIntelligence,
            RealityValidationTest,
            TahaIndex,
            UnitEconomics,
            get_watermark as get_v3_watermark,
            run_all_tests as run_v3_tests,
        )
    except Exception as err2:  # pragma: no cover
        _V3_IMPORT_ERROR = err2


# =============================================================================
# SECTION 0 · IDENTITY
# =============================================================================

FRAMEWORK_NAME = "THINC"
FRAMEWORK_VERSION = "v4.2 — Creative Intelligence, Media Testing & Scale Protocol Edition"
FRAMEWORK_FULL_NAME = "Taha's Holistic Integration of Needs & Consumer behavior"
AUTHOR_NAME_AR = "الدكتور إيهاب طه"
AUTHOR_NAME_EN = "Dr. Ehab Taha"
TRADEMARK_HOLDER = "EgyPioneers — طلائع شباب مصر"
ACADEMY_NAME = "Egy-Pioneers Academy / Insta Learn Academy"
PROGRAM_POSITIONING = "ابنِ مشروع تجارة إلكترونية مدعوم بالكامل من أول فكرة إلى أول عملية بيع."
COPYRIGHT_YEAR = 2026


def compute_identity_hash() -> str:
    identity_string = (
        f"{FRAMEWORK_NAME}|{FRAMEWORK_VERSION}|{FRAMEWORK_FULL_NAME}|"
        f"{AUTHOR_NAME_EN}|{TRADEMARK_HOLDER}|{PROGRAM_POSITIONING}|{COPYRIGHT_YEAR}"
    )
    return hashlib.sha256(identity_string.encode("utf-8")).hexdigest()


def verify_attribution() -> bool:
    return (
        AUTHOR_NAME_AR == "الدكتور إيهاب طه"
        and AUTHOR_NAME_EN == "Dr. Ehab Taha"
        and FRAMEWORK_NAME == "THINC"
        and FRAMEWORK_FULL_NAME.startswith("Taha's")
    )


def get_watermark() -> str:
    return (
        f"\n💎 {FRAMEWORK_NAME}™ {FRAMEWORK_VERSION.split('—')[0].strip()} — "
        f"© {COPYRIGHT_YEAR} {AUTHOR_NAME_AR} — {TRADEMARK_HOLDER}\n"
        f"   {ACADEMY_NAME}\n"
        f"   Positioning: {PROGRAM_POSITIONING}\n"
        f"   Identity Hash: {compute_identity_hash()[:16]}..."
    )


def enforce_watermark(text: str) -> str:
    if not verify_attribution():
        raise RuntimeError("Identity Protection Violated — THINC attribution was modified.")
    return text.rstrip() + "\n" + get_watermark()


# =============================================================================
# SECTION 1 · SCIENTIFIC THEORY REGISTRY
# =============================================================================

class TheoryDomain(Enum):
    BEHAVIORAL_ECONOMICS = "Behavioral Economics"
    COGNITIVE_PSYCHOLOGY = "Cognitive Psychology"
    SOCIAL_PSYCHOLOGY = "Social Psychology"
    MARKETING_STRATEGY = "Marketing Strategy"
    BRANDING = "Branding & Positioning"
    DECISION_SCIENCE = "Decision Science"
    CONSUMER_BEHAVIOR = "Consumer Behavior"
    NEUROECONOMICS = "Neuroeconomics"
    AI_SYSTEMS = "AI Systems"
    ENTREPRENEURSHIP = "Entrepreneurship"
    OPERATIONS = "Operations & Unit Economics"
    LOCAL_CULTURE = "Egyptian/Arab Cultural Lens"


class EvidenceLevel(Enum):
    ACADEMIC_CORE = "A — Foundational academic theory"
    META_REVIEWED = "B — Meta-reviewed / strongly replicated"
    INDUSTRY_VALIDATED = "C — Industry validated"
    LOCAL_FIELD_TESTED = "D — Local field-tested"
    HEURISTIC = "E — Useful heuristic / must be tested"


class UpdateCadence(Enum):
    STABLE = "Stable — review yearly"
    QUARTERLY = "Quarterly — update every 3 months"
    MONTHLY = "Monthly — update monthly"
    WEEKLY = "Weekly — update weekly"
    LIVE = "Live — update via API/search when enabled"


@dataclass(frozen=True)
class ScientificTheory:
    id: str
    name_en: str
    name_ar: str
    domain: TheoryDomain
    evidence_level: EvidenceLevel
    purpose_in_thinc: str
    applied_to: List[str]
    update_cadence: UpdateCadence = UpdateCadence.STABLE
    egyptianization_note: str = "يتم تكييفها لغويًا وسلوكيًا حسب السوق المصري والعربي."
    caution: str = "تستخدم كإطار قرار واحتمال، وليس كحقيقة حتمية."


class ScientificTheoryRegistry:
    """Registry for the scientific and strategic theories behind THINC v4.0."""

    @staticmethod
    def default_theories() -> List[ScientificTheory]:
        T = ScientificTheory
        D = TheoryDomain
        E = EvidenceLevel
        U = UpdateCadence
        return [
            T("maslow", "Maslow's Hierarchy of Needs", "هرم ماسلو للاحتياجات", D.COGNITIVE_PSYCHOLOGY, E.ACADEMIC_CORE, "تحديد الاحتياج الإنساني المسيطر وراء الشراء", ["Persona", "Offer", "Message"]),
            T("jtbd", "Jobs To Be Done", "المهام المطلوب إنجازها", D.MARKETING_STRATEGY, E.INDUSTRY_VALIDATED, "فهم الوظيفة الوظيفية والعاطفية والاجتماعية للمنتج", ["Product", "Offer", "Positioning"]),
            T("prospect", "Prospect Theory", "نظرية الاحتمالات السلوكية", D.BEHAVIORAL_ECONOMICS, E.META_REVIEWED, "فهم نفور الخسارة وتقييم المخاطر", ["Offer", "Pricing", "Objections"]),
            T(
                "loss_aversion", "Loss Aversion", "تجنب الخسارة", D.BEHAVIORAL_ECONOMICS, E.META_REVIEWED,
                "صياغة المخاطر والضمانات", ["Hooks", "Guarantee", "CTA"],
                egyptianization_note="في مصر تُصاغ كرسالة أمان: ادفع عند الاستلام، جرّب من غير مخاطرة، وفلوسك محفوظة لو طبّقت ومحققتش استفادة.",
            ),
            T("framing", "Framing Effect", "تأثير التأطير", D.COGNITIVE_PSYCHOLOGY, E.META_REVIEWED, "تغيير إدراك القيمة حسب طريقة العرض", ["Copywriting", "Pricing"]),
            T(
                "anchoring", "Anchoring Bias", "تحيز المرساة السعرية", D.COGNITIVE_PSYCHOLOGY, E.META_REVIEWED,
                "بناء السعر المرجعي والخصم", ["Pricing", "Landing Page"],
                egyptianization_note="في التسعير المصري تُستخدم مرساة واضحة: السعر الأصلي 6500، وسعر البرنامج 2900 مع توضيح القيمة التشغيلية وراء الفرق.",
            ),
            T(
                "scarcity", "Scarcity Principle", "مبدأ الندرة", D.SOCIAL_PSYCHOLOGY, E.INDUSTRY_VALIDATED,
                "رفع أولوية القرار عند ندرة الكمية/الفرصة", ["Offer", "Hooks"],
                egyptianization_note="تُستخدم بوضوح وصدق: العدد محدود لأن كل طالب له متابعة وتشغيل ودعم، مش ندرة مصطنعة.",
            ),
            T(
                "social_proof", "Social Proof", "الإثبات الاجتماعي", D.SOCIAL_PSYCHOLOGY, E.META_REVIEWED,
                "بناء الثقة عبر تجارب الآخرين", ["Trust", "Creative", "Landing Page"],
                egyptianization_note="مصريًا يُترجم إلى: شوف دفعات قبل كده، خريجين بيشتغلوا، نتائج طلاب، ومكان فعلي تقدر تزوره.",
            ),
            T(
                "authority", "Authority Principle", "مبدأ السلطة والخبرة", D.SOCIAL_PSYCHOLOGY, E.META_REVIEWED,
                "رفع الثقة في الأكاديمية والمحاضر", ["Brand", "Sales"],
                egyptianization_note="تُبنى عبر خبرة د. إيهاب طه، لجنة اعتماد المنتجات، أمثلة سوق محلية، ومنهج THINC الموثق داخل الأكاديمية.",
            ),
            T("reciprocity", "Reciprocity", "المعاملة بالمثل", D.SOCIAL_PSYCHOLOGY, E.META_REVIEWED, "رفع التحويل عبر قيمة مجانية مسبقة", ["Lead Magnet", "Nurture"]),
            T("commitment", "Commitment & Consistency", "الالتزام والاتساق", D.SOCIAL_PSYCHOLOGY, E.META_REVIEWED, "تحويل النية إلى فعل تدريجي", ["Follow-up", "Community"]),
            T("liking", "Liking Principle", "مبدأ الألفة والإعجاب", D.SOCIAL_PSYCHOLOGY, E.META_REVIEWED, "جعل الرسالة قريبة من مفردات الجمهور", ["Dialect", "Creative"]),
            T("nudge", "Nudge Theory", "نظرية الدفع السلوكي", D.BEHAVIORAL_ECONOMICS, E.INDUSTRY_VALIDATED, "تصميم اختيارات تسهل القرار", ["UX", "Checkout", "Enrollment"]),
            T(
                "fogg_behavior", "Fogg Behavior Model", "نموذج فوج للسلوك", D.CONSUMER_BEHAVIOR, E.INDUSTRY_VALIDATED,
                "تحليل السلوك باعتباره نتيجة تقاطع الدافع والقدرة والمحفز", ["Founder OS", "CTA", "Student Execution"],
                update_cadence=U.STABLE,
                egyptianization_note="في مصر يُستخدم لتقليل صعوبة البداية: خطوة صغيرة، منتج جاهز، دعم مباشر، ومطلوب واضح من الطالب.",
                caution="إطار عملي لتصميم السلوك وليس ضمانًا بأن كل محفز سيؤدي لنفس النتيجة.",
            ),
            T(
                "peak_end_rule", "Peak-End Rule", "قاعدة الذروة والنهاية", D.COGNITIVE_PSYCHOLOGY, E.META_REVIEWED,
                "تصميم تجربة الطالب والعميل بحيث تبقى أقوى لحظة وآخر لحظة في الذاكرة", ["Customer Journey", "Academy Experience", "Retention"],
                update_cadence=U.STABLE,
                egyptianization_note="تُستخدم في تجربة الطالب: أول مبيعة كذروة، وتقرير نهاية البرنامج كنهاية قوية قابلة للمشاركة.",
                caution="لا تُستخدم لتزييف التجربة؛ يجب أن تعكس قيمة حقيقية مدعومة بالتنفيذ.",
            ),
            T("endowment", "Endowment Effect", "تأثير التملك", D.BEHAVIORAL_ECONOMICS, E.META_REVIEWED, "رفع قيمة ما يشعر العميل أنه امتلكه بالفعل", ["Trial", "Community", "Offer"]),
            T("choice_architecture", "Choice Architecture", "هندسة الاختيارات", D.DECISION_SCIENCE, E.INDUSTRY_VALIDATED, "ترتيب العروض والباقات لتقليل التردد", ["Offer", "Pricing"]),
            T("mental_accounting", "Mental Accounting", "المحاسبة الذهنية", D.BEHAVIORAL_ECONOMICS, E.META_REVIEWED, "فهم تقسيم العميل للفلوس داخليًا", ["Pricing", "Installments"]),
            T("expected_value", "Expected Value", "القيمة المتوقعة", D.DECISION_SCIENCE, E.ACADEMIC_CORE, "تقدير العائد مقابل المخاطرة", ["Decision Engine", "Product Selection"]),
            T("bayesian", "Bayesian Decision Theory", "نظرية بايز لاتخاذ القرار", D.DECISION_SCIENCE, E.ACADEMIC_CORE, "تحديث احتمالات نجاح المنتج بالبيانات", ["Reality Validation", "Scaling"]),
            T("monte_carlo", "Monte Carlo Simulation", "محاكاة مونت كارلو", D.DECISION_SCIENCE, E.ACADEMIC_CORE, "محاكاة المخاطر والتباين", ["Forecasting", "Risk"]),
            T("decision_trees", "Decision Trees", "أشجار القرار", D.DECISION_SCIENCE, E.ACADEMIC_CORE, "تنظيم قرارات Kill/Fix/Scale", ["Decision Engine"]),
            T("positioning", "Positioning Theory", "نظرية التموضع", D.BRANDING, E.INDUSTRY_VALIDATED, "تحديد مكان البراند في عقل السوق", ["Brand", "Message"]),
            T("category_design", "Category Design", "تصميم الفئة السوقية", D.MARKETING_STRATEGY, E.INDUSTRY_VALIDATED, "خلق فئة جديدة بدل المنافسة التقليدية", ["Positioning", "Strategy"]),
            T("blue_ocean", "Blue Ocean Strategy", "استراتيجية المحيط الأزرق", D.MARKETING_STRATEGY, E.INDUSTRY_VALIDATED, "تجنب ازدحام المنافسة عبر إعادة تعريف القيمة", ["Strategy", "Offer"]),
            T("value_prop", "Value Proposition Canvas", "لوحة عرض القيمة", D.MARKETING_STRATEGY, E.INDUSTRY_VALIDATED, "ربط آلام العميل بالمكاسب والحلول", ["Offer", "Landing Page"]),
            T("stp", "Segmentation, Targeting, Positioning", "التقسيم والاستهداف والتموضع", D.MARKETING_STRATEGY, E.ACADEMIC_CORE, "اختيار الجمهور والرسالة", ["Campaign", "Persona"]),
            T("aida", "AIDA Model", "نموذج الانتباه والرغبة والفعل", D.MARKETING_STRATEGY, E.HEURISTIC, "ترتيب الرسالة الإعلانية", ["Copy", "Video Script"]),
            T("pas", "PAS Framework", "مشكلة-تضخيم-حل", D.MARKETING_STRATEGY, E.HEURISTIC, "كتابة إعلانات Direct Response", ["Ad Copy"]),
            T("kano", "Kano Model", "نموذج كانو للجودة", D.CONSUMER_BEHAVIOR, E.INDUSTRY_VALIDATED, "تمييز الجودة الأساسية عن المبهرة", ["Product", "Delighters"]),
            T("octalysis", "Octalysis Gamification", "محركات التحفيز الثمانية", D.CONSUMER_BEHAVIOR, E.INDUSTRY_VALIDATED, "فهم الدوافع السلوكية", ["Hooks", "Community", "Gamification"]),
            T("diffusion", "Diffusion of Innovations", "انتشار الابتكارات", D.CONSUMER_BEHAVIOR, E.ACADEMIC_CORE, "تقدير انتشار المنتج بين الشرائح", ["Market", "Launch"]),
            T("bass", "Bass Diffusion Model", "نموذج باس للانتشار", D.DECISION_SCIENCE, E.ACADEMIC_CORE, "تقدير نمو تبني المنتج", ["Forecasting"]),
            T("clv", "Customer Lifetime Value", "القيمة العمرية للعميل", D.OPERATIONS, E.INDUSTRY_VALIDATED, "قياس قيمة العميل على المدى الطويل", ["Profit", "Retention"]),
            T("unit_econ", "Unit Economics", "اقتصاديات الوحدة", D.OPERATIONS, E.INDUSTRY_VALIDATED, "معرفة ربحية كل طلب", ["Profit", "Scaling"]),
            T("breakeven", "Break-even Analysis", "تحليل نقطة التعادل", D.OPERATIONS, E.ACADEMIC_CORE, "تحديد أقصى CPA آمن", ["Campaign", "Profit"]),
            T("lean_startup", "Lean Startup", "منهجية الشركة الرشيقة", D.ENTREPRENEURSHIP, E.INDUSTRY_VALIDATED, "Build-Measure-Learn", ["Validation", "Iteration"]),
            T("customer_dev", "Customer Development", "تطوير العملاء", D.ENTREPRENEURSHIP, E.INDUSTRY_VALIDATED, "اختبار الفرضية مع العملاء", ["Research", "Validation"]),
            T("okr", "Objectives and Key Results", "الأهداف والنتائج الرئيسية", D.OPERATIONS, E.INDUSTRY_VALIDATED, "إدارة التقدم التشغيلي للطالب", ["Academy", "Founder OS"]),
            T("sop", "Standard Operating Procedures", "إجراءات التشغيل القياسية", D.OPERATIONS, E.INDUSTRY_VALIDATED, "تحويل الشغل إلى نظام قابل للتكرار", ["Business Architecture"]),
            T("rag", "Retrieval-Augmented Generation", "التوليد المعزز بالاسترجاع", D.AI_SYSTEMS, E.INDUSTRY_VALIDATED, "تحديث المعرفة من مصادر موثوقة", ["AI Layer", "Research"]),
            T("agents", "Multi-Agent Systems", "أنظمة الوكلاء المتعددة", D.AI_SYSTEMS, E.INDUSTRY_VALIDATED, "تقسيم العمل بين وكلاء بحث/كتابة/تحليل", ["AI Layer"]),
            T("knowledge_graph", "Knowledge Graphs", "خرائط المعرفة", D.AI_SYSTEMS, E.INDUSTRY_VALIDATED, "ربط النظريات بالمخرجات", ["Research", "Curriculum"]),
            T("rlhf", "Human-AI Feedback Loops", "دوائر التغذية الراجعة بين الإنسان والذكاء الاصطناعي", D.AI_SYSTEMS, E.INDUSTRY_VALIDATED, "تحسين المخرجات بناءً على تقييم البشر", ["Academy", "AI QA"]),
            T("reward_prediction", "Reward Prediction Error", "خطأ توقع المكافأة", D.NEUROECONOMICS, E.ACADEMIC_CORE, "فهم التوقع والمفاجأة في الرسالة", ["Hooks", "Offer"], caution="تحذير: إطار تفسيري سلوكي للتسويق واتخاذ القرار، وليس ادعاءً طبيًا أو تشخيصًا عصبيًا أو وعدًا بتغيير كيمياء المخ."),
            T("dopamine_motivation", "Dopamine Motivation Models", "نماذج الدافعية المرتبطة بالدوبامين", D.NEUROECONOMICS, E.ACADEMIC_CORE, "تحليل توقع المكافأة والرغبة", ["CNCR", "Hooks"], caution="تحذير: إطار تفسيري سلوكي للتسويق واتخاذ القرار، وليس ادعاءً طبيًا أو تشخيصًا عصبيًا أو وصفًا علاجيًا."),
            T("trust_oxytocin", "Trust & Social Bonding Research", "أبحاث الثقة والترابط الاجتماعي", D.NEUROECONOMICS, E.ACADEMIC_CORE, "رفع الأمان والثقة في الشراء", ["Trust", "Community"], caution="تحذير: إطار تفسيري سلوكي لبناء الثقة، وليس ادعاءً طبيًا أو تشخيصًا هرمونيًا أو وعدًا بتأثير بيولوجي مباشر."),
            T("hofstede", "Hofstede Cultural Dimensions", "أبعاد هوفستيد الثقافية", D.LOCAL_CULTURE, E.INDUSTRY_VALIDATED, "تكييف الرسالة حسب الثقافة المحلية", ["Arab Lens", "Egyptianization"], update_cadence=U.QUARTERLY),
            T("arab_barometer", "Arab Barometer Indicators", "مؤشرات الباروميتر العربي", D.LOCAL_CULTURE, E.INDUSTRY_VALIDATED, "تحديث الحس الثقافي والاجتماعي عربيًا", ["Research", "Generational"], update_cadence=U.QUARTERLY),
            T("capmas", "CAPMAS Egyptian Statistics", "بيانات الجهاز المركزي للتعبئة العامة والإحصاء", D.LOCAL_CULTURE, E.INDUSTRY_VALIDATED, "تحديث بيانات مصر الديموغرافية والاقتصادية", ["Egyptianization", "Market"], update_cadence=U.MONTHLY),
            T("generation_apc", "Age-Period-Cohort Lens", "عدسة العمر-الفترة-الجيل", D.CONSUMER_BEHAVIOR, E.INDUSTRY_VALIDATED, "منع التصنيف الجيلي الحتمي", ["Generational Intelligence"], update_cadence=U.QUARTERLY),
            T("paid_social_learning", "Paid Social Feedback Loops", "دوائر تعلم الإعلانات المدفوعة", D.MARKETING_STRATEGY, E.INDUSTRY_VALIDATED, "تحسين القرارات حسب بيانات الحملات", ["Pixel", "Decision Engine"], update_cadence=U.LIVE),
            T("creative_testing", "Creative Testing Methodology", "منهجية اختبار الكرياتيف", D.MARKETING_STRATEGY, E.INDUSTRY_VALIDATED, "فصل مشكلة المنتج عن مشكلة الرسالة", ["Campaign", "Creative"], update_cadence=U.WEEKLY),
            T("cohort_retention", "Cohort Retention Analysis", "تحليل الاحتفاظ حسب الدفعات", D.OPERATIONS, E.INDUSTRY_VALIDATED, "قياس استمرارية الطلاب والعملاء", ["Academy", "Club"], update_cadence=U.MONTHLY),
            T("community_network", "Network Effects & Community Theory", "تأثير الشبكة والمجتمع", D.ENTREPRENEURSHIP, E.INDUSTRY_VALIDATED, "بناء Merchants Arabia كنادي قيمة", ["Community", "Growth"], update_cadence=U.QUARTERLY),
            T("founder_resilience", "Entrepreneurial Resilience", "المرونة النفسية لرائد المشروع", D.ENTREPRENEURSHIP, E.INDUSTRY_VALIDATED, "قياس قدرة الطالب على الاستمرار", ["Founder OS"], update_cadence=U.QUARTERLY),
            T("self_efficacy", "Self-Efficacy Theory", "نظرية الكفاءة الذاتية", D.COGNITIVE_PSYCHOLOGY, E.ACADEMIC_CORE, "رفع ثقة الطالب في التنفيذ", ["Founder OS", "Curriculum"]),
            T("deliberate_practice", "Deliberate Practice", "الممارسة المتعمدة", D.COGNITIVE_PSYCHOLOGY, E.ACADEMIC_CORE, "تصميم ورش أسبوعية للجادين", ["Academy", "Workshops"]),
        ]

    @classmethod
    def count(cls) -> int:
        return len(cls.default_theories())

    @classmethod
    def by_domain(cls) -> Dict[str, int]:
        out: Dict[str, int] = {}
        for th in cls.default_theories():
            out[th.domain.value] = out.get(th.domain.value, 0) + 1
        return out

    @classmethod
    def export_csv(cls, path: str | Path) -> Path:
        path = Path(path)
        with path.open("w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "id", "name_en", "name_ar", "domain", "evidence_level",
                    "purpose_in_thinc", "applied_to", "update_cadence",
                    "egyptianization_note", "caution",
                ],
            )
            writer.writeheader()
            for th in cls.default_theories():
                row = asdict(th)
                row["domain"] = th.domain.value
                row["evidence_level"] = th.evidence_level.value
                row["update_cadence"] = th.update_cadence.value
                row["applied_to"] = " | ".join(th.applied_to)
                writer.writerow(row)
        return path


# =============================================================================
# SECTION 2 · EGYPTIANIZATION & GENERATIONAL LANGUAGE ENGINE
# =============================================================================

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


# =============================================================================
# SECTION 3 · BUSINESS ARCHITECTURE LAYER
# =============================================================================

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


# =============================================================================
# SECTION 4 · COMPETITIVE INTELLIGENCE LAYER
# =============================================================================

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


# =============================================================================
# SECTION 5 · CATEGORY DESIGN LAYER
# =============================================================================

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


# =============================================================================
# SECTION 6 · FOUNDER OS LAYER
# =============================================================================

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


# =============================================================================
# SECTION 7 · AI OPERATING LAYER
# =============================================================================

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


# =============================================================================
# SECTION 8 · ACADEMY OPERATING SYSTEM
# =============================================================================

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


# =============================================================================
# SECTION 9 · THINC v4 COMPOSITE ENGINE
# =============================================================================

@dataclass
class THINCV4ProjectInput:
    project_name: str
    target_generation: EgyptianAudienceGeneration = EgyptianAudienceGeneration.MIXED
    skill_level: AudienceSkillLevel = AudienceSkillLevel.BEGINNER
    persona_completeness: float = 75.0
    taha_index: float = 7.0
    profitability_score: float = -1.0
    reality_score: float = -1.0
    generational_alignment: float = 1.0
    founder_os: FounderOS = field(default_factory=FounderOS)
    business_architecture: BusinessArchitecture = field(default_factory=BusinessArchitecture)
    category_design: CategoryDesign = field(default_factory=CategoryDesign)
    competitive_intelligence: CompetitiveIntelligence = field(default_factory=CompetitiveIntelligence)
    academy_os: AcademyOperatingSystem = field(default_factory=AcademyOperatingSystem)


@dataclass
class THINCV4Report:
    project_name: str
    final_score: float
    grade: str
    components: Dict[str, float]
    language_profile: EgyptianLanguageProfile
    message: str
    recommendations: List[str]
    theory_count: int
    theory_domains: Dict[str, int]
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["language_profile"]["generation"] = self.language_profile.generation.value
        d["language_profile"]["skill_level"] = self.language_profile.skill_level.value
        return d


class THINCV4Engine:
    """Main orchestration engine for THINC v4.0."""

    @staticmethod
    def _grade(score: float) -> str:
        if score >= 8.5:
            return "A — جاهز كمنظومة قوية قابلة للتوسع"
        if score >= 7.0:
            return "B — قوي ويحتاج تحسينات محددة"
        if score >= 5.5:
            return "C — واعد لكن يحتاج ضبط هندسي"
        if score >= 4.0:
            return "D — لا يطلق قبل إعادة بناء نقاط الضعف"
        return "F — أوقف وأعد التصميم"

    @classmethod
    def assess(cls, project: THINCV4ProjectInput) -> THINCV4Report:
        # v3 composite is optional; if v3 unavailable, fallback to local calculation
        if _V3_IMPORT_ERROR is None:
            v3_comp = CompositeScoreV3(
                persona_completeness=project.persona_completeness,
                taha_index=project.taha_index,
                profitability_score=project.profitability_score,
                reality_score=project.reality_score,
                generational_alignment=project.generational_alignment,
            ).calculate()
            v3_score = float(v3_comp["score"])
        else:
            v3_score = round((project.persona_completeness / 10) * 0.4 + project.taha_index * 0.6, 2)

        founder = project.founder_os.founder_readiness()["score"]
        business = project.business_architecture.readiness_score()
        category = project.category_design.category_strength()
        competitive = project.competitive_intelligence.differentiation_score()
        academy = project.academy_os.value_stack_score()

        weights = {
            "v3_behavioral_commerce_core": 0.35,
            "founder_os": 0.15,
            "business_architecture": 0.15,
            "category_design": 0.12,
            "competitive_differentiation": 0.10,
            "academy_operating_system": 0.13,
        }
        components = {
            "v3_behavioral_commerce_core": v3_score,
            "founder_os": founder,
            "business_architecture": business,
            "category_design": category,
            "competitive_differentiation": competitive,
            "academy_operating_system": academy,
        }
        final = round(sum(components[k] * weights[k] for k in weights), 2)

        profile = EgyptianizationEngine.build_profile(project.target_generation, project.skill_level)
        message = EgyptianizationEngine.generate_offer_message(profile)
        recommendations: List[str] = []

        if business < 8:
            recommendations.append("استكمل SOPs التشغيلية قبل التوسع: اعتماد المنتج، الشحن، المرتجعات، وتسوية أرباح الطالب.")
        if founder < 7:
            recommendations.extend(project.founder_os.coaching_recommendations())
        if competitive < 7:
            recommendations.append("اعمل Competitive Matrix لثلاثة منافسين على الأقل قبل إطلاق الرسالة النهائية.")
        if category < 8:
            recommendations.append("قوّي Category POV: نحن لسنا كورسًا؛ نحن برنامج بناء مشروع مدعوم بالكامل.")
        if project.reality_score < 0:
            recommendations.append("أضف Reality Validation فعلي من حملة اختبار قبل أي Scale.")
        if project.academy_os.value_stack_score() >= 8:
            recommendations.append("استخدم Value Stack في العرض: تدريب + تشغيل + مكان فعلي + نادي + AI Tools + Workshops.")

        return THINCV4Report(
            project_name=project.project_name,
            final_score=final,
            grade=cls._grade(final),
            components=components,
            language_profile=profile,
            message=message,
            recommendations=recommendations,
            theory_count=ScientificTheoryRegistry.count(),
            theory_domains=ScientificTheoryRegistry.by_domain(),
        )


# =============================================================================
# SECTION 10 · CREATIVE INTELLIGENCE & EXPERIMENTAL ADVERTISING LAYER
# =============================================================================

class BenefitType(Enum):
    FUNCTIONAL = "Functional"
    EMOTIONAL = "Emotional"
    SOCIAL = "Social"
    ECONOMIC = "Economic"


class AngleArchetype(Enum):
    PROBLEM = "Problem / Pain"
    TRANSFORMATION = "Transformation / Before-After"
    SPEED = "Speed / First Use"
    SAVINGS = "Savings / Alternative Cost"
    TRUST = "Trust / Authenticity / Guarantee"
    SOCIAL_PROOF = "Social Proof / Testimonial"
    OCCASION = "Occasion / Life Event"
    CONVENIENCE = "Convenience / Time Saving"
    INGREDIENT = "Ingredient / Mechanism"
    OBJECTION = "Objection Reversal"
    IDENTITY = "Identity / Self-Image"


class CreativeFormat(Enum):
    UGC = "UGC"
    DEMO = "Product Demo"
    BEFORE_AFTER = "Before / After"
    TESTIMONIAL = "Testimonial"
    CINEMATIC = "Cinematic"
    EXPERT = "Expert Explanation"
    COMPARISON = "Comparison"


class ExperimentVariable(Enum):
    ANGLE = "angle"
    HOOK = "hook"
    EDITING = "editing"
    OFFER = "offer"
    CTA = "cta"


class SalesChannel(Enum):
    WEBSITE = "website"
    WHATSAPP = "whatsapp"
    INSTAGRAM_DM = "instagram_dm"
    MESSENGER = "messenger"
    LEAD_FORM = "lead_form"


class TestBudgetMode(Enum):
    CONTROLLED_ABO = "Controlled ABO"
    META_AB_TEST = "Meta A/B Test"


class EvidenceMode(Enum):
    LEAN = "lean"
    STANDARD = "standard"
    CONSERVATIVE = "conservative"


@dataclass
class ProductFeature:
    name: str
    proof: str = ""
    functional_benefit: str = ""
    emotional_benefit: str = ""
    social_benefit: str = ""
    economic_benefit: str = ""
    claim_risk: str = "low"


@dataclass
class ProductProblem:
    visible_problem: str
    daily_cost: str = ""
    financial_cost: str = ""
    emotional_cost: str = ""
    urgency: float = 5.0
    frequency: float = 5.0


@dataclass
class EgyptianConsumerPersona:
    name: str
    age_range: str
    context: str
    dominant_pains: List[str]
    desired_outcomes: List[str]
    buying_triggers: List[str]
    objections: List[str]
    preferred_proof: List[str]
    price_sensitivity: float = 5.0
    trust_sensitivity: float = 7.0


@dataclass
class ProductIntelligenceInput:
    product_name: str
    category: str
    core_job: str
    features: List[ProductFeature]
    problems: List[ProductProblem]
    differentiators: List[str]
    proof_assets: List[str]
    usage_context: str = ""
    price: float | None = None
    competitor_reference_price: float | None = None
    forbidden_claims: List[str] = field(default_factory=list)


@dataclass
class AdvertisingAngle:
    id: str
    name: str
    archetype: AngleArchetype
    promise: str
    pain: str
    persona_name: str
    proof_required: List[str]
    recommended_formats: List[CreativeFormat]
    sample_hooks: List[str]
    scores: Dict[str, float]
    total_score: float
    cautions: List[str] = field(default_factory=list)


@dataclass
class StoryboardBeat:
    start_second: float
    end_second: float
    purpose: str
    visual: str
    on_screen_text: str
    voiceover: str = ""
    editing_note: str = ""


@dataclass
class CreativeBlueprint:
    angle_id: str
    format: CreativeFormat
    duration_seconds: int
    hook: str
    beats: List[StoryboardBeat]
    proof_sequence: List[str]
    cta: str
    export_ratios: List[str] = field(default_factory=lambda: ["9:16", "4:5", "1:1"])


@dataclass
class CreativeVariant:
    variant_id: str
    angle_id: str
    hook: str
    editing_style: str
    offer: str
    cta: str
    format: CreativeFormat


@dataclass
class CreativePerformance:
    variant_id: str
    spend: float
    impressions: int
    three_second_views: int
    outbound_clicks: int
    purchases: int
    confirmed_orders: int
    delivered_orders: int
    revenue: float
    gross_profit_per_delivered_order: float = 0.0
    average_watch_seconds: float = 0.0
    video_duration_seconds: float = 1.0


@dataclass
class WinnerDecision:
    variant_id: str
    decision: str
    score: float
    metrics: Dict[str, float]
    reasons: List[str]


@dataclass
class MediaEconomicsInput:
    """Per-order economics used to protect cash before any media scale decision."""

    selling_price: float
    product_cost: float
    packaging_cost: float = 0.0
    company_shipping_cost: float = 0.0
    collection_fees: float = 0.0
    expected_return_cost_per_order: float = 0.0
    variable_operations_cost: float = 0.0
    confirmation_rate_pct: float = 80.0
    delivery_rate_from_confirmed_pct: float = 75.0
    safety_margin_pct: float = 30.0


@dataclass
class MediaTestConfig:
    sales_channel: SalesChannel
    total_daily_budget: float
    angle_variants: int = 4
    hook_variants: int = 4
    editing_variants: int = 3
    offer_variants: int = 2
    pixel_ready: bool = False
    capi_ready: bool = False
    purchase_event_configured: bool = False
    sales_messaging_objective_available: bool = False
    country: str = "Egypt"
    audience_description: str = "Broad audience; same audience across all creative variants"
    exclude_existing_customers_days: int = 180
    budget_mode: TestBudgetMode = TestBudgetMode.CONTROLLED_ABO
    evidence_mode: EvidenceMode = EvidenceMode.STANDARD
    decision_stage: DecisionStage = DecisionStage.PRE_TEST_RESEARCH


@dataclass
class CampaignObjectivePlan:
    objective: str
    conversion_location: str
    destination: str
    performance_goal: str
    optimization_event: str
    readiness: str
    prerequisites: List[str]
    rationale: List[str]


@dataclass
class MediaEconomicsResult:
    contribution_margin_before_ads: float
    break_even_delivered_cpa: float
    target_delivered_cpa: float
    target_confirmed_cpa: float
    target_purchase_cpa: float
    confirmation_rate_pct: float
    delivery_rate_from_confirmed_pct: float
    expected_purchase_to_delivery_rate_pct: float


@dataclass
class MediaTestStagePlan:
    stage: str
    variable_tested: str
    variants: int
    recommended_days: int
    daily_budget_total: float
    daily_budget_per_variant: float
    target_spend_per_variant: float
    estimated_stage_budget: float
    controlled_variables: List[str]
    graduation_gate: List[str]


@dataclass
class StopLossPolicy:
    attention_review_impressions: int
    hard_review_impressions: int
    soft_stop_spend: float
    hard_stop_spend: float
    soft_stop_conditions: List[str]
    hard_stop_conditions: List[str]
    diagnostic_checks_before_kill: List[str]


@dataclass
class ScalePolicy:
    minimum_delivered_orders: int
    recommended_delivered_orders: int
    minimum_stable_days: int
    minimum_delivery_rate_pct: float
    maximum_delivered_cpa: float
    required_conditions: List[str]
    scaling_method: List[str]


@dataclass
class MediaTestProtocolReport:
    decision: str
    decision_reasons: List[str]
    market_signal_gate: MarketSignalGateResult
    objective_plan: CampaignObjectivePlan
    economics: MediaEconomicsResult
    campaign_structure: Dict[str, Any]
    stages: List[MediaTestStagePlan]
    stop_loss: StopLossPolicy
    scale_policy: ScalePolicy
    warnings: List[str]

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["market_signal_gate"] = self.market_signal_gate.to_dict()
        return data


class ProductDeconstructionEngine:
    """Converts features into customer outcomes and a structured problem hierarchy."""

    @staticmethod
    def feature_value_map(product: ProductIntelligenceInput) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        for feature in product.features:
            rows.append({
                "feature": feature.name,
                "functional_benefit": feature.functional_benefit or f"يساعد على {product.core_job}",
                "emotional_benefit": feature.emotional_benefit,
                "social_benefit": feature.social_benefit,
                "economic_benefit": feature.economic_benefit,
                "proof": feature.proof,
                "claim_risk": feature.claim_risk,
            })
        return rows

    @staticmethod
    def problem_hierarchy(product: ProductIntelligenceInput) -> List[Dict[str, Any]]:
        return [
            {
                "visible_problem": p.visible_problem,
                "daily_cost": p.daily_cost,
                "financial_cost": p.financial_cost,
                "emotional_cost": p.emotional_cost,
                "problem_strength": round((p.urgency * 0.55) + (p.frequency * 0.45), 2),
            }
            for p in sorted(product.problems, key=lambda x: (x.urgency * .55 + x.frequency * .45), reverse=True)
        ]


class CreativeAngleIntelligenceEngine:
    """Generates and ranks advertising angles for a specific Egyptian persona."""

    WEIGHTS = {
        "pain_strength": 0.25,
        "visual_demonstrability": 0.20,
        "egyptian_market_fit": 0.20,
        "proof_strength": 0.15,
        "message_clarity": 0.10,
        "objection_reversal": 0.10,
    }

    @staticmethod
    def _clamp(value: float) -> float:
        return max(0.0, min(10.0, float(value)))

    @classmethod
    def _score(cls, values: Dict[str, float]) -> Tuple[Dict[str, float], float]:
        clean = {k: cls._clamp(values.get(k, 0)) for k in cls.WEIGHTS}
        total = round(sum(clean[k] * w for k, w in cls.WEIGHTS.items()), 2)
        return clean, total

    @classmethod
    def generate_angles(
        cls,
        product: ProductIntelligenceInput,
        persona: EgyptianConsumerPersona,
    ) -> List[AdvertisingAngle]:
        top_problem = ProductDeconstructionEngine.problem_hierarchy(product)[0] if product.problems else {
            "visible_problem": product.core_job, "emotional_cost": "", "problem_strength": 5.0
        }
        proof_score = min(10.0, 3.0 + len(product.proof_assets) * 1.3)
        trust_score = cls._clamp(5 + persona.trust_sensitivity * 0.5)
        pain_score = cls._clamp(top_problem.get("problem_strength", 5))
        visual_score = 9.0 if any(x in product.category.lower() for x in ["beauty", "hair", "skin", "fashion", "home"]) else 6.5
        market_fit = cls._clamp(6 + (persona.price_sensitivity + persona.trust_sensitivity) / 5)
        objection_score = cls._clamp(4 + len(persona.objections) * .8)
        base_cautions = [f"تجنب الادعاءات غير المثبتة: {x}" for x in product.forbidden_claims]

        specs = [
            ("problem", "مشكلة يومية مؤلمة", AngleArchetype.PROBLEM,
             f"حل عملي لمشكلة {top_problem['visible_problem']}", top_problem["visible_problem"],
             [CreativeFormat.UGC, CreativeFormat.DEMO],
             [f"بتعاني من {top_problem['visible_problem']}؟", f"لو {top_problem['visible_problem']} بيرجع كل مرة، شوفي الحل ده."],
             {"pain_strength": pain_score, "visual_demonstrability": visual_score, "egyptian_market_fit": market_fit,
              "proof_strength": proof_score, "message_clarity": 9, "objection_reversal": objection_score}),
            ("transformation", "التحول البصري", AngleArchetype.TRANSFORMATION,
             f"تحول واضح يساعدك على {product.core_job}", top_problem["visible_problem"],
             [CreativeFormat.BEFORE_AFTER, CreativeFormat.DEMO],
             ["استني تشوفي الفرق بين قبل وبعد.", "نفس الشعر… لكن النتيجة مختلفة تمامًا."],
             {"pain_strength": pain_score, "visual_demonstrability": 10, "egyptian_market_fit": market_fit,
              "proof_strength": proof_score, "message_clarity": 9.5, "objection_reversal": 7.5}),
            ("trust", "الأصلي والثقة", AngleArchetype.TRUST,
             "اشتري وأنت مطمّن: إثبات واضح وضمان حقيقي", "الخوف من التقليد أو ضياع الفلوس",
             [CreativeFormat.EXPERT, CreativeFormat.COMPARISON, CreativeFormat.UGC],
             ["قبل ما تشتري… اعرفي إزاي تفرقي الأصلي.", "مش كل عبوة شبه بعض تبقى نفس المنتج."],
             {"pain_strength": trust_score, "visual_demonstrability": 7, "egyptian_market_fit": 9,
              "proof_strength": proof_score, "message_clarity": 8.5, "objection_reversal": 10}),
            ("savings", "بديل أوفر", AngleArchetype.SAVINGS,
             "نتيجة عملية في البيت بتكلفة أقل من البدائل المتكررة", "تكلفة الحلول البديلة",
             [CreativeFormat.COMPARISON, CreativeFormat.UGC],
             ["بتدفعي كام كل شهر علشان توصلي لنفس النتيجة؟", "بدل المصاريف المتكررة… اعملي روتينك في البيت."],
             {"pain_strength": cls._clamp(5 + persona.price_sensitivity / 2), "visual_demonstrability": 7,
              "egyptian_market_fit": market_fit, "proof_strength": proof_score, "message_clarity": 9,
              "objection_reversal": 8.5}),
            ("proof", "تجربة عميلة حقيقية", AngleArchetype.SOCIAL_PROOF,
             "تجربة قابلة للمشاهدة بدل الوعود", "عدم الثقة في الإعلانات",
             [CreativeFormat.TESTIMONIAL, CreativeFormat.UGC, CreativeFormat.BEFORE_AFTER],
             ["دي مش دعاية… دي تجربة الاستخدام كاملة.", "شوفي النتيجة من غير فلتر ولا إضاءة خادعة."],
             {"pain_strength": trust_score, "visual_demonstrability": 9, "egyptian_market_fit": 9,
              "proof_strength": proof_score, "message_clarity": 8.5, "objection_reversal": 9.5}),
            ("convenience", "السهولة وتوفير الوقت", AngleArchetype.CONVENIENCE,
             f"طريقة أسهل وأسرع تساعدك على {product.core_job}", "الوقت والمجهود",
             [CreativeFormat.DEMO, CreativeFormat.UGC],
             ["روتين بسيط بدل وقت ومجهود كل يوم.", "لو وقتك ضيق، الخطوة دي هتفرق معاكي."],
             {"pain_strength": 7.5, "visual_demonstrability": 8, "egyptian_market_fit": 8.5,
              "proof_strength": proof_score, "message_clarity": 9, "objection_reversal": 7}),
        ]

        angles: List[AdvertisingAngle] = []
        for aid, name, archetype, promise, pain, formats, hooks, score_values in specs:
            scores, total = cls._score(score_values)
            angles.append(AdvertisingAngle(
                id=aid,
                name=name,
                archetype=archetype,
                promise=promise,
                pain=pain,
                persona_name=persona.name,
                proof_required=persona.preferred_proof[:3] + product.proof_assets[:3],
                recommended_formats=formats,
                sample_hooks=hooks,
                scores=scores,
                total_score=total,
                cautions=list(base_cautions),
            ))
        return sorted(angles, key=lambda x: x.total_score, reverse=True)


class MontageStrategyEngine:
    """Builds a production-ready short-form storyboard from the selected angle."""

    @staticmethod
    def build_blueprint(
        angle: AdvertisingAngle,
        product: ProductIntelligenceInput,
        duration_seconds: int = 25,
        format: CreativeFormat | None = None,
        cta: str = "اطلبيه دلوقتي قبل انتهاء العرض.",
    ) -> CreativeBlueprint:
        duration_seconds = max(15, min(45, int(duration_seconds)))
        fmt = format or angle.recommended_formats[0]
        hook = angle.sample_hooks[0]
        scale = duration_seconds / 25.0
        def t(x: float) -> float: return round(x * scale, 1)
        beats = [
            StoryboardBeat(t(0), t(3), "Hook", f"لقطة مباشرة للمشكلة: {angle.pain}", hook, hook,
                           "ابدأ بحركة أو Contrast قوي؛ المنتج لا يتأخر عن الثانية 3."),
            StoryboardBeat(t(3), t(7), "Problem Agitation", "تفصيل المشكلة في الاستخدام اليومي",
                           angle.pain, "المشكلة مش في شكلك… المشكلة إن الحل المؤقت بيرجع يختفي.",
                           "Cuts سريعة 0.7–1.2 ثانية، مع نص كبير داخل الـSafe Zone."),
            StoryboardBeat(t(7), t(12), "Solution Reveal", f"إظهار {product.product_name} وطريقة الاستخدام",
                           product.product_name, f"هنا بييجي دور {product.product_name}: {product.core_job}.",
                           "Macro product shot + texture/demo؛ ثبّت لون وهوية المنتج."),
            StoryboardBeat(t(12), t(18), "Proof", "Before/After أو تجربة واقعية بدون فلتر",
                           "شوفي الفرق", "الفرق لازم يتشاف، مش بس يتقال.",
                           "نفس الإضاءة والزاوية قبل وبعد؛ أظهر دليلًا واحدًا في كل لقطة."),
            StoryboardBeat(t(18), t(22), "Offer", "عرض السعر/الضمان/الشحن بشكل واضح",
                           "عرض محدود", "خدي النتيجة مع عرض واضح وضمان حقيقي.",
                           "ثبّت السعر والميزة 2–3 ثوانٍ؛ تجنب ازدحام النص."),
            StoryboardBeat(t(22), t(25), "CTA", "Packshot نهائي + طريقة الطلب",
                           cta, cta, "End card نظيف، CTA واحد، واتساب/زر الطلب واضح."),
        ]
        return CreativeBlueprint(
            angle_id=angle.id,
            format=fmt,
            duration_seconds=duration_seconds,
            hook=hook,
            beats=beats,
            proof_sequence=angle.proof_required,
            cta=cta,
        )


class ControlledCreativeExperimentEngine:
    """Creates a sequential test plan where only one variable changes at a time."""

    @staticmethod
    def build_test_matrix(
        top_angles: List[AdvertisingAngle],
        base_offer: str,
        base_cta: str,
        editing_styles: List[str] | None = None,
    ) -> Dict[str, List[CreativeVariant]]:
        if not top_angles:
            raise ValueError("At least one advertising angle is required.")
        editing_styles = editing_styles or ["UGC واقعي", "Demo سريع", "Premium Clean"]
        matrix: Dict[str, List[CreativeVariant]] = {"angle_test": [], "hook_test": [], "editing_test": []}

        # Stage 1: angle changes; hook structure, offer, CTA and editing are controlled.
        for i, angle in enumerate(top_angles[:4], 1):
            matrix["angle_test"].append(CreativeVariant(
                variant_id=f"A{i}", angle_id=angle.id, hook=angle.sample_hooks[0],
                editing_style=editing_styles[0], offer=base_offer, cta=base_cta,
                format=angle.recommended_formats[0],
            ))

        # Stage 2: hooks change only for the best predicted angle.
        winner = top_angles[0]
        for i, hook in enumerate(winner.sample_hooks[:4], 1):
            matrix["hook_test"].append(CreativeVariant(
                variant_id=f"H{i}", angle_id=winner.id, hook=hook,
                editing_style=editing_styles[0], offer=base_offer, cta=base_cta,
                format=winner.recommended_formats[0],
            ))

        # Stage 3: editing changes only.
        for i, style in enumerate(editing_styles, 1):
            matrix["editing_test"].append(CreativeVariant(
                variant_id=f"E{i}", angle_id=winner.id, hook=winner.sample_hooks[0],
                editing_style=style, offer=base_offer, cta=base_cta,
                format=winner.recommended_formats[min(i - 1, len(winner.recommended_formats) - 1)],
            ))
        return matrix


class CreativeWinnerElectionEngine:
    """Elects creative winners using attention, intent, sales and delivered-profit signals."""

    @staticmethod
    def evaluate(performance: CreativePerformance) -> WinnerDecision:
        impressions = max(1, performance.impressions)
        spend = max(0.01, performance.spend)
        purchases = max(1, performance.purchases)
        confirmed = max(1, performance.confirmed_orders)
        delivered = max(1, performance.delivered_orders)
        hook_rate = performance.three_second_views / impressions * 100
        ctr = performance.outbound_clicks / impressions * 100
        cpa = performance.spend / purchases
        confirmed_cpa = performance.spend / confirmed
        delivered_cpa = performance.spend / delivered
        confirmation_rate = performance.confirmed_orders / purchases * 100
        delivery_rate = performance.delivered_orders / confirmed * 100
        roas = performance.revenue / spend
        hold_rate = min(100.0, performance.average_watch_seconds / max(1.0, performance.video_duration_seconds) * 100)
        delivered_profit = (performance.gross_profit_per_delivered_order * performance.delivered_orders) - performance.spend

        # Normalized score: delivered outcomes dominate vanity metrics.
        attention = min(10.0, hook_rate / 4.0) * 0.12 + min(10.0, hold_rate / 7.0) * 0.08
        intent = min(10.0, ctr / 0.25) * 0.15
        conversion = min(10.0, roas * 2.0) * 0.20
        operations = min(10.0, confirmation_rate / 10.0) * 0.10 + min(10.0, delivery_rate / 10.0) * 0.15
        profit = (10.0 if delivered_profit > 0 else max(0.0, 5 + delivered_profit / max(1.0, spend))) * 0.20
        score = round(attention + intent + conversion + operations + profit, 2)

        reasons: List[str] = []
        if performance.delivered_orders == 0:
            decision = "HOLD — لا يوجد دليل تسليم كافٍ"
            reasons.append("لا يتم إعلان فائز أو Scale قبل وجود Delivered Orders.")
        elif delivered_profit <= 0:
            decision = "FIX — الإعلان يبيع لكن الربح المسلم غير موجب"
            reasons.append("راجع العرض، تكلفة الطلب المسلم، التأكيد، أو المرتجعات.")
        elif score >= 7.5 and delivery_rate >= 65:
            decision = "SCALE — فائز مثبت بالطلبات المسلمة"
            reasons.append("الانتباه والتحويل وجودة التسليم تدعم التوسع المنضبط.")
        elif score >= 5.5:
            decision = "ITERATE — واعد ويحتاج نسخة محسنة"
            reasons.append("احتفظ بالزاوية الفائزة واختبر Hook أو مونتاج واحد في كل مرة.")
        else:
            decision = "KILL — أوقف النسخة وأعد بناء الرسالة"
            reasons.append("الإشارات الحالية غير كافية لحماية الميزانية.")

        metrics = {
            "hook_rate_pct": round(hook_rate, 2),
            "hold_rate_pct": round(hold_rate, 2),
            "ctr_pct": round(ctr, 2),
            "cpa": round(cpa, 2),
            "confirmed_cpa": round(confirmed_cpa, 2),
            "delivered_cpa": round(delivered_cpa, 2),
            "confirmation_rate_pct": round(confirmation_rate, 2),
            "delivery_rate_pct": round(delivery_rate, 2),
            "roas": round(roas, 2),
            "delivered_profit": round(delivered_profit, 2),
        }
        return WinnerDecision(performance.variant_id, decision, score, metrics, reasons)

    @classmethod
    def rank(cls, performances: List[CreativePerformance]) -> List[WinnerDecision]:
        return sorted((cls.evaluate(p) for p in performances), key=lambda x: x.score, reverse=True)


class MediaTestProtocolEngine:
    """
    Selects the campaign objective and builds a controlled media test protocol.

    The engine protects unit economics first, tests one creative variable at a
    time, and blocks scale until delivered orders produce positive profit.
    Platform labels may vary by ad account, so the generated plan records
    readiness and fallbacks instead of silently changing the business goal.
    """

    MIN_MAX_DAYS: Dict[str, Tuple[int, int]] = {
        "Angle Test": (4, 7),
        "Hook Test": (3, 5),
        "Editing Test": (3, 5),
        "Offer & CTA Test": (3, 5),
        "Winner Validation": (5, 7),
    }

    @staticmethod
    def _validate_percent(name: str, value: float) -> None:
        if not 0 < float(value) <= 100:
            raise ValueError(f"{name} must be greater than 0 and no more than 100.")

    @staticmethod
    def _numeric_campaign_metric(
        metrics: Dict[str, Any],
        name: str,
        reasons: List[str],
    ) -> float | None:
        value = metrics.get(name)
        if value is None:
            reasons.append(f"{name} is required by the existing SCALE policy")
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            reasons.append(f"{name} must be numeric for the existing SCALE policy")
            return None

    @classmethod
    def calculate_economics(cls, inputs: MediaEconomicsInput) -> MediaEconomicsResult:
        cls._validate_percent("confirmation_rate_pct", inputs.confirmation_rate_pct)
        cls._validate_percent("delivery_rate_from_confirmed_pct", inputs.delivery_rate_from_confirmed_pct)
        if not 0 <= float(inputs.safety_margin_pct) < 100:
            raise ValueError("safety_margin_pct must be between 0 and less than 100.")

        costs = (
            inputs.product_cost
            + inputs.packaging_cost
            + inputs.company_shipping_cost
            + inputs.collection_fees
            + inputs.expected_return_cost_per_order
            + inputs.variable_operations_cost
        )
        contribution = inputs.selling_price - costs
        if contribution <= 0:
            raise ValueError("Product contribution margin before advertising must be positive.")

        confirmation = inputs.confirmation_rate_pct / 100.0
        delivery = inputs.delivery_rate_from_confirmed_pct / 100.0
        purchase_to_delivery = confirmation * delivery
        target_delivered = contribution * (1.0 - inputs.safety_margin_pct / 100.0)
        target_confirmed = target_delivered * delivery
        target_purchase = target_confirmed * confirmation

        return MediaEconomicsResult(
            contribution_margin_before_ads=round(contribution, 2),
            break_even_delivered_cpa=round(contribution, 2),
            target_delivered_cpa=round(target_delivered, 2),
            target_confirmed_cpa=round(target_confirmed, 2),
            target_purchase_cpa=round(target_purchase, 2),
            confirmation_rate_pct=round(inputs.confirmation_rate_pct, 2),
            delivery_rate_from_confirmed_pct=round(inputs.delivery_rate_from_confirmed_pct, 2),
            expected_purchase_to_delivery_rate_pct=round(purchase_to_delivery * 100.0, 2),
        )

    @staticmethod
    def choose_objective(config: MediaTestConfig) -> CampaignObjectivePlan:
        channel = config.sales_channel
        prerequisites: List[str] = []
        rationale: List[str] = []

        if channel == SalesChannel.WEBSITE:
            prerequisites = [
                "Meta Pixel is installed and firing correctly",
                "Purchase event is configured and deduplicated",
                "Conversions API is recommended for server-side resilience",
                "Checkout and order confirmation flow have been tested",
            ]
            ready = config.pixel_ready and config.purchase_event_configured
            readiness = "READY" if ready else "BLOCKED — fix tracking before purchase testing"
            rationale = [
                "The business outcome is a purchase, so optimization must remain aligned with Purchase.",
                "Traffic or video-view optimization can identify cheap visitors or viewers rather than buyers.",
            ]
            if not config.capi_ready:
                rationale.append("CAPI is not mandatory to generate the plan, but its absence weakens measurement resilience.")
            return CampaignObjectivePlan(
                objective="Sales",
                conversion_location="Website",
                destination="Product / checkout website",
                performance_goal="Maximize number of conversions",
                optimization_event="Purchase",
                readiness=readiness,
                prerequisites=prerequisites,
                rationale=rationale,
            )

        if channel in {SalesChannel.WHATSAPP, SalesChannel.INSTAGRAM_DM, SalesChannel.MESSENGER}:
            app_name = {
                SalesChannel.WHATSAPP: "WhatsApp",
                SalesChannel.INSTAGRAM_DM: "Instagram Direct",
                SalesChannel.MESSENGER: "Messenger",
            }[channel]
            objective = "Sales" if config.sales_messaging_objective_available else "Leads"
            readiness = "READY"
            prerequisites = [
                f"{app_name} account is connected to the Meta business portfolio",
                "A qualification script separates inquiries from qualified leads",
                "Order, confirmation, and delivery statuses are recorded outside Ads Manager",
            ]
            rationale = [
                "Use the messaging objective available in the ad account while keeping the final KPI as delivered orders.",
                "A conversation is not counted as a sale; track qualified lead → order → confirmed → delivered.",
            ]
            return CampaignObjectivePlan(
                objective=objective,
                conversion_location="Messaging apps",
                destination=app_name,
                performance_goal="Maximize number of conversations",
                optimization_event="Qualified conversation with offline order tracking",
                readiness=readiness,
                prerequisites=prerequisites,
                rationale=rationale,
            )

        return CampaignObjectivePlan(
            objective="Leads",
            conversion_location="Instant forms",
            destination="Meta instant form",
            performance_goal="Maximize number of leads",
            optimization_event="Qualified lead",
            readiness="READY",
            prerequisites=[
                "The form includes qualification questions",
                "Lead status is synced to a CRM or order sheet",
                "Confirmed and delivered outcomes are fed back into reporting",
            ],
            rationale=["Use only when website or messaging checkout is not the operational path."],
        )

    @classmethod
    def _stage_days(
        cls,
        stage: str,
        target_spend_per_variant: float,
        budget_per_variant: float,
    ) -> int:
        min_days, max_days = cls.MIN_MAX_DAYS[stage]
        raw_days = math.ceil(target_spend_per_variant / max(1.0, budget_per_variant))
        return max(min_days, min(max_days, raw_days))

    @classmethod
    def _build_stage(
        cls,
        stage: str,
        variable: str,
        variants: int,
        total_daily_budget: float,
        target_purchase_cpa: float,
        spend_multiple: float,
        controlled: List[str],
        gate: List[str],
    ) -> MediaTestStagePlan:
        variants = max(1, int(variants))
        per_variant = total_daily_budget / variants
        target_spend = max(target_purchase_cpa, target_purchase_cpa * spend_multiple)
        days = cls._stage_days(stage, target_spend, per_variant)
        return MediaTestStagePlan(
            stage=stage,
            variable_tested=variable,
            variants=variants,
            recommended_days=days,
            daily_budget_total=round(total_daily_budget, 2),
            daily_budget_per_variant=round(per_variant, 2),
            target_spend_per_variant=round(target_spend, 2),
            estimated_stage_budget=round(total_daily_budget * days, 2),
            controlled_variables=controlled,
            graduation_gate=gate,
        )

    @classmethod
    def build(
        cls,
        economics_input: MediaEconomicsInput,
        config: MediaTestConfig,
        market_evidence: List[MarketSignalEvidence] | None = None,
    ) -> MediaTestProtocolReport:
        if config.total_daily_budget <= 0:
            raise ValueError("total_daily_budget must be positive.")
        economics = cls.calculate_economics(economics_input)
        objective = cls.choose_objective(config)
        market_gate = MarketSignalTriangulationEngine.evaluate(
            market_evidence or [],
            config.decision_stage,
        )

        angle_count = max(2, min(4, int(config.angle_variants)))
        hook_count = max(2, min(4, int(config.hook_variants)))
        editing_count = max(2, min(3, int(config.editing_variants)))
        offer_count = max(2, min(3, int(config.offer_variants)))
        cpa = economics.target_purchase_cpa

        stages = [
            cls._build_stage(
                "Angle Test", "Advertising angle", angle_count, config.total_daily_budget, cpa, 2.0,
                ["Audience", "Offer", "CTA", "Editing style", "Landing page / messaging script"],
                ["At least one conversion-quality signal", "Compare Purchase/qualified-order CPA", "Keep top 1–2 angles"],
            ),
            cls._build_stage(
                "Hook Test", "First 2–3 seconds", hook_count, config.total_daily_budget, cpa, 1.5,
                ["Winning angle", "Body", "Offer", "CTA", "Editing style"],
                ["Hook and hold improve without damaging purchase quality", "Select one winning hook"],
            ),
            cls._build_stage(
                "Editing Test", "Editing / format", editing_count, config.total_daily_budget, cpa, 1.5,
                ["Winning angle", "Winning hook", "Offer", "CTA"],
                ["Choose format by delivered-order economics, not watch time alone"],
            ),
            cls._build_stage(
                "Offer & CTA Test", "Offer or CTA — one at a time", offer_count, config.total_daily_budget, cpa, 1.5,
                ["Winning angle", "Winning hook", "Winning edit", "Audience"],
                ["Improved conversion rate", "Delivered CPA remains within target"],
            ),
            cls._build_stage(
                "Winner Validation", "No new creative variable", 1, config.total_daily_budget, cpa, 4.0,
                ["Creative", "Audience", "Offer", "CTA", "Tracking"],
                ["Delivered profit is positive", "Delivery rate is stable", "Scale gate is met"],
            ),
        ]

        soft_stop = round(cpa, 2)
        hard_stop = round(cpa * 1.75, 2)
        intent_signal = (
            "No Add to Cart / Checkout signal"
            if config.sales_channel == SalesChannel.WEBSITE
            else "No qualified conversation or order signal"
        )
        stop_loss = StopLossPolicy(
            attention_review_impressions=1500,
            hard_review_impressions=2000,
            soft_stop_spend=soft_stop,
            hard_stop_spend=hard_stop,
            soft_stop_conditions=[
                f"Spend reaches about 1× target Purchase CPA ({soft_stop:.2f})",
                intent_signal,
                "Weak outbound CTR and weak early retention together",
            ],
            hard_stop_conditions=[
                f"Spend reaches about 1.75× target Purchase CPA ({hard_stop:.2f}) with no purchase/order",
                "Creative is weak at attention, intent, and conversion layers",
                "No tracking or checkout defect explains the result",
            ],
            diagnostic_checks_before_kill=[
                "Verify website, checkout, form, or WhatsApp destination",
                "Verify Pixel/CAPI and event firing when using a website",
                "Verify price, stock, shipping, and offer clarity",
                "Verify the call-center response time and qualification script",
            ],
        )

        delivered_min = {
            EvidenceMode.LEAN: 5,
            EvidenceMode.STANDARD: 10,
            EvidenceMode.CONSERVATIVE: 20,
        }[config.evidence_mode]
        scale_policy = ScalePolicy(
            minimum_delivered_orders=delivered_min,
            recommended_delivered_orders=max(10, delivered_min),
            minimum_stable_days=3 if config.evidence_mode != EvidenceMode.CONSERVATIVE else 5,
            minimum_delivery_rate_pct=65.0,
            maximum_delivered_cpa=economics.target_delivered_cpa,
            required_conditions=[
                "Delivered profit is positive",
                "Delivered CPA is at or below the target",
                "Delivery rate is at least 65% or the business-specific minimum",
                "Results are stable for the minimum number of days",
                "No operational bottleneck in stock, confirmation, or fulfillment",
            ],
            scaling_method=[
                "Increase budget in controlled steps rather than a single large jump",
                "Keep the proven creative unchanged while validating the higher spend",
                "Continue generating iterations from the winning angle to avoid fatigue",
                "Recalculate CPA thresholds whenever price, cost, or delivery rates change",
            ],
        )

        decision = market_gate.decision.value
        decision_reasons = list(market_gate.reasons)
        scale_threshold_reasons: List[str] = []
        if (
            config.decision_stage is DecisionStage.SCALE
            and market_gate.decision is GateDecision.PASS
        ):
            campaign_snapshots = [
                item
                for item in market_gate.evidence_snapshot
                if item.get("source") == "first_party_campaign"
                and item.get("evaluated_status") == "FRESH"
            ]
            campaign_snapshot = max(
                campaign_snapshots,
                key=lambda item: str(item.get("collected_at") or ""),
            )
            campaign_metrics = dict(campaign_snapshot.get("metrics", {}))
            delivered_orders = cls._numeric_campaign_metric(
                campaign_metrics,
                "delivered_orders",
                scale_threshold_reasons,
            )
            delivered_cpa = cls._numeric_campaign_metric(
                campaign_metrics,
                "delivered_cpa",
                scale_threshold_reasons,
            )
            delivery_rate = cls._numeric_campaign_metric(
                campaign_metrics,
                "delivery_rate_pct",
                scale_threshold_reasons,
            )
            if (
                delivered_orders is not None
                and delivered_orders < scale_policy.minimum_delivered_orders
            ):
                scale_threshold_reasons.append(
                    "delivered_orders is below the existing minimum of "
                    f"{scale_policy.minimum_delivered_orders}"
                )
            if (
                delivered_cpa is not None
                and delivered_cpa > scale_policy.maximum_delivered_cpa
            ):
                scale_threshold_reasons.append(
                    "delivered_cpa exceeds the existing maximum of "
                    f"{scale_policy.maximum_delivered_cpa:.2f}"
                )
            if (
                delivery_rate is not None
                and delivery_rate < scale_policy.minimum_delivery_rate_pct
            ):
                scale_threshold_reasons.append(
                    "delivery_rate_pct is below the existing minimum of "
                    f"{scale_policy.minimum_delivery_rate_pct:.2f}"
                )
            if scale_threshold_reasons:
                decision = GateDecision.BLOCK_SCALE.value
                decision_reasons.extend(scale_threshold_reasons)
            else:
                decision_reasons.append(
                    "Existing delivered-order, Delivered CPA, and delivery-rate SCALE thresholds pass."
                )

        warnings: List[str] = []
        if objective.readiness.startswith("BLOCKED"):
            warnings.append("Website purchase testing is blocked until tracking and the Purchase event are ready.")
        if config.sales_channel == SalesChannel.WEBSITE and not config.capi_ready:
            warnings.append("CAPI is not ready; measurement may be less resilient than Pixel + CAPI together.")
        angle_budget_per_variant = config.total_daily_budget / angle_count
        if angle_budget_per_variant < cpa:
            warnings.append(
                "Daily budget per angle is below 1× target Purchase CPA. Test angles in waves or expect the maximum duration."
            )
        if config.total_daily_budget < cpa * 2:
            warnings.append("Total daily budget is low relative to target CPA; avoid testing too many variables simultaneously.")
        if config.sales_channel != SalesChannel.WEBSITE:
            warnings.append("Ads Manager conversations/leads are intermediate signals; the final winner must use confirmed and delivered orders.")
        if market_gate.decision is GateDecision.HOLD_FOR_RESEARCH:
            warnings.append(
                "Market research is held until fresh Google Trends, Meta Ad Library, and marketplace evidence is supplied."
            )
        elif market_gate.decision is GateDecision.BLOCK_SCALE:
            warnings.append(
                "Scale is blocked until the market gate and fresh first-party delivered-profit evidence pass."
            )
        if scale_threshold_reasons:
            warnings.append(
                "Market evidence is complete, but the independent Media Test Protocol SCALE thresholds block expansion."
            )

        campaign_structure = {
            "naming": "[PRODUCT]_[VARIABLE]_TEST_[OBJECTIVE]",
            "budget_method": config.budget_mode.value,
            "ad_sets": "One identical ad set per variant during controlled testing",
            "ads_per_ad_set": 1,
            "audience": config.audience_description,
            "country": config.country,
            "placements": "Advantage+ placements unless a placement-specific hypothesis is being tested",
            "exclusions": f"Exclude existing customers/purchasers for {config.exclude_existing_customers_days} days where data is available",
            "change_control": "Change one variable only in each stage",
            "final_kpi": "Delivered profit and Delivered CPA",
        }

        return MediaTestProtocolReport(
            decision=decision,
            decision_reasons=decision_reasons,
            market_signal_gate=market_gate,
            objective_plan=objective,
            economics=economics,
            campaign_structure=campaign_structure,
            stages=stages,
            stop_loss=stop_loss,
            scale_policy=scale_policy,
            warnings=warnings,
        )


@dataclass
class CreativeIntelligenceReport:
    product_name: str
    feature_value_map: List[Dict[str, Any]]
    problem_hierarchy: List[Dict[str, Any]]
    ranked_angles: List[AdvertisingAngle]
    top_blueprint: CreativeBlueprint
    experiment_matrix: Dict[str, List[CreativeVariant]]
    media_test_protocol: MediaTestProtocolReport | None = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if self.media_test_protocol is not None:
            data["media_test_protocol"] = self.media_test_protocol.to_dict()
        return data


class THINCCreativeIntelligenceLayer:
    """End-to-end orchestration: Product → Persona → Angles → Montage → Test Matrix."""

    @classmethod
    def build(
        cls,
        product: ProductIntelligenceInput,
        persona: EgyptianConsumerPersona,
        base_offer: str,
        base_cta: str,
        media_economics: MediaEconomicsInput | None = None,
        media_config: MediaTestConfig | None = None,
        market_evidence: List[MarketSignalEvidence] | None = None,
    ) -> CreativeIntelligenceReport:
        if (media_economics is None) != (media_config is None):
            raise ValueError("media_economics and media_config must be supplied together.")
        angles = CreativeAngleIntelligenceEngine.generate_angles(product, persona)
        blueprint = MontageStrategyEngine.build_blueprint(angles[0], product, cta=base_cta)
        matrix = ControlledCreativeExperimentEngine.build_test_matrix(angles, base_offer, base_cta)
        media_protocol = (
            MediaTestProtocolEngine.build(
                media_economics,
                media_config,
                market_evidence=market_evidence,
            )
            if media_economics is not None and media_config is not None
            else None
        )
        return CreativeIntelligenceReport(
            product_name=product.product_name,
            feature_value_map=ProductDeconstructionEngine.feature_value_map(product),
            problem_hierarchy=ProductDeconstructionEngine.problem_hierarchy(product),
            ranked_angles=angles,
            top_blueprint=blueprint,
            experiment_matrix=matrix,
            media_test_protocol=media_protocol,
        )


# =============================================================================
# SECTION 12 · AUTO-UPDATE RESEARCH LAYER (SAFE STUBS)
# =============================================================================

@dataclass
class ResearchSourceSpec:
    name: str
    env_key: str
    purpose: str
    update_cadence: UpdateCadence
    configured: bool = False
    provider_implemented: bool = False
    enabled: bool = False


class AutoUpdateResearchLayer:
    """Safe auto-update skeleton. Actual APIs must be configured by environment variables."""

    @staticmethod
    def default_sources() -> List[ResearchSourceSpec]:
        U = UpdateCadence
        sources = [
            ResearchSourceSpec("CAPMAS", "CAPMAS_API_KEY", "Egyptian demographic and economic updates", U.MONTHLY),
            ResearchSourceSpec("Arab Barometer", "ARAB_BAROMETER_API_KEY", "Arab cultural and social indicators", U.QUARTERLY),
            ResearchSourceSpec("Meta Ad Library", "META_ADLIB_TOKEN", "Competitor creative intelligence", U.LIVE),
            ResearchSourceSpec("TikTok Creative Center", "TIKTOK_API_KEY", "Trend and creative insights", U.WEEKLY),
            ResearchSourceSpec("Google Trends", "GOOGLE_TRENDS_KEY", "Demand and search trends", U.WEEKLY),
            ResearchSourceSpec("Noon/Jumia/Amazon", "ECOM_PRICE_API_KEY", "Prices and availability", U.LIVE),
        ]
        for s in sources:
            s.configured = bool(os.environ.get(s.env_key))
            s.enabled = s.configured and s.provider_implemented
        return sources

    @staticmethod
    def status() -> Dict[str, Any]:
        sources = AutoUpdateResearchLayer.default_sources()
        return {
            "enabled": [s.name for s in sources if s.enabled],
            "disabled": [s.name for s in sources if not s.enabled],
            "configured_credentials": [s.name for s in sources if s.configured],
            "market_signal_providers": {
                "google_trends": AutomatedProvider.status(
                    "GOOGLE_TRENDS_KEY", provider_implemented=False
                ),
                "meta_ad_library": AutomatedProvider.status(
                    "META_ADLIB_TOKEN", provider_implemented=False
                ),
            },
            "note": (
                "Browser-assisted research and file ingestion are available. "
                "Automated providers remain pending; credentials alone are not evidence."
            ),
        }


# =============================================================================
# SECTION 13 · TESTS & EXAMPLES
# =============================================================================

def example_academy_project() -> THINCV4Report:
    competitors = [
        CompetitorProfile("كورس دروبشيبينج تقليدي", "تعليم فقط", "2000-7000", 5, 5, 4, 2, "لا يوجد تشغيل فعلي"),
        CompetitorProfile("أكاديمية تسويق", "محاضرات وشهادة", "3000-12000", 6, 6, 6, 3, "ضعف التطبيق العملي"),
    ]
    project = THINCV4ProjectInput(
        project_name="برنامج بناء مشروع تجارة إلكترونية مدعوم بالكامل",
        target_generation=EgyptianAudienceGeneration.MIXED,
        skill_level=AudienceSkillLevel.EXPERIENCED_COURSE_BUYER,
        persona_completeness=88,
        taha_index=8.5,
        profitability_score=7.2,
        reality_score=-1,
        generational_alignment=0.92,
        founder_os=FounderOS(7, 7, 8, 7, 7, 6.5),
        competitive_intelligence=CompetitiveIntelligence(
            competitors=competitors,
            market_gap="السوق مليان كورسات نظرية، لكن قليل جدًا برامج فيها تشغيل حقيقي ومكان فعلي ودعم AI ونادي تجار.",
        ),
    )
    return THINCV4Engine.assess(project)


def example_creative_product() -> CreativeIntelligenceReport:
    product = ProductIntelligenceInput(
        product_name="Karseell Collagen Hair Mask",
        category="Beauty Hair Care",
        core_job="تقليل مظهر الهيشان والجفاف وتحسين نعومة ولمعان الشعر",
        features=[
            ProductFeature("قوام ماسك كثيف", "لقطة Texture واضحة", "تغطية الشعر بسهولة", "إحساس عناية ورفاهية"),
            ProductFeature("استخدام منزلي", "Demo كامل", "روتين سهل في البيت", "راحة وثقة", economic_benefit="تقليل الاعتماد على الصالون"),
        ],
        problems=[
            ProductProblem("الهيشان والجفاف", "وقت أطول في التصفيف", "مصاريف منتجات وصالون متكررة", "إحباط وقلة ثقة", 9, 9),
            ProductProblem("التقصف ومظهر الأطراف المجهدة", "الشعر شكله غير مرتب", "قص أو علاجات متكررة", "قلق قبل المناسبات", 8, 7),
        ],
        differentiators=["نتيجة بصرية قابلة للتصوير", "حجم مناسب للاستخدام المتكرر"],
        proof_assets=["Before/After بنفس الإضاءة", "UGC حقيقي", "تصوير العبوة والقوام"],
        usage_context="روتين عناية أسبوعي في المنزل",
        forbidden_claims=["علاج دائم للتقصف", "تغيير كيمياء الشعر", "نتيجة مضمونة لكل المستخدمين"],
    )
    persona = EgyptianConsumerPersona(
        name="سيدة مصرية مهتمة بالعناية بالشعر",
        age_range="18-35",
        context="طالبة أو موظفة أو عروسة تريد نتيجة واضحة في البيت",
        dominant_pains=["الهيشان", "الجفاف", "ضيق الوقت"],
        desired_outcomes=["نعومة", "لمعان", "ثقة"],
        buying_triggers=["Before/After", "عرض واضح", "ضمان الأصلي"],
        objections=["هل أصلي؟", "هل يناسب شعري؟", "هل النتيجة حقيقية؟"],
        preferred_proof=["تجربة بدون فلتر", "نفس الإضاءة قبل وبعد", "مراجعة عميلة مصرية"],
        price_sensitivity=7.5,
        trust_sensitivity=9.0,
    )
    economics = MediaEconomicsInput(
        selling_price=1000,
        product_cost=500,
        packaging_cost=20,
        company_shipping_cost=70,
        collection_fees=20,
        expected_return_cost_per_order=30,
        variable_operations_cost=10,
        confirmation_rate_pct=80,
        delivery_rate_from_confirmed_pct=75,
        safety_margin_pct=30,
    )
    media_config = MediaTestConfig(
        sales_channel=SalesChannel.WEBSITE,
        total_daily_budget=1000,
        angle_variants=4,
        hook_variants=4,
        editing_variants=3,
        offer_variants=2,
        pixel_ready=True,
        capi_ready=True,
        purchase_event_configured=True,
    )
    return THINCCreativeIntelligenceLayer.build(
        product, persona,
        base_offer="خصم محدود + ضمان المنتج الأصلي",
        base_cta="اطلبيه دلوقتي قبل انتهاء العرض.",
        media_economics=economics,
        media_config=media_config,
    )


def example_media_protocol() -> MediaTestProtocolReport:
    economics = MediaEconomicsInput(
        selling_price=1000,
        product_cost=500,
        packaging_cost=20,
        company_shipping_cost=70,
        collection_fees=20,
        expected_return_cost_per_order=30,
        variable_operations_cost=10,
        confirmation_rate_pct=80,
        delivery_rate_from_confirmed_pct=75,
        safety_margin_pct=30,
    )
    config = MediaTestConfig(
        sales_channel=SalesChannel.WHATSAPP,
        total_daily_budget=1000,
        sales_messaging_objective_available=False,
        evidence_mode=EvidenceMode.STANDARD,
    )
    return MediaTestProtocolEngine.build(economics, config)


def run_all_tests() -> Dict[str, Any]:
    passed: List[str] = []
    failed: List[str] = []

    def check(name: str, condition: bool) -> None:
        (passed if condition else failed).append(name)

    check("identity attribution", verify_attribution())
    check("identity hash length", len(compute_identity_hash()) == 64)
    check("theory count >= 50", ScientificTheoryRegistry.count() >= 50)
    check("has behavioral economics domain", ScientificTheoryRegistry.by_domain().get(TheoryDomain.BEHAVIORAL_ECONOMICS.value, 0) >= 5)

    profile = EgyptianizationEngine.build_profile(EgyptianAudienceGeneration.GEN_Z, AudienceSkillLevel.BEGINNER)
    check("egyptian profile hook", bool(profile.sample_hook))
    check("egyptian profile preferred words", len(profile.preferred_words) >= 5)

    b = BusinessArchitecture()
    check("business architecture readiness", b.readiness_score() >= 8)

    cat = CategoryDesign()
    check("category strength", cat.category_strength() >= 8)

    founder = FounderOS(8, 7, 8, 7, 7, 6)
    check("founder readiness", founder.founder_readiness()["score"] > 6)

    tools = AIOperatingLayer.recommend_stack(AITaskType.CODING)
    check("ai coding stack includes codex", any(t.name == "Codex" for t in tools))

    academy = AcademyOperatingSystem()
    check("academy value stack", academy.value_stack_score() >= 8)

    report = example_academy_project()
    check("example final score", report.final_score > 7)
    check("report theory count", report.theory_count >= 50)

    creative = example_creative_product()
    check("creative feature map", len(creative.feature_value_map) >= 2)
    check("creative problem hierarchy", creative.problem_hierarchy[0]["problem_strength"] >= 8)
    check("creative angles generated", len(creative.ranked_angles) >= 5)
    check("creative angles ranked", creative.ranked_angles[0].total_score >= creative.ranked_angles[-1].total_score)
    check("montage storyboard beats", len(creative.top_blueprint.beats) == 6)
    check("controlled experiment matrix", all(creative.experiment_matrix[k] for k in ["angle_test", "hook_test", "editing_test"]))
    perf = CreativePerformance("A1", 1000, 20000, 8000, 500, 40, 34, 28, 42000, 650, 8.0, 25.0)
    winner = CreativeWinnerElectionEngine.evaluate(perf)
    check("winner uses delivered orders", winner.metrics["delivered_cpa"] > 0)
    check("winner decision generated", winner.decision.startswith(("SCALE", "ITERATE", "FIX", "HOLD", "KILL")))

    media = creative.media_test_protocol
    check("media protocol integrated", media is not None)
    if media is not None:
        check("website objective is sales", media.objective_plan.objective == "Sales")
        check("website optimization is purchase", media.objective_plan.optimization_event == "Purchase")
        check("economics target cpa hierarchy", media.economics.target_purchase_cpa < media.economics.target_confirmed_cpa < media.economics.target_delivered_cpa)
        check("media stages complete", [s.stage for s in media.stages] == ["Angle Test", "Hook Test", "Editing Test", "Offer & CTA Test", "Winner Validation"])
        check("angle duration bounded", 4 <= media.stages[0].recommended_days <= 7)
        check("stop loss protects target cpa", media.stop_loss.hard_stop_spend > media.stop_loss.soft_stop_spend > 0)
        check("scale uses delivered cpa", media.scale_policy.maximum_delivered_cpa == media.economics.target_delivered_cpa)
        check("scale requires delivered orders", media.scale_policy.minimum_delivered_orders >= 5)

    whatsapp = example_media_protocol()
    check("whatsapp fallback objective", whatsapp.objective_plan.objective == "Leads")
    check("whatsapp destination", whatsapp.objective_plan.destination == "WhatsApp")
    check("whatsapp delivered warning", any("delivered" in w.lower() for w in whatsapp.warnings))

    market_now = datetime.now(timezone.utc)

    def market_record(
        source: MarketSignalSource,
        metrics: Dict[str, Any],
        *,
        country: str = "Egypt",
        collected_at: datetime | None = None,
        summary: str = "Documented evidence for an embedded behavioral test.",
    ) -> MarketSignalEvidence:
        return MarketSignalEvidence(
            source=source,
            status=MarketEvidenceStatus.COLLECTED,
            query="embedded test product",
            country=country,
            timeframe="embedded test observation window",
            collected_at=collected_at or market_now,
            collection_method=CollectionMethod.FILE_UPLOAD,
            source_reference=f"embedded-{source.value}.json",
            summary=summary,
            metrics=metrics,
        )

    trends = market_record(
        MarketSignalSource.GOOGLE_TRENDS,
        {"relative_interest_index": 60, "signal_direction": "positive"},
    )
    meta = market_record(
        MarketSignalSource.META_AD_LIBRARY,
        {"active_ads_observed": 4, "signal_direction": "positive"},
    )
    marketplace = market_record(
        MarketSignalSource.MARKETPLACE,
        {"listing_count_observed": 3, "signal_direction": "positive"},
    )
    first_party = market_record(
        MarketSignalSource.FIRST_PARTY_CAMPAIGN,
        {
            "spend": 2400,
            "delivered_orders": 12,
            "delivered_cpa": 200,
            "delivery_rate_pct": 75,
            "delivered_profit": 2400,
            "signal_direction": "positive",
        },
    )

    missing_trends = MarketSignalTriangulationEngine.evaluate(
        [meta, marketplace], DecisionStage.PRE_TEST_RESEARCH, now=market_now
    )
    check(
        "market gate missing trends holds",
        missing_trends.decision is GateDecision.HOLD_FOR_RESEARCH
        and missing_trends.coverage_status_by_source["google_trends"]
        == "NOT_COLLECTED",
    )
    missing_meta = MarketSignalTriangulationEngine.evaluate(
        [trends, marketplace], DecisionStage.PRE_TEST_RESEARCH, now=market_now
    )
    check(
        "market gate missing meta holds",
        missing_meta.decision is GateDecision.HOLD_FOR_RESEARCH,
    )
    stale_marketplace = market_record(
        MarketSignalSource.MARKETPLACE,
        {"listing_count_observed": 3},
        collected_at=market_now - timedelta(days=4),
    )
    stale_gate = MarketSignalTriangulationEngine.evaluate(
        [trends, meta, stale_marketplace],
        DecisionStage.PRE_TEST_RESEARCH,
        now=market_now,
    )
    check(
        "market gate stale evidence holds",
        stale_gate.decision is GateDecision.HOLD_FOR_RESEARCH
        and stale_gate.freshness_status_by_source["marketplace"] == "STALE",
    )
    wrong_country_gate = MarketSignalTriangulationEngine.evaluate(
        [
            market_record(
                MarketSignalSource.GOOGLE_TRENDS,
                {"relative_interest_index": 60},
                country="Saudi Arabia",
            ),
            meta,
            marketplace,
        ],
        DecisionStage.PRE_TEST_RESEARCH,
        now=market_now,
    )
    check(
        "market gate requires Egypt evidence",
        wrong_country_gate.decision is GateDecision.HOLD_FOR_RESEARCH
        and wrong_country_gate.coverage_status_by_source["google_trends"]
        == "WRONG_COUNTRY",
    )
    research_pass = MarketSignalTriangulationEngine.evaluate(
        [trends, meta, marketplace],
        DecisionStage.PRE_TEST_RESEARCH,
        now=market_now,
    )
    check(
        "market gate fresh research passes",
        research_pass.decision is GateDecision.PASS,
    )
    check(
        "campaign evidence not required pretest",
        research_pass.coverage_status_by_source["first_party_campaign"]
        == "NOT_APPLICABLE",
    )
    no_profit = market_record(
        MarketSignalSource.FIRST_PARTY_CAMPAIGN,
        {"delivered_orders": 12},
    )
    scale_no_profit = MarketSignalTriangulationEngine.evaluate(
        [trends, meta, marketplace, no_profit],
        DecisionStage.SCALE,
        now=market_now,
    )
    check(
        "scale gate requires delivered profit",
        scale_no_profit.decision is GateDecision.BLOCK_SCALE,
    )
    scale_pass = MarketSignalTriangulationEngine.evaluate(
        [trends, meta, marketplace, first_party],
        DecisionStage.SCALE,
        now=market_now,
    )
    check("scale evidence gate passes", scale_pass.decision is GateDecision.PASS)
    prior_key = os.environ.get("GOOGLE_TRENDS_KEY")
    os.environ["GOOGLE_TRENDS_KEY"] = "configured-for-test"
    try:
        key_only_gate = MarketSignalTriangulationEngine.evaluate(
            [], DecisionStage.PRE_TEST_RESEARCH, now=market_now
        )
        provider_status = AutomatedProvider.status(
            "GOOGLE_TRENDS_KEY", provider_implemented=False
        )
    finally:
        if prior_key is None:
            os.environ.pop("GOOGLE_TRENDS_KEY", None)
        else:
            os.environ["GOOGLE_TRENDS_KEY"] = prior_key
    check(
        "provider key is not evidence",
        key_only_gate.decision is GateDecision.HOLD_FOR_RESEARCH
        and provider_status["automation_status"] == "AUTOMATED_PROVIDER_PENDING",
    )
    serialized_gate = missing_trends.to_dict()
    check(
        "market gate provenance serializes",
        serialized_gate["decision"] == "HOLD_FOR_RESEARCH"
        and serialized_gate["evidence_snapshot"][0]["source_reference"]
        == "embedded-meta_ad_library.json"
        and bool(serialized_gate["required_actions"]),
    )
    legacy_media = example_media_protocol()
    check(
        "legacy media call returns research hold",
        legacy_media.decision == "HOLD_FOR_RESEARCH"
        and legacy_media.market_signal_gate.decision
        is GateDecision.HOLD_FOR_RESEARCH,
    )

    # Optional v3 tests if v3 import is available
    v3_status = "not_available"
    if _V3_IMPORT_ERROR is None:
        try:
            v3 = run_v3_tests()
            v3_status = "passed" if v3.get("failed", 1) == 0 else "failed"
            check("v3 tests pass", v3_status == "passed")
        except Exception:
            v3_status = "error"
            check("v3 tests pass", False)

    return {
        "total": len(passed) + len(failed),
        "passed": len(passed),
        "failed": len(failed),
        "failed_names": failed,
        "success_rate": round(len(passed) / max(1, len(passed) + len(failed)) * 100, 1),
        "v3_status": v3_status,
    }


def print_summary() -> None:
    print("=" * 80)
    print(f"{FRAMEWORK_NAME}™ {FRAMEWORK_VERSION}")
    print(PROGRAM_POSITIONING)
    print("=" * 80)
    print(f"Scientific theories loaded: {ScientificTheoryRegistry.count()}")
    print("Theory domains:")
    for domain, count in ScientificTheoryRegistry.by_domain().items():
        print(f"- {domain}: {count}")
    print("\nAuto-update status:")
    print(json.dumps(AutoUpdateResearchLayer.status(), ensure_ascii=False, indent=2))
    print(get_watermark())


if __name__ == "__main__":
    if "--test" in sys.argv:
        results = run_all_tests()
        print(json.dumps(results, ensure_ascii=False, indent=2))
        if results["failed"]:
            sys.exit(1)
    elif "--example" in sys.argv:
        academy_report = example_academy_project()
        print(json.dumps(academy_report.to_dict(), ensure_ascii=False, indent=2))
        print(get_watermark())
    elif "--creative-example" in sys.argv:
        creative_report = example_creative_product()
        print(json.dumps(creative_report.to_dict(), ensure_ascii=False, indent=2, default=str))
        print(get_watermark())
    elif "--media-example" in sys.argv:
        media_report = example_media_protocol()
        print(json.dumps(media_report.to_dict(), ensure_ascii=False, indent=2, default=str))
        print(get_watermark())
    elif "--export-theories" in sys.argv:
        out = ScientificTheoryRegistry.export_csv(REPO_ROOT / "thinc_v4_theory_registry.csv")
        print(f"Exported: {out}")
    else:
        print_summary()
