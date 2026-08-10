# -*- coding: utf-8 -*-
"""Scientific theory registry for the THINC v4.2 layer.

THINC™ v4.2 — Invented by Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 Dr. Ehab Taha — Egy-Pioneers Academy.
"""
from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List


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
