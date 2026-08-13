# -*- coding: utf-8 -*-
"""
THINC™ v4.0 — Adaptive Commerce Intelligence & Venture Building System
نظام طه المتكيف للذكاء التجاري وبناء المشاريع

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 الدكتور إيهاب طه — EgyPioneers / Egy-Pioneers Academy

هذا الملف يمثل طبقة v4.0 فوق THINC v3.1.
- يحتفظ بمحركات v3.1: Persona, CNCR, Profit, Reality Validation, Decision Engine.
- يضيف طبقات v4.0: Scientific Theory Registry, Egyptianization, Business Architecture,
  Competitive Intelligence, Category Design, Founder OS, AI Operating Layer,
  Academy Operating System.

تشغيل الاختبارات:
    python THINC_v4_0_Master_Framework.py --test

تشغيل مثال:
    python THINC_v4_0_Master_Framework.py --example
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple, cast

# =============================================================================
# Compatibility with THINC v3.1
# =============================================================================

APP_DIR = Path(__file__).resolve().parent
REPO_ROOT = APP_DIR.parents[1]
LEGACY_DIR = REPO_ROOT / "thinc_v4_0_final_verified_20260620" / "thinc_v4_final"
for import_dir in (APP_DIR, REPO_ROOT, LEGACY_DIR):
    if import_dir.exists() and str(import_dir) not in sys.path:
        sys.path.insert(0, str(import_dir))

from .identity import (
    ATTRIBUTION_NOTICE,
    COPYRIGHT_NOTICE,
    IDENTITY_TAGLINE,
    INVENTOR,
    INVENTOR_AR,
    IP_STATEMENT,
    MODEL_NAME,
    VERSION,
    WATERMARK,
)

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

FRAMEWORK_NAME = MODEL_NAME
FRAMEWORK_VERSION = f"v{VERSION} — Adaptive Commerce Intelligence Edition"
FRAMEWORK_FULL_NAME = "Taha's Holistic Integration of Needs & Consumer behavior"
AUTHOR_NAME_AR = INVENTOR_AR
AUTHOR_NAME_EN = INVENTOR
TRADEMARK_HOLDER = "EgyPioneers — طلائع شباب مصر"
ACADEMY_NAME = "Egy-Pioneers Academy / Insta Learn Academy"
PROGRAM_POSITIONING = "ابنِ مشروع تجارة إلكترونية مدعوم بالكامل من أول فكرة إلى أول عملية بيع."
COPYRIGHT_YEAR = 2026


def validate_finite_number(value: float, name: str) -> float:
    """Validate that a numeric value is finite."""
    numeric = float(value)
    if not math.isfinite(numeric):
        raise ValueError(f"{name} must be a finite number")
    return numeric


def clamp_score(value: float, lower: float = 0.0, upper: float = 10.0) -> float:
    """Clamp a finite score to an inclusive range."""
    numeric = validate_finite_number(value, "score")
    return max(lower, min(upper, numeric))


def validate_score(value: float, name: str, lower: float = 0.0, upper: float = 10.0) -> float:
    """Validate a finite score in an inclusive range."""
    numeric = validate_finite_number(value, name)
    if not lower <= numeric <= upper:
        raise ValueError(f"{name} must be between {lower:g} and {upper:g}")
    return numeric


def compute_identity_hash() -> str:
    identity_string = (
        f"{FRAMEWORK_NAME}|{FRAMEWORK_VERSION}|{FRAMEWORK_FULL_NAME}|"
        f"{AUTHOR_NAME_EN}|{TRADEMARK_HOLDER}|{PROGRAM_POSITIONING}|{COPYRIGHT_YEAR}"
    )
    return hashlib.sha256(identity_string.encode("utf-8")).hexdigest()


def verify_attribution() -> bool:
    return (
        AUTHOR_NAME_AR == INVENTOR_AR
        and AUTHOR_NAME_EN == INVENTOR
        and FRAMEWORK_NAME == MODEL_NAME
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
    # v4.1 — توثيق الاختبار الميداني المحلي (المرحلة 3 من خطة المعايرة)
    field_tests_count: int = 0
    field_test_result: str = ""  # "supported" | "not_supported" | "mixed" | ""
    last_tested: str = ""  # ISO date of the most recent documented field test


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
                    "field_tests_count", "field_test_result", "last_tested",
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
        base = {
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

        skill_modifiers = {
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
            tone=cast(str, base["tone"]),
            preferred_words=list(base["preferred"]) + list(skill_modifiers["extra"]),
            avoided_words=cast(List[str], base["avoided"]),
            trust_builders=skill_modifiers["trust"],
            pain_words=cast(List[str], base["pain"]),
            aspiration_words=cast(List[str], base["aspiration"]),
            sample_hook=cast(str, base["hook"]),
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
            validate_score(val, name)


@dataclass(frozen=True)
class DifferentiationAsset:
    """أصل تمايز واحد في المصفوفة المنظمة — Boolean بدليل، لا تحليل نص.

    v4.1: يستبدل عدّ الكلمات المفتاحية (heuristic قابلة للتلاعب) بحقائق مُثبتة.
    """

    id: str
    name_ar: str
    present: bool = False
    evidence: str = ""  # لينك / مستند / صورة — إلزامي لو present=True

    def __post_init__(self) -> None:
        if self.present and not self.evidence.strip():
            raise ValueError(
                f"Differentiation asset {self.id!r} marked present without evidence — "
                "مفيش تمايز بدون إثبات."
            )


def default_differentiation_assets() -> List[DifferentiationAsset]:
    """أصول التمايز السبعة القياسية لبرامج الأكاديمية (كلها غائبة افتراضيًا)."""
    return [
        DifferentiationAsset("real_operations", "تشغيل فعلي (مصادر، تخزين، شحن، تحصيل)"),
        DifferentiationAsset("physical_location", "مكان فعلي يبني الثقة"),
        DifferentiationAsset("merchants_club", "نادي/مجتمع تجار نشط"),
        DifferentiationAsset("ai_tooling", "أدوات ذكاء اصطناعي تشغيلية"),
        DifferentiationAsset("guarantee", "ضمان/سياسة استرداد واضحة"),
        DifferentiationAsset("financing", "تمويل أو تقسيط فعلي"),
        DifferentiationAsset("execution_followup", "متابعة تنفيذ فردية موثقة"),
    ]


@dataclass
class CompetitiveIntelligence:
    competitors: List[CompetitorProfile] = field(default_factory=list)
    market_gap: str = ""
    recommended_positioning: str = PROGRAM_POSITIONING
    # v4.1 — المصفوفة المنظمة؛ لو فاضية نرجع للـ heuristic القديمة للتوافق الخلفي
    differentiation_assets: List[DifferentiationAsset] = field(default_factory=list)

    def average_competitor_strength(self) -> float:
        if not self.competitors:
            return 0.0
        scores = []
        for c in self.competitors:
            scores.append((c.offer_strength + c.creative_strength + c.trust_strength + c.operational_strength) / 4)
        return round(sum(scores) / len(scores), 2)

    def structured_differentiation_score(self) -> float:
        """v4.1: الدرجة تُحسب من أصول مُثبتة بأدلة، معدّلة بقوة المنافسين."""
        proven = sum(1 for a in self.differentiation_assets if a.present)
        base = 3 + proven * 1.0
        base -= max(0.0, self.average_competitor_strength() - 7) * 0.5
        return round(max(1, min(10, base)), 2)

    def differentiation_score(self) -> float:
        if self.differentiation_assets:
            return self.structured_differentiation_score()
        # Legacy keyword heuristic — retained only for inputs created before v4.1
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
            validate_score(value, name)

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
        monthly_club_fee_egp = validate_finite_number(monthly_club_fee_egp, "monthly_club_fee_egp")
        estimated_individual_cost_egp = validate_finite_number(estimated_individual_cost_egp, "estimated_individual_cost_egp")
        if monthly_club_fee_egp <= 0:
            raise ValueError("Club fee must be > 0")
        if estimated_individual_cost_egp <= 0:
            raise ValueError("Estimated individual cost must be > 0")
        saving = max(0.0, estimated_individual_cost_egp - monthly_club_fee_egp)
        pct = saving / estimated_individual_cost_egp * 100
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
    model_version: str = ""
    weights_version: str = ""
    prediction_id: str = ""
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["language_profile"]["generation"] = self.language_profile.generation.value
        d["language_profile"]["skill_level"] = self.language_profile.skill_level.value
        return d


DEFAULT_COMPONENT_WEIGHTS: Dict[str, float] = {
    "v3_behavioral_commerce_core": 0.35,
    "founder_os": 0.15,
    "business_architecture": 0.15,
    "category_design": 0.12,
    "competitive_differentiation": 0.10,
    "academy_operating_system": 0.13,
}


def load_component_weights() -> Tuple[Dict[str, float], str]:
    """v4.1: الأوزان تُقرأ من weights.json المُصدَّر (المعايرة البايزية تحدثه).

    لو الملف غير موجود أو تالف نرجع للأوزان الافتراضية بأمان.
    يمكن توجيه القراءة لملف أوزان خارجي عبر THINC_WEIGHTS_PATH.
    """
    override = os.environ.get("THINC_WEIGHTS_PATH", "").strip()
    weights_path = Path(override).expanduser() if override else APP_DIR / "weights.json"
    if override and not weights_path.exists():
        weights_path = APP_DIR / "weights.json"
    try:
        with weights_path.open(encoding="utf-8") as fh:
            payload = json.load(fh)
        weights = {k: float(v) for k, v in payload["weights"].items()}
        if set(weights) != set(DEFAULT_COMPONENT_WEIGHTS) or abs(sum(weights.values()) - 1.0) > 1e-6:
            raise ValueError("invalid weights payload")
        return weights, str(payload.get("version", "unversioned"))
    except (OSError, ValueError, KeyError, json.JSONDecodeError):
        return dict(DEFAULT_COMPONENT_WEIGHTS), "builtin-fallback"


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
    def assess(
        cls,
        project: THINCV4ProjectInput,
        outcome_registry: Any = None,
        cohort_id: str = "",
        assessor_id: str = "unassigned",
    ) -> THINCV4Report:
        """يقيّم المشروع، ولو تم تمرير outcome_registry يسجل التوقع تلقائيًا.

        v4.1: كل تقييم في بيئة التشغيل (Streamlit/الأكاديمية) يجب أن يمر بسجل
        النتائج؛ الاستدعاء بدون registry متاح للاختبارات والتجارب فقط.
        """
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
            v3_score = round(clamp_score((project.persona_completeness / 100) * 10) * 0.4 + clamp_score(project.taha_index) * 0.6, 2)

        founder = project.founder_os.founder_readiness()["score"]
        business = project.business_architecture.readiness_score()
        category = project.category_design.category_strength()
        competitive = project.competitive_intelligence.differentiation_score()
        academy = project.academy_os.value_stack_score()

        weights, weights_version = load_component_weights()
        components = {
            "v3_behavioral_commerce_core": v3_score,
            "founder_os": founder,
            "business_architecture": business,
            "category_design": category,
            "competitive_differentiation": competitive,
            "academy_operating_system": academy,
        }
        final = round(clamp_score(sum(components[k] * weights[k] for k in weights)), 2)

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

        report = THINCV4Report(
            project_name=project.project_name,
            final_score=final,
            grade=cls._grade(final),
            components=components,
            language_profile=profile,
            message=message,
            recommendations=recommendations,
            theory_count=ScientificTheoryRegistry.count(),
            theory_domains=ScientificTheoryRegistry.by_domain(),
            model_version=f"{FRAMEWORK_NAME} v{VERSION}",
            weights_version=weights_version,
        )

        if outcome_registry is not None:
            from .outcomes import PredictionRecord, anonymize_student

            record = PredictionRecord(
                student_ref=anonymize_student(project.project_name),
                cohort_id=cohort_id or "uncohorted",
                final_score=final,
                grade=report.grade,
                components=components,
                target_generation=project.target_generation.value,
                skill_level=project.skill_level.value,
                model_version=report.model_version,
                weights_version=weights_version,
                assessor_id=assessor_id,
            )
            report.prediction_id = outcome_registry.log_prediction(record)

        return report


# =============================================================================
# SECTION 10 · AUTO-UPDATE RESEARCH LAYER (SAFE STUBS)
# =============================================================================

@dataclass
class ResearchSourceSpec:
    name: str
    env_key: str
    purpose: str
    update_cadence: UpdateCadence
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
            s.enabled = bool(os.environ.get(s.env_key))
        return sources

    @staticmethod
    def status() -> Dict[str, Any]:
        sources = AutoUpdateResearchLayer.default_sources()
        return {
            "enabled": [s.name for s in sources if s.enabled],
            "disabled": [s.name for s in sources if not s.enabled],
            "note": "التحديث الأوتوماتيك يحتاج مفاتيح API أو RAG pipeline. بدونها يعمل النظام كـ registry ثابت قابل للمراجعة اليدوية.",
        }


# =============================================================================
# SECTION 11 · TESTS & EXAMPLES
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


def main() -> None:
    """CLI entrypoint for THINC v4.0."""
    if "--test" in sys.argv:
        results = run_all_tests()
        print(json.dumps(results, ensure_ascii=False, indent=2))
        if results["failed"]:
            raise SystemExit(1)
    elif "--example" in sys.argv:
        report = example_academy_project()
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
        print(get_watermark())
    elif "--export-registry" in sys.argv or "--export-theories" in sys.argv:
        out = ScientificTheoryRegistry.export_csv(REPO_ROOT / "thinc_v4_theory_registry.csv")
        print(f"Exported: {out}")
    else:
        print_summary()


if __name__ == "__main__":
    main()
