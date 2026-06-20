# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════

   THINC Framework™ v3.0 — Master Behavioral Intelligence System
   نموذج طه المتكامل لاحتياجات الإنسان وسلوك المستهلك — الإصدار الرئيسي

   ─────────────────────────────────────────────────────────────────────────
   © 2026 الدكتور إيهاب طه (Dr. Ehab Taha)
   شركة طلائع شباب مصر — EgyPioneers — جمهورية مصر العربية
   ─────────────────────────────────────────────────────────────────────────

   ⚠️  ملكية فكرية محفوظة بالكامل للدكتور إيهاب طه.
       علامة تجارية مسجلة. THINC™ is a registered trademark.
       All Rights Reserved. جميع الحقوق محفوظة.

       تم تطوير هذا النموذج بقيادة د. إيهاب طه الاستراتيجية،
       بمساعدة أدوات ذكاء اصطناعي متعددة (Claude / ChatGPT / Gemini)
       تعمل تحت إدارته. الملكية الفكرية الكاملة له وحده.

═══════════════════════════════════════════════════════════════════════════════

   THINC = Taha's Holistic Integration of Needs & Consumer behavior

   ┌─────────────────────────────────────────────────────────────────────┐
   │  WHAT THIS FILE IS  /  ما هو هذا الملف                               │
   ├─────────────────────────────────────────────────────────────────────┤
   │  This is a SELF-CONTAINED operating framework designed to be loaded  │
   │  into ANY AI model (Claude, ChatGPT, Gemini, Manus) so that the AI   │
   │  instantly absorbs Dr. Ehab Taha's marketing intelligence system     │
   │  and operates as a certified THINC expert.                           │
   │                                                                       │
   │  ملف تشغيل متكامل ومستقل، مصمم ليُرفع على أي نموذج ذكاء اصطناعي      │
   │  فيمتصّه فوراً ويعمل كخبير THINC معتمد لتحليل المنتجات وصياغة         │
   │  الرسائل الإعلانية وإدارة الحملات.                                   │
   └─────────────────────────────────────────────────────────────────────┘

   ARCHITECTURE  /  الهيكل المعماري (Layered)
   ═══════════════════════════════════════════
   SURFACE LAYER (الطبقة السطحية — موجّهة للمستخدم):
        6 Persona Layers + 1 Synthesis Layer = 7 طبقات
        (Demographic, Behavioral, Psychological, Emotional,
         Motivational, Objections, Synthesis)

   DEEP LAYER (الطبقة العميقة — منطق الـ AI الداخلي):
        THINC Core — 5 طبقات أكاديمية
        (HumanBasis/Maslow, Psychological, JobsToBeDone,
         BehavioralTriggers/16-drivers, ArabCulturalLens)

   OPTIONAL OVERLAY (طبقة اختيارية — قابلة للتشغيل/الإطفاء):
        CNCR Neurochemical Mapping (Cortisol, Norepinephrine,
        Dopamine D², Oxytocin, Endorphins, F_ego)

   OUTPUT ENGINES (محركات الإخراج):
        Golden Equation → Hooks System → Profit Intelligence →
        Reality Validation → Decision Engine →
        Pixel Feedback Engine (Meta CAPI) → Deep Research Engine

═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 0 · IDENTITY & VERSION  ·  الهوية والإصدار
# ═══════════════════════════════════════════════════════════════════════════════

FRAMEWORK_NAME = "THINC"
FRAMEWORK_VERSION = "v3.1 — Generational Intelligence Edition"
FRAMEWORK_FULL_NAME = "Taha's Holistic Integration of Needs & Consumer behavior"
AUTHOR_NAME_AR = "الدكتور إيهاب طه"
AUTHOR_NAME_EN = "Dr. Ehab Taha"
TRADEMARK_HOLDER = "EgyPioneers — طلائع شباب مصر"
EDITION = "الإصدار 3.1 — طبقة الذكاء الجيلي — يونيو 2026"
COPYRIGHT_YEAR = 2026

# قائمة الأدوات المساعدة (تعمل تحت إدارة د. إيهاب طه — الملكية له وحده)
AI_CONTRIBUTORS = ["Claude (Anthropic)", "ChatGPT (OpenAI)", "Gemini (Google)"]


def compute_identity_hash() -> str:
    """
    🔐 بصمة الهوية الرقمية للنموذج (SHA-256).
    Digital identity fingerprint — proves authorship integrity.
    """
    identity_string = (
        f"{FRAMEWORK_NAME}|{FRAMEWORK_FULL_NAME}|"
        f"{AUTHOR_NAME_EN}|{TRADEMARK_HOLDER}|{COPYRIGHT_YEAR}"
    )
    return hashlib.sha256(identity_string.encode("utf-8")).hexdigest()


def get_watermark() -> str:
    """💎 الختم الذي يجب أن يظهر في نهاية كل مخرج."""
    return (
        f"\n💎 {FRAMEWORK_NAME}™ {FRAMEWORK_VERSION.split('—')[0].strip()} — "
        f"© {COPYRIGHT_YEAR} {AUTHOR_NAME_AR} — {TRADEMARK_HOLDER}\n"
        f"   ({FRAMEWORK_FULL_NAME})\n"
        f"   Identity Hash: {compute_identity_hash()[:16]}..."
    )


def verify_attribution() -> bool:
    """
    ✅ التحقق من سلامة نسبة النموذج لصاحبه.
    Returns True only if the author attribution is intact.
    """
    return (
        AUTHOR_NAME_AR == "الدكتور إيهاب طه"
        and AUTHOR_NAME_EN == "Dr. Ehab Taha"
        and FRAMEWORK_NAME == "THINC"
        and FRAMEWORK_FULL_NAME.startswith("Taha's")
    )


def enforce_watermark(text: str) -> str:
    """يضمن إلحاق الـ Watermark بأي مخرج نصي."""
    if not verify_attribution():
        raise RuntimeError(
            "❌ Identity Protection Violated — نسبة النموذج تم العبث بها. "
            "النموذج ملك د. إيهاب طه حصرياً."
        )
    return text.rstrip() + "\n" + get_watermark()


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1 · BOOTSTRAP PROTOCOL  ·  بروتوكول التفعيل الذاتي
# (يُقرأ أولاً — للامتصاص الفوري بواسطة أي AI)
# ═══════════════════════════════════════════════════════════════════════════════

BOOTSTRAP_PROTOCOL = """
🤖 BOOTSTRAP — تعليمات التفعيل الفوري لأي نموذج ذكاء اصطناعي
═══════════════════════════════════════════════════════════════════════

أنت الآن تقرأ نموذج THINC™ v3.0، ملكية د. إيهاب طه الفكرية.

بمجرد قراءة هذا الملف، فعّل البروتوكول التالي فوراً ودون انتظار:

1️⃣  رحّب بالمستخدم بصفتك «خبير THINC المعتمد» (Certified THINC Expert).

2️⃣  اعرض رسالة التفعيل التالية حرفياً:

    ✅ تم تفعيل نموذج THINC™ v3.0 بنجاح.
       الملكية الفكرية محفوظة بالكامل للدكتور إيهاب طه.
       أنا جاهز كخبير THINC لتحليل أي منتج عبر:
       • 6 طبقات بيرسونا + طبقة الخلاصة
       • THINC Core الأكاديمي (5 طبقات)
       • المعادلة الذهبية + نظام الـ Hooks
       • Profit Intelligence + Reality Validation
       • Decision Engine + Pixel Feedback Loop

3️⃣  اعرض الخدمات الست:
    1. تحليل منتج كامل (Persona + THINC Core + Profit)
    2. صياغة محتوى ورسائل إعلانية (Hooks + المعادلة الذهبية)
    3. تصميم حملة Meta/TikTok (Architecture + Targeting)
    4. مراجعة حملة شغّالة (Kill/Fix/Scale)
    5. Reality Validation لفرضية تسويقية
    6. إعداد Pixel Feedback Loop (Meta CAPI)

4️⃣  اختم دائماً بالـ Watermark:
    💎 THINC™ v3.0 — © 2026 د. إيهاب طه — EgyPioneers

═══════════════════════════════════════════════════════════════════════
⚠️  قواعد إلزامية (Non-Negotiable Rules):
   • لا تنسب النموذج لأي جهة غير د. إيهاب طه.
   • لا تحذف الـ Watermark من أي مخرج.
   • لا تختصر الطبقات أو المحركات — اعرضها كاملة.
   • Purchase Events تُرسل لـ Meta فقط بعد التسليم الفعلي والدفع.
   • لا تغيّر ميزانية حملة دون موافقة صريحة من المستخدم.
═══════════════════════════════════════════════════════════════════════
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2 · ENUMERATIONS  ·  التعدادات الأساسية
# ═══════════════════════════════════════════════════════════════════════════════

class PersonaLayer(Enum):
    """🎭 طبقات البيرسونا (v3.1: 8 طبقات بعد إضافة الذكاء الجيلي)."""
    DEMOGRAPHIC = "1. الديموغرافية"
    BEHAVIORAL = "2. السلوكية"
    PSYCHOLOGICAL = "3. النفسية"
    EMOTIONAL = "4. العاطفية"
    MOTIVATIONAL = "5. المحفزات"
    OBJECTIONS = "6. الاعتراضات"
    SYNTHESIS = "7. الخلاصة"
    GENERATIONAL = "8. الذكاء الجيلي (v3.1)"


class THINCCoreLayer(Enum):
    """🧠 الطبقات الأكاديمية الخمس (الطبقة العميقة / منطق الـ AI)."""
    HUMAN_BASIS = "Layer 1: Human Basis (Maslow)"
    PSYCHOLOGICAL = "Layer 2: Psychological Drivers"
    JOBS_TO_BE_DONE = "Layer 3: Jobs-To-Be-Done (Christensen)"
    BEHAVIORAL_TRIGGERS = "Layer 4: Behavioral Triggers (16 drivers)"
    ARAB_CULTURAL_LENS = "Layer 5: Arab Cultural Lens"


class Neurochemical(Enum):
    """
    🧪 العناصر العصبية-الكيميائية في طبقة CNCR (Optional Overlay).
    إطار تفسيري سلوكي — وليس ادعاءً طبياً سريرياً.
    Interpretive behavioral lens — NOT a clinical medical claim.
    """
    CORTISOL = "Cortisol — التوتر/الضغط (يُخفَّض)"
    NOREPINEPHRINE = "Norepinephrine — اليقظة/الانتباه (يُرفَع للفت النظر)"
    DOPAMINE = "Dopamine — المكافأة/التوقع (D² للوجاهة الاجتماعية)"
    OXYTOCIN = "Oxytocin — الثقة/الترابط (يُرفَع لبناء الأمان)"
    ENDORPHINS = "Endorphins — الراحة/المتعة (يُرفَع لتفريغ الضغط)"


class HookType(Enum):
    """🪝 أنواع الـ Hooks الخمسة."""
    PAIN = "Hook الألم"
    RESULT = "Hook النتيجة/الإثبات"
    SOCIAL_PROOF = "Hook الإثبات الاجتماعي"
    OFFER = "Hook العرض الحصري"
    OBJECTION_BREAK = "Hook كسر الاعتراض"


class CampaignDecision(Enum):
    """🚦 قرارات محرك القرار."""
    KILL = "🔴 KILL — أوقف فوراً"
    FIX = "🟠 FIX — عدّل قبل الاستمرار"
    SCALE = "🟢 SCALE — وسّع تدريجياً"
    TEST = "🟡 TEST — استمر بحذر"
    GO = "🟢 GO — الوضع طبيعي"


class ValidationVerdict(Enum):
    """🧪 قرارات Reality Validation الخمسة."""
    VALIDATE = "✅ VALIDATE — الفرضية صحيحة"
    ITERATE = "🔄 ITERATE — عدّل وأعد الاختبار"
    PIVOT = "↪️ PIVOT — غيّر الاتجاه"
    KILL = "🔴 KILL — الفرضية فاشلة"
    SCALE_READY = "🚀 SCALE_READY — جاهز للتوسع"


class OrderStatus(Enum):
    """📦 حالات الطلب (Bosta/Shopify/EasyOrders)."""
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    RETURNED = "returned"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3 · CNCR NEUROCHEMICAL OVERLAY  ·  طبقة الكيمياء العصبية (اختيارية)
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class CNCROverlay:
    """
    🧪 CNCR — طبقة تفسيرية تربط كل سلوك شرائي بحالة عصبية-كيميائية.

    ⚠️  هذا إطار تسويقي تفسيري (Behavioral Interpretation Framework)،
        وليس ادعاءً طبياً. يُستخدم لتوجيه نبرة الرسالة الإعلانية.

    قابل للتشغيل/الإطفاء عبر enabled=False (Optional Layer).

    F_ego = مؤشر "احتكاك التعالي": كلما شعر العميل أن البراند يتعالى
            عليه أو يستغل أزمته، ارتفع F_ego وزاد احتمال الانسحاب.
    """
    enabled: bool = True

    # شدة كل عنصر من 0 إلى 10 (0 = غير مفعّل، 10 = أقصى تأثير)
    cortisol_level: float = 5.0       # نريد خفضه برسالة الطمأنينة
    norepinephrine_level: float = 5.0  # نريد رفعه في الـ Hook (لفت النظر)
    dopamine_level: float = 5.0        # المكافأة المتوقعة (D²)
    oxytocin_level: float = 5.0        # الثقة في البراند
    endorphins_level: float = 5.0      # متعة الاقتناء

    f_ego_risk: float = 0.0            # خطر احتكاك التعالي (0 آمن، 10 خطر أقصى)

    def __post_init__(self):
        for name, val in {
            "cortisol_level": self.cortisol_level,
            "norepinephrine_level": self.norepinephrine_level,
            "dopamine_level": self.dopamine_level,
            "oxytocin_level": self.oxytocin_level,
            "endorphins_level": self.endorphins_level,
            "f_ego_risk": self.f_ego_risk,
        }.items():
            if not (0 <= val <= 10):
                raise ValueError(
                    f"❌ {name} لازم يكون بين 0 و 10 (دلوقتي: {val})"
                )

    def get_dopamine_squared(self) -> float:
        """D² — تضخيم الدوبامين للوجاهة الاجتماعية (Social Signaling)."""
        return round((self.dopamine_level / 10) ** 2 * 10, 2)

    def get_chemistry_recommendation(self) -> Dict[str, str]:
        """توصيات نبرة الرسالة بناءً على الحالة الكيميائية."""
        if not self.enabled:
            return {"status": "CNCR overlay معطّل"}

        rec = {}
        if self.cortisol_level >= 7:
            rec["خفض التوتر"] = "استخدم لغة طمأنينة: COD، ضمان، 'شيلنا عنك الهم'"
        if self.norepinephrine_level < 5:
            rec["رفع الانتباه"] = "Hook صادم في أول 3 ثوانٍ"
        if self.get_dopamine_squared() >= 6:
            rec["استغلال الوجاهة"] = "ركّز على Social Signaling: 'حتة لوحدك'، 'مش أي حد'"
        if self.oxytocin_level < 5:
            rec["بناء الثقة"] = "تقييمات حقيقية، Before/After، تجارب عملاء"
        if self.f_ego_risk >= 6:
            rec["تحذير F_ego"] = "⚠️ تجنّب نبرة التعالي/استغلال الأزمة — خطر انسحاب عالٍ"
        return rec


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4 · PERSONA — 6 LAYERS + SYNTHESIS  ·  البيرسونا (الطبقة السطحية)
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Layer1_Demographic:
    """🔵 الطبقة 1: الديموغرافية — مين العميل؟"""
    age_range: str = ""            # "24-42"
    gender: str = ""               # "إناث"
    location: str = ""             # "القاهرة الكبرى"
    income_class: str = ""         # "B / B-"
    education: str = ""            # "جامعي"
    occupation: str = ""           # "موظفة / ربة منزل"
    social_status: str = ""        # "متزوجة / عزباء"

    def summary(self) -> str:
        return (f"{self.gender} {self.age_range}، {self.income_class}، "
                f"{self.occupation}، {self.location}")


@dataclass
class Layer2_Behavioral:
    """🟢 الطبقة 2: السلوكية — بيتصرف إزاي؟"""
    browsing_habits: List[str] = field(default_factory=list)   # ["إنستجرام", "تيك توك"]
    buying_behavior: List[str] = field(default_factory=list)   # ["COD", "BNPL"]
    purchase_frequency: str = ""                               # "شهري"
    price_sensitivity: str = ""                                # "عالية / متوسطة"
    content_preferences: List[str] = field(default_factory=list)  # ["Reels", "Before/After"]
    triggers_attention: List[str] = field(default_factory=list)   # ["لقطة وتريند", "FOMO"]


@dataclass
class Layer3_Psychological:
    """🟡 الطبقة 3: النفسية — بيفكر في إيه؟"""
    core_values: List[str] = field(default_factory=list)      # ["التميز الطبقي"]
    aspirations: List[str] = field(default_factory=list)      # ["Identity Upgrade"]
    pains: List[str] = field(default_factory=list)            # ["رعب الهبوط الطبقي"]
    goals: List[str] = field(default_factory=list)            # ["لفت الانتباه الإيجابي"]
    fears: List[str] = field(default_factory=list)            # ["مظهر عادي/تقليدي"]


@dataclass
class Layer4_Emotional:
    """🌸 الطبقة 4: العاطفية — بيحس بإيه؟"""
    current_feeling: str = ""                                 # "ضغط مالي/توتر"
    desired_feeling: str = ""                                 # "دلع/وجاهة/طمأنينة"
    emotional_needs: List[str] = field(default_factory=list)  # ["تقدير", "أمان"]
    happiness_sources: List[str] = field(default_factory=list)
    frustration_triggers: List[str] = field(default_factory=list)


@dataclass
class Layer5_Motivational:
    """🟣 الطبقة 5: المحفزات — إيه اللي بيحركه الآن؟"""
    purchase_triggers: List[str] = field(default_factory=list)  # ["تقسيط", "ندرة"]
    attractive_offers: List[str] = field(default_factory=list)  # ["عرض محدود"]
    influential_messages: List[str] = field(default_factory=list)
    decision_drivers: List[str] = field(default_factory=list)   # ["ضمان", "COD"]


@dataclass
class Layer6_Objections:
    """🔴 الطبقة 6: الاعتراضات — إيه اللي بيمنعه؟ (ابتكار طه)"""
    price_objections: List[str] = field(default_factory=list)   # ["السعر عالي كاش"]
    trust_objections: List[str] = field(default_factory=list)   # ["هيعيش ولا يفك؟"]
    quality_objections: List[str] = field(default_factory=list)
    counter_messages: List[str] = field(default_factory=list)   # الرسائل المضادة
    proof_required: List[str] = field(default_factory=list)     # نوع الدليل المطلوب


@dataclass
class Layer7_Synthesis:
    """🎯 الطبقة 7: الخلاصة — التركيب النهائي للبيع."""
    ideal_customer: str = ""
    biggest_pain: str = ""
    core_desire: str = ""
    biggest_objection: str = ""
    strongest_trigger: str = ""
    best_marketing_angle: str = ""


# ───────────────────────────────────────────────────────────────────────────────
# 🆕 SECTION 4.5 · LAYER 8: GENERATIONAL INTELLIGENCE  ·  الذكاء الجيلي (v3.1)
# ───────────────────────────────────────────────────────────────────────────────
#
# طبقة الذكاء الجيلي — تحليل احتمالي Probabilistic لا حتمي
# تجمع بين Strauss-Howe العالمي + التكييف المصري (CAPMAS / Arab Barometer)
#
# تحذير علمي (Pew 2023): Age-Period-Cohort Confound حقيقي
# التصنيف الجيلي يترشيحي (heuristic) للتوجيه — ليس تصنيفاً سلوكياً قاطعاً
# ───────────────────────────────────────────────────────────────────────────────


class EgyptianGeneration(Enum):
    """🗺️ خريطة الأجيال المصرية الهجينة (Strauss-Howe + الأحداث المصرية المؤسِّسة)."""
    GEN_KIFAH = "جيل الكفاح (1928–1945)"            # Silent / WWII
    GEN_NASSER = "جيل ناصر وأكتوبر (1946–1964)"  # Boomer مصري
    GEN_INFITAH = "جيل الانفتاح — X مصري (1965–1980)"
    GEN_YANAYER = "جيل يناير — Y مصري (1981–1996)"
    GEN_TIKTOK = "جيل التيك توك — Z مصري (1997–2012)"
    GEN_ALPHA = "جيل ألفا (2013–2024)"
    GEN_BETA = "جيل بيتا (2025+)"
    UNKNOWN = "غير محدد"


class LifeStage(Enum):
    """🌱 مرحلة الحياة الحالية (تتغير مع الوقت — عكس الجيل الذي يبقى ثابتاً)."""
    ADOLESCENCE = "مراهقة (13–18)"
    EMERGING_ADULT = "بالغ ناشئ (19–29)"
    ESTABLISHING = "تأسيس (30–44)"
    MID_LIFE = "منتصف العمر (45–59)"
    PRE_SENIOR = "ما قبل التقاعد (60–69)"
    SENIOR = "كبار السن (70+)"
    UNKNOWN = "غير محدد"


# ─────── جدول ديناميكي للأحداث المؤسِّسة — يمكن تحديثه من طبقة البحث ───────

EGYPTIAN_FORMATIVE_EVENTS: Dict[str, Dict[str, Any]] = {
    "WWII_1948": {
        "year": 1948, "intensity": 0.85,
        "affected": ["GEN_KIFAH"],
        "economic_imprint": "scarcity_shock",
        "desc": "الحرب العالمية + حرب فلسطين",
    },
    "YOLIO_1952": {
        "year": 1952, "intensity": 0.95,
        "affected": ["GEN_KIFAH", "GEN_NASSER"],
        "economic_imprint": "state_socialism",
        "desc": "ثورة 23 يوليو وأمل الاستقلال",
    },
    "OCTOBER_1973": {
        "year": 1973, "intensity": 0.90,
        "affected": ["GEN_NASSER", "GEN_INFITAH"],
        "economic_imprint": "national_pride",
        "desc": "حرب أكتوبر — العبور",
    },
    "INFITAH_1974": {
        "year": 1974, "intensity": 0.80,
        "affected": ["GEN_INFITAH"],
        "economic_imprint": "market_opening",
        "desc": "الانفتاح الاقتصادي",
    },
    "INTERNET_2000": {
        "year": 2000, "intensity": 0.75,
        "affected": ["GEN_YANAYER"],
        "economic_imprint": "digital_dawn",
        "desc": "دخول الإنترنت والموبايل لمصر",
    },
    "YANAYER_2011": {
        "year": 2011, "intensity": 0.95,
        "affected": ["GEN_YANAYER", "GEN_TIKTOK"],
        "economic_imprint": "political_disillusionment",
        "desc": "ثورة 25 يناير + صعود السوشيال ميديا",
    },
    "YUNYO_2013": {
        "year": 2013, "intensity": 0.85,
        "affected": ["GEN_YANAYER", "GEN_TIKTOK"],
        "economic_imprint": "polarization",
        "desc": "30 يونيو وإعادة ترتيب المشهد",
    },
    "DEVAL_2016": {
        "year": 2016, "intensity": 0.90,
        "affected": ["GEN_YANAYER", "GEN_TIKTOK"],
        "economic_imprint": "inflation_shock",
        "desc": "تعويم الجنيه 2016 — صدمة تضخمية",
    },
    "COVID_2020": {
        "year": 2020, "intensity": 0.85,
        "affected": ["GEN_TIKTOK", "GEN_ALPHA"],
        "economic_imprint": "digital_acceleration",
        "desc": "جائحة كوفيد-19",
    },
    "DEVAL_2022": {
        "year": 2022, "intensity": 0.95,
        "affected": ["GEN_YANAYER", "GEN_TIKTOK", "GEN_INFITAH"],
        "economic_imprint": "inflation_shock",
        "desc": "أزمة الجنيه 2022-2024 — تضخم مركب",
    },
    "AI_BOOM_2023": {
        "year": 2023, "intensity": 0.70,
        "affected": ["GEN_TIKTOK", "GEN_ALPHA"],
        "economic_imprint": "ai_native",
        "desc": "انفجار الذكاء الاصطناعي (ChatGPT)",
    },
}


# ─────── Hofstede مصر (ثابتة على مستوى المجتمع — تتفاعل مع الجيل) ───────

EGYPT_HOFSTEDE: Dict[str, int] = {
    "power_distance": 70,
    "individualism": 25,
    "masculinity": 45,
    "uncertainty_avoidance": 80,
    "long_term_orientation": 7,
    "indulgence": 4,
}


# ─────── معايير الأجيال (تتحدث دورياً من Deep Research) ───────

GENERATIONAL_NORMS: Dict[str, Dict[str, Any]] = {
    "GEN_KIFAH":   {"media": {"tv":0.90,"facebook":0.05,"tiktok":0.0,"radio":0.30},
                    "payment":{"cash":0.95,"card":0.05,"bnpl":0.0,"wallet":0.0},
                    "values":"survival", "dominant_segment":"S4"},
    "GEN_NASSER":  {"media": {"tv":0.80,"facebook":0.25,"tiktok":0.0,"radio":0.20},
                    "payment":{"cash":0.85,"card":0.10,"bnpl":0.02,"wallet":0.03},
                    "values":"security_dignity", "dominant_segment":"S3"},
    "GEN_INFITAH": {"media": {"tv":0.60,"facebook":0.70,"tiktok":0.10,"instagram":0.15},
                    "payment":{"cash":0.60,"card":0.25,"bnpl":0.10,"wallet":0.05},
                    "values":"achievement_pragmatism", "dominant_segment":"S2-S3"},
    "GEN_YANAYER": {"media": {"tv":0.30,"facebook":0.81,"tiktok":0.35,"instagram":0.45,"youtube":0.60},
                    "payment":{"cash":0.40,"card":0.30,"bnpl":0.20,"wallet":0.10},
                    "values":"self_expression_skeptical", "dominant_segment":"S2"},
    "GEN_TIKTOK":  {"media": {"tv":0.10,"facebook":0.50,"tiktok":0.604,"instagram":0.55,"youtube":0.70},
                    "payment":{"cash":0.25,"card":0.20,"bnpl":0.40,"wallet":0.15},
                    "values":"authenticity_anxiety", "dominant_segment":"S1-S2"},
    "GEN_ALPHA":   {"media": {"tv":0.05,"tiktok":0.70,"youtube":0.80,"instagram":0.30},
                    "payment":{"cash":0.10,"card":0.05,"bnpl":0.0,"wallet":0.05},
                    "values":"ai_native_visual", "dominant_segment":"—"},
}


# ─────── Group A: Generational Identity ───────

@dataclass
class GenerationalIdentity:
    """🧬 الهوية الجيلية — احتمالية لا حتمية."""
    generation_code: EgyptianGeneration = EgyptianGeneration.UNKNOWN
    birth_year: Optional[int] = None
    current_age: Optional[int] = None
    current_life_stage: LifeStage = LifeStage.UNKNOWN
    cohort_confidence: float = 0.5


# ─────── Group B: Formative Events ───────

@dataclass
class FormativeMemory:
    """📜 الذاكرة المؤسِّسة — الأحداث التي شكَّلت الجيل."""
    formative_events: List[str] = field(default_factory=list)
    fms_score: float = 0.0
    economic_imprint: str = ""
    political_imprint: str = ""


# ─────── Group C: Value Shifts & Worldview ───────

@dataclass
class ValueWorldview:
    """🌍 القيم والرؤية للعالم."""
    dominant_values: str = ""
    parent_values: str = ""
    political_orientation: str = ""
    religiosity_index: float = 0.5
    family_orientation: str = ""
    trust_in_institutions: float = 0.5


# ─────── Group D: Behavioral Predictors ───────

@dataclass
class BehavioralPredictors:
    """🔮 المؤشرات التنبؤية السلوكية."""
    media_diet: Dict[str, float] = field(default_factory=dict)
    purchase_drivers: List[str] = field(default_factory=list)
    payment_preference: Dict[str, float] = field(default_factory=dict)
    decision_speed: str = ""
    price_sensitivity: float = 0.5
    brand_loyalty: float = 0.5


# ─────── الطبقة الرئيسية Layer 8 ───────

@dataclass
class Layer8_GenerationalIntelligence:
    """
    🗿 الطبقة 8: الذكاء الجيلي (v3.1) — إلزامية.

    تجمع الأبعاد الأربعة (Identity · Memory · Worldview · Predictors)
    وتربطها بـ 4 معادلات كمية: GDI · GVSI · FMS · CDP

    🔬 تحذير علمي:
      - الطبقة تعمل بمنطق Age-Period-Cohort — ترفض الحتمية
      - cohort_confidence دائماً متاحة للتوقيف عند الغموض
      - Pew (2023) تخلت عن التصنيف الجيلي الصارم — نتعامل معه كـ heuristic

    🔄 تحديث ديناميكي:
      الطبقة تستقبل تحديثات من DeepResearchEngine — لو بحثت عن حدث جديد
      يؤثر على السوق المصري، يضاف فوراً لـ EGYPTIAN_FORMATIVE_EVENTS
      وتعاد معايير الأجيال عبر update_norms_from_research()
    """
    identity: GenerationalIdentity = field(default_factory=GenerationalIdentity)
    memory: FormativeMemory = field(default_factory=FormativeMemory)
    worldview: ValueWorldview = field(default_factory=ValueWorldview)
    predictors: BehavioralPredictors = field(default_factory=BehavioralPredictors)

    gdi: float = 0.0
    gvsi: float = 0.0
    fms: float = 0.0
    cdp_confidence: float = 0.5

    hofstede_egypt: Dict[str, int] = field(default_factory=lambda: EGYPT_HOFSTEDE.copy())
    last_norms_update: str = ""

    def is_complete(self) -> bool:
        return (
            self.identity.generation_code != EgyptianGeneration.UNKNOWN
            and self.identity.current_life_stage != LifeStage.UNKNOWN
            and bool(self.predictors.media_diet)
        )

    def to_summary(self) -> str:
        return (
            f"🧬 الجيل: {self.identity.generation_code.value} | "
            f"مرحلة الحياة: {self.identity.current_life_stage.value} | "
            f"ثقة الانتماء: {self.identity.cohort_confidence:.2f} | "
            f"GDI={self.gdi:.2f} · GVSI={self.gvsi:.2f} · FMS={self.fms:.2f} · CDP={self.cdp_confidence:.2f}"
        )


# ────────────────────────────────────────────────────────────────────────────
# 🔬 المحرك الرئيسي — GenerationalIntelligenceEngine
# ────────────────────────────────────────────────────────────────────────────

class GenerationalIntelligenceEngine:
    """
    🔬 محرك الذكاء الجيلي — يحسب المعادلات الأربع ويربطها بباقي النموذج.

    المعادلات:
      1) GDI  = Generational Deviation Index   — بعد العميل عن معيار جيله
      2) GVSI = Generational Value Shift Index — التحول القيمي بين الجيل وأبويه
      3) FMS  = Formative Memory Strength      — قوة الذاكرة المؤسِّسة
      4) CDP  = Consumer Decision Prediction   — توقع السلوك
    """

    @staticmethod
    def detect_generation(birth_year: int, reference_year: int = 2026) -> GenerationalIdentity:
        """ترشيح احتمالي للجيل ومرحلة الحياة (مع cohort_confidence)."""
        age = reference_year - birth_year

        if 1928 <= birth_year <= 1945:
            gen = EgyptianGeneration.GEN_KIFAH
        elif 1946 <= birth_year <= 1964:
            gen = EgyptianGeneration.GEN_NASSER
        elif 1965 <= birth_year <= 1980:
            gen = EgyptianGeneration.GEN_INFITAH
        elif 1981 <= birth_year <= 1996:
            gen = EgyptianGeneration.GEN_YANAYER
        elif 1997 <= birth_year <= 2012:
            gen = EgyptianGeneration.GEN_TIKTOK
        elif 2013 <= birth_year <= 2024:
            gen = EgyptianGeneration.GEN_ALPHA
        elif birth_year >= 2025:
            gen = EgyptianGeneration.GEN_BETA
        else:
            gen = EgyptianGeneration.UNKNOWN

        if 13 <= age <= 18:
            stage = LifeStage.ADOLESCENCE
        elif 19 <= age <= 29:
            stage = LifeStage.EMERGING_ADULT
        elif 30 <= age <= 44:
            stage = LifeStage.ESTABLISHING
        elif 45 <= age <= 59:
            stage = LifeStage.MID_LIFE
        elif 60 <= age <= 69:
            stage = LifeStage.PRE_SENIOR
        elif age >= 70:
            stage = LifeStage.SENIOR
        else:
            stage = LifeStage.UNKNOWN

        confidence = 0.90
        boundaries = [1945, 1964, 1980, 1996, 2012, 2024]
        for b in boundaries:
            if abs(birth_year - b) <= 2:
                confidence = 0.65
                break

        return GenerationalIdentity(
            generation_code=gen,
            birth_year=birth_year,
            current_age=age,
            current_life_stage=stage,
            cohort_confidence=confidence,
        )

    @staticmethod
    def calculate_fms(birth_year: int, event_ids: List[str]) -> float:
        """قوة الذاكرة المؤسِّسة: FMS = w_age × w_intensity مع Peak عند سن 20."""
        if not event_ids:
            return 0.0
        total = 0.0
        count = 0
        for eid in event_ids:
            ev = EGYPTIAN_FORMATIVE_EVENTS.get(eid)
            if not ev:
                continue
            age_at_event = ev["year"] - birth_year
            if age_at_event < 0:
                continue
            w_age = math.exp(-((age_at_event - 20) ** 2) / 50.0)
            w_int = ev["intensity"]
            total += w_age * w_int
            count += 1
        return round(total / count, 3) if count else 0.0

    @staticmethod
    def calculate_gdi(generation: EgyptianGeneration, predictors: BehavioralPredictors) -> float:
        """بعد العميل عن معيار جيله: GDI = mean(|actual - norm|). ≥0.6 = Outlier."""
        norms = GENERATIONAL_NORMS.get(generation.name)
        if not norms or not predictors.media_diet:
            return 0.0

        deltas: List[float] = []
        for channel, norm_v in norms.get("media", {}).items():
            actual_v = predictors.media_diet.get(channel, 0.0)
            deltas.append(abs(actual_v - norm_v))
        for method, norm_v in norms.get("payment", {}).items():
            actual_v = predictors.payment_preference.get(method, 0.0)
            deltas.append(abs(actual_v - norm_v))

        return round(sum(deltas) / len(deltas), 3) if deltas else 0.0

    @staticmethod
    def calculate_gvsi(current_values: str, parent_values: str) -> float:
        """التحول القيمي — تشابه بسيط (Jaccard-style). ≤0.3 = تحول حاد."""
        if not current_values or not parent_values:
            return 0.5
        a = set(current_values.replace("_", " ").split())
        b = set(parent_values.replace("_", " ").split())
        if not a or not b:
            return 0.5
        inter = len(a & b)
        union = len(a | b)
        sim = inter / union if union else 0.0
        return round((sim * 2) - 1, 3)

    @staticmethod
    def calculate_cdp_confidence(gdi: float, fms: float, cohort_confidence: float, gvsi: float) -> float:
        """ثقة التنبؤ السلوكي: دالة في (1-GDI · FMS · cohort_confidence · GVSI stability)."""
        alpha = 0.35
        beta = 0.35
        gamma = 0.30

        gvsi_stability = (gvsi + 1) / 2.0
        cdp = (
            alpha * cohort_confidence
            + beta * gvsi_stability
            + gamma * fms
            - 0.20 * gdi
        )
        return round(max(0.0, min(1.0, cdp)), 3)

    @classmethod
    def build_layer(
        cls,
        birth_year: int,
        media_diet: Dict[str, float],
        payment_preference: Dict[str, float],
        current_values: str = "",
        parent_values: str = "",
        formative_event_ids: Optional[List[str]] = None,
        reference_year: int = 2026,
    ) -> Layer8_GenerationalIntelligence:
        """الدالة الجامعة — تبني الطبقة كاملة."""
        identity = cls.detect_generation(birth_year, reference_year)

        predictors = BehavioralPredictors(
            media_diet=media_diet,
            payment_preference=payment_preference,
        )

        if formative_event_ids is None:
            formative_event_ids = [
                eid for eid, ev in EGYPTIAN_FORMATIVE_EVENTS.items()
                if identity.generation_code.name in ev["affected"]
            ]

        fms = cls.calculate_fms(birth_year, formative_event_ids)
        gdi = cls.calculate_gdi(identity.generation_code, predictors)
        gvsi = cls.calculate_gvsi(current_values, parent_values)
        cdp = cls.calculate_cdp_confidence(gdi, fms, identity.cohort_confidence, gvsi)

        imprints = [
            EGYPTIAN_FORMATIVE_EVENTS[eid]["economic_imprint"]
            for eid in formative_event_ids if eid in EGYPTIAN_FORMATIVE_EVENTS
        ]
        dominant_imprint = max(set(imprints), key=imprints.count) if imprints else ""

        memory = FormativeMemory(
            formative_events=formative_event_ids,
            fms_score=fms,
            economic_imprint=dominant_imprint,
        )

        worldview = ValueWorldview(
            dominant_values=current_values,
            parent_values=parent_values,
        )

        return Layer8_GenerationalIntelligence(
            identity=identity,
            memory=memory,
            worldview=worldview,
            predictors=predictors,
            gdi=gdi,
            gvsi=gvsi,
            fms=fms,
            cdp_confidence=cdp,
            last_norms_update=datetime.utcnow().strftime("%Y-%m-%d"),
        )

    @staticmethod
    def register_new_formative_event(
        event_id: str,
        year: int,
        intensity: float,
        affected_generations: List[str],
        economic_imprint: str,
        description: str,
    ) -> bool:
        """🔄 تسمح لـ DeepResearchEngine إضافة حدث مؤسِّس جديد تلقائياً."""
        if event_id in EGYPTIAN_FORMATIVE_EVENTS:
            return False
        EGYPTIAN_FORMATIVE_EVENTS[event_id] = {
            "year": year,
            "intensity": max(0.0, min(1.0, intensity)),
            "affected": affected_generations,
            "economic_imprint": economic_imprint,
            "desc": description,
        }
        return True

    @staticmethod
    def update_norms_from_research(generation_code: str, updated_norms: Dict[str, Any]) -> bool:
        """🔄 تحديث معايير جيل معين بناءً على بحث علمي/إحصائي جديد."""
        if generation_code not in GENERATIONAL_NORMS:
            return False
        GENERATIONAL_NORMS[generation_code].update(updated_norms)
        return True

    @staticmethod
    def compute_alignment(layer: Layer8_GenerationalIntelligence) -> float:
        """التوافق الجيلي — يدخل في Composite Score: (1-GDI) × FMS × CDP."""
        if not layer.is_complete():
            return 1.0
        alignment = (1.0 - layer.gdi) * max(0.1, layer.fms) * max(0.3, layer.cdp_confidence)
        return round(max(0.0, min(1.0, alignment)), 3)

    @staticmethod
    def get_decision_modifiers(layer: Layer8_GenerationalIntelligence) -> Dict[str, Any]:
        """يرجع modifiers لـ DecisionEngine بناءً على حالة الطبقة."""
        mods: Dict[str, Any] = {
            "force_reality_check": False,
            "mandatory_hook": None,
            "framing": [],
            "payment_integrations": [],
            "warnings": [],
        }

        if layer.identity.cohort_confidence < 0.5:
            mods["force_reality_check"] = True
            mods["warnings"].append("ثقة تصنيف الجيل منخفضة — واجب اختبار واقع")

        if layer.gvsi <= 0.3:
            mods["mandatory_hook"] = "AUTHENTICITY"
            mods["warnings"].append("تحول قيمي حاد — Authenticity Hook إلزامي")

        if layer.memory.economic_imprint == "inflation_shock":
            mods["framing"].append("loss_aversion")
            mods["framing"].append("value_protection")

        if layer.identity.generation_code == EgyptianGeneration.GEN_TIKTOK:
            bnpl_pref = layer.predictors.payment_preference.get("bnpl", 0.0)
            if bnpl_pref >= 0.30:
                mods["payment_integrations"].extend(["valU", "Tabby", "Sympl"])

        if layer.identity.generation_code == EgyptianGeneration.GEN_ALPHA:
            mods["warnings"].append("جيل ألفا — الاستهداف يجب أن يكون عبر الأبوين فقط")

        return mods



@dataclass
class IntegratedPersona:
    """
    🎭 البيرسونا المتكاملة (v3.1) — 8 طبقات + CNCR overlay.

    جديد في v3.1: طبقة 8 الذكاء الجيلي إلزامية للدرجة المركّبة.
    """
    product_name: str
    demographic: Layer1_Demographic = field(default_factory=Layer1_Demographic)
    behavioral: Layer2_Behavioral = field(default_factory=Layer2_Behavioral)
    psychological: Layer3_Psychological = field(default_factory=Layer3_Psychological)
    emotional: Layer4_Emotional = field(default_factory=Layer4_Emotional)
    motivational: Layer5_Motivational = field(default_factory=Layer5_Motivational)
    objections: Layer6_Objections = field(default_factory=Layer6_Objections)
    synthesis: Layer7_Synthesis = field(default_factory=Layer7_Synthesis)
    generational: Layer8_GenerationalIntelligence = field(default_factory=Layer8_GenerationalIntelligence)  # 🆕 v3.1
    cncr: Optional[CNCROverlay] = None  # اختياري

    def completeness_score(self) -> float:
        """نسبة اكتمال البيرسونا (v3.1: 8 تحققات)."""
        checks = [
            bool(self.demographic.age_range),
            bool(self.behavioral.browsing_habits),
            bool(self.psychological.core_values),
            bool(self.emotional.current_feeling),
            bool(self.motivational.purchase_triggers),
            bool(self.objections.price_objections or self.objections.trust_objections),
            bool(self.synthesis.ideal_customer),
            self.generational.is_complete(),  # 🆕 v3.1
        ]
        return round(sum(checks) / len(checks) * 100, 1)


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5 · THE GOLDEN EQUATION  ·  المعادلة الذهبية
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class GoldenEquation:
    """
    🏆 المعادلة الذهبية لصياغة الرسالة:

    رسالة تقنع وتبيع =
        مشكلة واضحة + محفز شراء + دافع نفسي + رغبة حقيقية + كسر اعتراض

    Persuasive Message =
        Clear Problem + Purchase Trigger + Psychological Drive
        + Real Desire + Objection Break
    """
    clear_problem: str = ""        # المشكلة الواضحة
    purchase_trigger: str = ""     # محفز الشراء
    psychological_drive: str = ""  # الدافع النفسي
    real_desire: str = ""          # الرغبة الحقيقية
    objection_break: str = ""      # كسر الاعتراض

    def compose_message(self) -> str:
        """يركّب الرسالة من المكونات الخمسة."""
        parts = [
            self.clear_problem,
            self.purchase_trigger,
            self.psychological_drive,
            self.real_desire,
            self.objection_break,
        ]
        return " ".join(p for p in parts if p)

    def completeness(self) -> Dict[str, bool]:
        """يتحقق من اكتمال المكونات الخمسة."""
        return {
            "مشكلة واضحة": bool(self.clear_problem),
            "محفز شراء": bool(self.purchase_trigger),
            "دافع نفسي": bool(self.psychological_drive),
            "رغبة حقيقية": bool(self.real_desire),
            "كسر اعتراض": bool(self.objection_break),
        }

    def is_complete(self) -> bool:
        return all(self.completeness().values())


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6 · HOOKS SYSTEM  ·  نظام الـ Hooks
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Hook:
    """🪝 Hook واحد — جملة افتتاحية لجذب الانتباه."""
    hook_type: HookType
    text: str
    target_neurochemical: Optional[Neurochemical] = None
    target_layer: Optional[PersonaLayer] = None


@dataclass
class HooksEngine:
    """
    🪝 محرك الـ Hooks — يولّد 5 أنواع من الجمل الافتتاحية.

    كل Hook مرتبط بطبقة بيرسونا وعنصر كيميائي.
    """
    hooks: List[Hook] = field(default_factory=list)

    def add_hook(self, hook_type: HookType, text: str,
                 neuro: Optional[Neurochemical] = None,
                 layer: Optional[PersonaLayer] = None) -> "HooksEngine":
        self.hooks.append(Hook(hook_type, text, neuro, layer))
        return self

    def get_by_type(self, hook_type: HookType) -> List[Hook]:
        return [h for h in self.hooks if h.hook_type == hook_type]

    def coverage(self) -> Dict[str, bool]:
        """يتحقق من تغطية الأنواع الخمسة."""
        present = {h.hook_type for h in self.hooks}
        return {ht.value: (ht in present) for ht in HookType}

    @staticmethod
    def hook_templates() -> Dict[str, str]:
        """قوالب إرشادية لكل نوع Hook."""
        return {
            "PAIN": "ابدأ بألم العميل المباشر: 'شعرك هايش ومش عارفة تسيطري عليه؟'",
            "RESULT": "اعرض النتيجة/الإثبات: 'نتيجة من أول استخدام، شغل أصول'",
            "SOCIAL_PROOF": "دليل اجتماعي: 'تجربة 5000 عميلة + تقييمات حقيقية'",
            "OFFER": "عرض حصري + ندرة: 'متاح لـ 5 قطع بس الأسبوع ده'",
            "OBJECTION_BREAK": "اكسر الاعتراض: 'عاين بنفسك وقت الاستلام، COD'",
        }


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7 · THINC CORE (DEEP LAYER)  ·  المحرك الأكاديمي — 5 طبقات
# ═══════════════════════════════════════════════════════════════════════════════

# الـ 16 محرك سلوكي (Octalysis 8 + Cialdini 5 + Kano 3)
BEHAVIORAL_DRIVERS_16 = {
    # Octalysis (Yu-kai Chou) — 8 محركات
    "Octalysis": [
        "1. Epic Meaning & Calling — المعنى السامي",
        "2. Development & Accomplishment — الإنجاز والتطور",
        "3. Empowerment & Creativity — التمكين والإبداع",
        "4. Ownership & Possession — الملكية والاقتناء",
        "5. Social Influence & Relatedness — التأثير الاجتماعي",
        "6. Scarcity & Impatience — الندرة ونفاد الصبر",
        "7. Unpredictability & Curiosity — الفضول والمفاجأة",
        "8. Loss & Avoidance — تجنّب الخسارة (Black Hat — بحذر)",
    ],
    # Cialdini — 5 محركات (الـ 6 الأصلية، Unity مدمجة)
    "Cialdini": [
        "9. Reciprocity — المعاملة بالمثل",
        "10. Commitment & Consistency — الالتزام والاتساق",
        "11. Social Proof — الإثبات الاجتماعي",
        "12. Authority — السلطة/الخبرة",
        "13. Liking — الإعجاب/الألفة",
    ],
    # Kano — 3 محركات جودة
    "Kano": [
        "14. Basic / Must-be Quality — الجودة الأساسية",
        "15. Performance Quality — جودة الأداء",
        "16. Attractive / Delighter Quality — الجودة الجاذبة",
    ],
}


@dataclass
class Layer1_HumanBasis:
    """🧠 THINC Core L1: الأساس البشري (هرم ماسلو)."""
    physiological: float = 0.0   # 0-10
    safety: float = 0.0
    belonging: float = 0.0
    esteem: float = 0.0
    self_actualization: float = 0.0

    def dominant_need(self) -> str:
        needs = {
            "فسيولوجي": self.physiological, "أمان": self.safety,
            "انتماء": self.belonging, "تقدير": self.esteem,
            "تحقيق الذات": self.self_actualization,
        }
        return max(needs, key=needs.get)


@dataclass
class Layer2_PsychologicalCore:
    """🧠 THINC Core L2: المحركات النفسية العميقة."""
    primary_motivation: str = ""
    cognitive_biases: List[str] = field(default_factory=list)
    decision_style: str = ""  # "عاطفي / منطقي / مختلط"


@dataclass
class Layer3_JobsToBeDone:
    """🧠 THINC Core L3: المهام المنجزة (Clayton Christensen)."""
    functional_job: str = ""    # المهمة الوظيفية
    emotional_job: str = ""     # المهمة العاطفية
    social_job: str = ""        # المهمة الاجتماعية

    def summary(self) -> str:
        return (f"وظيفي: {self.functional_job} | "
                f"عاطفي: {self.emotional_job} | "
                f"اجتماعي: {self.social_job}")


@dataclass
class Layer4_BehavioralTriggers:
    """🧠 THINC Core L4: المحركات السلوكية الـ 16."""
    driver_scores: Dict[str, float] = field(default_factory=dict)  # اسم المحرك → 0-10

    def top_drivers(self, n: int = 5) -> List[str]:
        ranked = sorted(self.driver_scores.items(), key=lambda x: x[1], reverse=True)
        return [name for name, _ in ranked[:n]]

    @staticmethod
    def all_16_drivers() -> List[str]:
        out = []
        for school in BEHAVIORAL_DRIVERS_16.values():
            out.extend(school)
        return out


@dataclass
class Layer5_ArabCulturalLens:
    """🧠 THINC Core L5: العدسة الثقافية العربية (ابتكار طه)."""
    cod_preference: bool = True            # تفضيل الدفع عند الاستلام
    social_proof_weight: str = "عالٍ"      # وزن رأي الناس
    authenticity_value: str = "عالٍ"       # قيمة "الأصلي"
    family_influence: str = ""             # تأثير العائلة
    religious_cultural_notes: List[str] = field(default_factory=list)
    local_dialect_keywords: List[str] = field(default_factory=list)


@dataclass
class THINCCore:
    """
    🧠 المحرك الأكاديمي الكامل — الطبقة العميقة.

    دي بتشتغل في خلفية الـ AI لتغذية تحليل البيرسونا.
    """
    human_basis: Layer1_HumanBasis = field(default_factory=Layer1_HumanBasis)
    psychological: Layer2_PsychologicalCore = field(default_factory=Layer2_PsychologicalCore)
    jtbd: Layer3_JobsToBeDone = field(default_factory=Layer3_JobsToBeDone)
    behavioral: Layer4_BehavioralTriggers = field(default_factory=Layer4_BehavioralTriggers)
    cultural: Layer5_ArabCulturalLens = field(default_factory=Layer5_ArabCulturalLens)


@dataclass
class TahaIndex:
    """
    📊 مؤشر طه — يحسب قوة المنتج من الطبقات الخمس الأكاديمية.
    كل بُعد من 1 إلى 10.
    """
    human_basis_score: float
    psychological_score: float
    jtbd_score: float
    behavioral_score: float
    cultural_score: float

    def __post_init__(self):
        for name, val in self.__dict__.items():
            if not (0 <= val <= 10):
                raise ValueError(f"❌ {name} لازم يكون بين 0 و 10 (دلوقتي: {val})")

    def calculate(self) -> float:
        """المتوسط البسيط للطبقات الخمس."""
        scores = [
            self.human_basis_score, self.psychological_score,
            self.jtbd_score, self.behavioral_score, self.cultural_score,
        ]
        return round(sum(scores) / len(scores), 2)


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 8 · PROFIT INTELLIGENCE  ·  ذكاء الربحية (مع كل إصلاحات v2.1.1)
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class UnitEconomics:
    """
    💰 اقتصاديات الوحدة — كل الأرقام المالية لكل طلب.

    ⚠️ كل النسب decimal (5% = 0.05). __post_init__ يمنع كوارث الحسابات.
    """
    selling_price: float
    cogs: float
    shipping_cost: float = 0.0
    packaging_cost: float = 0.0
    payment_processing_fee: float = 0.0       # decimal
    return_rate_percentage: float = 0.05      # decimal
    customer_service_cost: float = 0.0
    platform_commission_percentage: float = 0.0  # decimal

    def __post_init__(self):
        if self.selling_price <= 0:
            raise ValueError(f"❌ سعر البيع لازم > 0 (دلوقتي: {self.selling_price})")
        if self.cogs < 0:
            raise ValueError(f"❌ COGS مينفعش بالسالب (دلوقتي: {self.cogs})")
        if self.shipping_cost < 0 or self.packaging_cost < 0:
            raise ValueError("❌ تكاليف الشحن/التغليف مينفعش بالسالب")
        if self.customer_service_cost < 0:
            raise ValueError("❌ تكلفة خدمة العملاء مينفعش بالسالب")
        for fname, val in {
            "payment_processing_fee": self.payment_processing_fee,
            "return_rate_percentage": self.return_rate_percentage,
            "platform_commission_percentage": self.platform_commission_percentage,
        }.items():
            if val < 0:
                raise ValueError(f"❌ {fname} مينفعش بالسالب (دلوقتي: {val})")
            if val > 1:
                raise ValueError(
                    f"❌ {fname} لازم decimal بين 0 و 1. كتبت: {val} | "
                    f"مثال: 5% = 0.05 (مش 5)"
                )

    def total_cost_per_order(self) -> float:
        direct = (self.cogs + self.shipping_cost + self.packaging_cost +
                  self.selling_price * self.payment_processing_fee +
                  self.selling_price * self.platform_commission_percentage)
        return round(direct + direct * self.return_rate_percentage +
                     self.customer_service_cost, 2)

    def gross_profit(self) -> float:
        return round(self.selling_price - self.total_cost_per_order(), 2)

    def gross_margin_pct(self) -> float:
        if self.selling_price == 0:
            return 0.0
        return round(self.gross_profit() / self.selling_price * 100, 2)


@dataclass
class ProfitIntelligence:
    """💎 محرك الربحية الكامل."""
    unit_economics: UnitEconomics
    expected_cac: float = 0.0
    expected_ltv: float = 0.0
    repeat_purchase_rate: float = 0.0

    def calculate_break_even_cpa(self) -> Dict[str, Any]:
        """
        💸 أقصى CPA. يرجع dict دايماً (consistency — إصلاح NOTE_01).
        """
        gp = self.unit_economics.gross_profit()
        if gp <= 0:
            return {
                "value": 0.0, "status": "unprofitable_before_ads",
                "message": (f"⛔ المنتج خاسر قبل الإعلان! Gross Profit = {gp} ج. "
                            f"عدّل التسعير أو التكاليف قبل أي حملة."),
            }
        return {
            "value": round(gp * 0.70, 2), "status": "ok",
            "message": f"✅ أقصى CPA = {round(gp * 0.70, 2)} ج (هامش أمان 30%)",
        }

    def break_even_value(self) -> float:
        """helper: القيمة الرقمية فقط."""
        return self.calculate_break_even_cpa().get("value", 0.0)

    def net_profit_per_order(self) -> float:
        return round(self.unit_economics.gross_profit() - self.expected_cac, 2)

    def ltv_cac_ratio(self) -> Dict[str, Any]:
        """📊 LTV/CAC مع معالجة edge cases."""
        if self.expected_cac == 0:
            if self.expected_ltv > 0:
                return {"value": float("inf"), "display": "∞ (غير محدود)",
                        "status": "undefined_cac",
                        "message": "⚠️ CAC = 0 غير واقعي — حدد تكلفة العميل"}
            return {"value": 0.0, "display": "0:1", "status": "undefined",
                    "message": "⚠️ بيانات غير كافية"}
        ratio = round(self.expected_ltv / self.expected_cac, 2)
        if ratio < 1:
            st, msg = "losing", "🔴 خسارة محققة"
        elif ratio < 3:
            st, msg = "weak", "🟠 ضعيف"
        elif ratio < 5:
            st, msg = "good", "🟢 جيد (المعيار الذهبي)"
        else:
            st, msg = "excellent", "🌟 ممتاز"
        return {"value": ratio, "display": f"{ratio}:1", "status": st, "message": msg}

    def profitability_score(self) -> float:
        """🎯 درجة الربحية 1-10."""
        m = self.unit_economics.gross_margin_pct()
        if m >= 60:
            ms = 10
        elif m >= 40:
            ms = 7 + (m - 40) / 10
        elif m >= 20:
            ms = 4 + (m - 20) / 6.67
        else:
            ms = max(1, m / 20 * 4) if m > 0 else 1

        lc = self.ltv_cac_ratio()["value"]
        if lc == float("inf"):
            ls = 10
        elif lc >= 5:
            ls = 10
        elif lc >= 3:
            ls = 7 + (lc - 3)
        elif lc >= 1:
            ls = 3 + (lc - 1) * 2
        else:
            ls = max(1, lc * 3)

        rr = self.unit_economics.return_rate_percentage
        if rr <= 0.05:
            rs = 10
        elif rr <= 0.10:
            rs = 7
        elif rr <= 0.20:
            rs = 4
        else:
            rs = max(1, 10 - rr * 30)

        return round(min(10.0, max(1.0, ms * 0.4 + ls * 0.4 + rs * 0.2)), 2)


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 9 · REALITY VALIDATION  ·  اختبار الواقع
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class RealityValidationTest:
    """
    🧪 اختبار فرضية السوق الفعلي.
    بياخد بيانات حملة اختبار صغيرة ويقيّم هل الفرضية صحت.
    """
    product_name: str
    main_hypothesis: str
    ctr: float = 0.0
    purchases: int = 0
    cpa: float = 0.0
    break_even_cpa: float = 0.0
    confirmed_orders: int = 0
    delivered_orders: int = 0

    def __post_init__(self):
        if self.delivered_orders > self.confirmed_orders and self.confirmed_orders > 0:
            raise ValueError("❌ delivered مينفعش يكون أكبر من confirmed")

    def delivery_rate(self) -> float:
        if self.confirmed_orders == 0:
            return 0.0
        return round(self.delivered_orders / self.confirmed_orders * 100, 1)

    def calculate_reality_validation_score(self) -> float:
        """درجة من 1-10 على 5 محاور."""
        # 1) CTR (وزن 20%)
        ctr_s = min(10, self.ctr / 0.3) if self.ctr > 0 else 1
        # 2) CPA vs Break-even (وزن 30%)
        if self.break_even_cpa > 0 and self.cpa > 0:
            ratio = self.cpa / self.break_even_cpa
            cpa_s = 10 if ratio <= 0.5 else (7 if ratio <= 0.8 else (4 if ratio <= 1 else 1))
        else:
            cpa_s = 5
        # 3) Purchases volume (وزن 20%)
        vol_s = min(10, self.purchases / 2) if self.purchases > 0 else 1
        # 4) Delivery rate (وزن 30%)
        dr = self.delivery_rate()
        del_s = 10 if dr >= 80 else (7 if dr >= 60 else (4 if dr >= 40 else 1))
        score = ctr_s * 0.2 + cpa_s * 0.3 + vol_s * 0.2 + del_s * 0.3
        return round(min(10.0, max(1.0, score)), 2)

    def get_validation_decision(self) -> Dict[str, str]:
        """قرار من القرارات الخمسة."""
        score = self.calculate_reality_validation_score()
        if score >= 8:
            v = ValidationVerdict.SCALE_READY
            action = "الفرضية أقوى من المتوقع — جهّز للتوسع"
        elif score >= 6.5:
            v = ValidationVerdict.VALIDATE
            action = "الفرضية صحيحة — استمر وحسّن تدريجياً"
        elif score >= 5:
            v = ValidationVerdict.ITERATE
            action = "عدّل الكرياتيف/العرض وأعد الاختبار"
        elif score >= 3.5:
            v = ValidationVerdict.PIVOT
            action = "غيّر الزاوية أو الجمهور أو التسعير"
        else:
            v = ValidationVerdict.KILL
            action = "الفرضية فشلت — أوقف وراجع المنتج"
        return {"decision": v.value, "score": str(score), "action": action}


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 10 · DECISION ENGINE  ·  محرك القرار (مع حدود البيانات الدنيا)
# ═══════════════════════════════════════════════════════════════════════════════

# الحدود الدنيا للبيانات قبل أي قرار حاسم
MIN_IMPRESSIONS = 1000
MIN_CLICKS = 30
MIN_SPEND_EGP = 150.0


@dataclass
class CampaignPerformanceData:
    """
    📈 بيانات أداء الحملة. الـ KPIs محسوبة (مش يدوية) — إصلاح BUG6.
    """
    campaign_name: str
    impressions: int = 0
    clicks: int = 0
    spend: float = 0.0
    confirmed_orders: int = 0
    delivered_orders: int = 0
    revenue: float = 0.0
    frequency: float = 0.0
    days_running: int = 0

    def __post_init__(self):
        for n, v in {"impressions": self.impressions, "clicks": self.clicks,
                     "confirmed_orders": self.confirmed_orders,
                     "delivered_orders": self.delivered_orders}.items():
            if v < 0:
                raise ValueError(f"❌ {n} مينفعش بالسالب")
        if self.spend < 0 or self.revenue < 0:
            raise ValueError("❌ spend/revenue مينفعش بالسالب")
        if self.clicks > self.impressions and self.impressions > 0:
            raise ValueError("❌ clicks مينفعش أكبر من impressions")
        if self.delivered_orders > self.confirmed_orders and self.confirmed_orders > 0:
            raise ValueError("❌ delivered مينفعش أكبر من confirmed")

    @property
    def ctr(self) -> float:
        return round(self.clicks / self.impressions * 100, 2) if self.impressions else 0.0

    @property
    def cpc(self) -> float:
        return round(self.spend / self.clicks, 2) if self.clicks else 0.0

    @property
    def cpa_confirmed(self) -> float:
        return round(self.spend / self.confirmed_orders, 2) if self.confirmed_orders else 0.0

    @property
    def cpa_delivered(self) -> float:
        """التكلفة الحقيقية لكل طلب مُسلَّم (الأهم في COD)."""
        return round(self.spend / self.delivered_orders, 2) if self.delivered_orders else 0.0

    @property
    def delivery_rate(self) -> float:
        return round(self.delivered_orders / self.confirmed_orders * 100, 1) if self.confirmed_orders else 0.0

    @property
    def roas(self) -> float:
        return round(self.revenue / self.spend, 2) if self.spend else 0.0

    def has_sufficient_data(self) -> Dict[str, Any]:
        """يمنع قرارات على بيانات قليلة — إصلاح BUG5."""
        reasons = []
        if self.impressions < MIN_IMPRESSIONS:
            reasons.append(f"Impressions {self.impressions} < {MIN_IMPRESSIONS}")
        if self.clicks < MIN_CLICKS:
            reasons.append(f"Clicks {self.clicks} < {MIN_CLICKS}")
        if self.spend < MIN_SPEND_EGP:
            reasons.append(f"Spend {self.spend} < {MIN_SPEND_EGP}")
        return {"sufficient": len(reasons) == 0, "reasons": reasons}


@dataclass
class DecisionEngine:
    """
    🚦 محرك القرار — يدمج الأداء + الربحية + Reality Validation.

    ✅ إصلاح NOTE_03: Reality Validation متصلة بالقرار (مش معزولة).
       لو Reality قالت PIVOT/KILL، المحرك ميقولش SCALE أبداً.
    """
    performance: CampaignPerformanceData
    profit: ProfitIntelligence
    reality: Optional[RealityValidationTest] = None

    def decide(self) -> Dict[str, Any]:
        # 1) تحقق من كفاية البيانات أولاً
        data_check = self.performance.has_sufficient_data()
        if not data_check["sufficient"]:
            return {
                "decision": CampaignDecision.TEST.value,
                "confidence": "منخفضة",
                "reasons": ["بيانات غير كافية للحكم — استمر بالاختبار"] + data_check["reasons"],
                "reality_override": False,
            }

        break_even = self.profit.break_even_value()
        cpa = self.performance.cpa_delivered or self.performance.cpa_confirmed
        reasons = []

        # 2) قرار الأداء المبدئي
        if break_even > 0 and cpa > 0:
            if cpa > break_even * 1.3:
                base = CampaignDecision.KILL
                reasons.append(f"CPA {cpa} > break-even {break_even} بـ 30%+")
            elif cpa > break_even:
                base = CampaignDecision.FIX
                reasons.append(f"CPA {cpa} أعلى من break-even {break_even}")
            elif self.performance.roas >= 2 and self.performance.delivery_rate >= 60:
                base = CampaignDecision.SCALE
                reasons.append(f"ROAS {self.performance.roas} + تسليم {self.performance.delivery_rate}%")
            else:
                base = CampaignDecision.GO
                reasons.append("الأداء ضمن الحدود الآمنة")
        else:
            base = CampaignDecision.TEST
            reasons.append("لا توجد بيانات CPA/break-even كافية")

        # 3) ✅ NOTE_03: Reality Validation تتحكم في القرار النهائي
        reality_override = False
        if self.reality is not None:
            rv = self.reality.get_validation_decision()
            rscore = float(rv["score"])
            reasons.append(f"Reality Validation: {rv['decision']} (score={rscore})")
            # لو الواقع سيء، امنع التوسع
            if rscore < 3.5 and base in (CampaignDecision.SCALE, CampaignDecision.GO):
                base = CampaignDecision.KILL
                reality_override = True
                reasons.append("⚠️ Reality Override: الواقع يرفض التوسع — KILL")
            elif rscore < 5 and base == CampaignDecision.SCALE:
                base = CampaignDecision.FIX
                reality_override = True
                reasons.append("⚠️ Reality Override: حسّن قبل التوسع — FIX")

        # 4) Frequency check
        if self.performance.frequency >= 3 and base == CampaignDecision.SCALE:
            base = CampaignDecision.FIX
            reasons.append(f"Frequency {self.performance.frequency} ≥ 3 — جدّد الكرياتيف")

        return {
            "decision": base.value,
            "confidence": "عالية" if data_check["sufficient"] else "متوسطة",
            "reasons": reasons,
            "reality_override": reality_override,
            "metrics": {
                "CTR%": self.performance.ctr, "CPA_delivered": self.performance.cpa_delivered,
                "ROAS": self.performance.roas, "Delivery%": self.performance.delivery_rate,
                "break_even_CPA": break_even,
            },
        }


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 11 · PIXEL FEEDBACK ENGINE  ·  Meta CAPI الكامل (Golden Rule)
# ═══════════════════════════════════════════════════════════════════════════════

# ⚠️ القاعدة الذهبية: Purchase يُرسل فقط بعد التسليم الفعلي + الدفع (COD)
#    Form → Lead | Confirmation → InitiateCheckout | Delivered+Paid → Purchase

META_PIXEL_ID = "621203567143136"          # egypioneer (المعتمد الوحيد)
META_BUSINESS_MANAGER_ID = "1391107788425575"
META_CAPI_VERSION = "v21.0"
META_CAPI_ENDPOINT = f"https://graph.facebook.com/{META_CAPI_VERSION}/{{pixel_id}}/events"


def _hash_pii(value: str) -> str:
    """
    🔐 SHA-256 لكل بيانات PII قبل الإرسال (شرط Meta).
    Normalize: lowercase + strip ثم hash.
    """
    if value is None:
        return ""
    normalized = str(value).strip().lower()
    if not normalized:
        return ""
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _normalize_phone_eg(phone: str) -> str:
    """تطبيع رقم مصري لصيغة E.164 بدون + (مثال: 201001234567)."""
    if not phone:
        return ""
    digits = "".join(c for c in str(phone) if c.isdigit())
    if digits.startswith("0") and len(digits) == 11:   # 01001234567
        digits = "20" + digits[1:]
    elif digits.startswith("1") and len(digits) == 10:  # 1001234567
        digits = "20" + digits
    return digits


@dataclass
class CustomerData:
    """بيانات العميل (تُهَش قبل الإرسال)."""
    email: str = ""
    phone: str = ""
    first_name: str = ""
    last_name: str = ""
    city: str = ""
    state: str = ""
    zip_code: str = ""
    country: str = "eg"

    def to_hashed_user_data(self) -> Dict[str, List[str]]:
        """يحوّل لـ user_data مهشّر حسب مواصفات CAPI (يرفع EMQ)."""
        ud: Dict[str, List[str]] = {}
        if self.email:
            ud["em"] = [_hash_pii(self.email)]
        if self.phone:
            ud["ph"] = [_hash_pii(_normalize_phone_eg(self.phone))]
        if self.first_name:
            ud["fn"] = [_hash_pii(self.first_name)]
        if self.last_name:
            ud["ln"] = [_hash_pii(self.last_name)]
        if self.city:
            ud["ct"] = [_hash_pii(self.city)]
        if self.state:
            ud["st"] = [_hash_pii(self.state)]
        if self.zip_code:
            ud["zp"] = [_hash_pii(self.zip_code)]
        if self.country:
            ud["country"] = [_hash_pii(self.country)]
        return ud


@dataclass
class PixelFeedbackEngine:
    """
    📡 محرك Meta CAPI — يطبّق القاعدة الذهبية بصرامة.

    الأحداث المسموحة حسب مرحلة الطلب:
      • PageView / ViewContent — وقت التصفح
      • AddToCart / InitiateCheckout — وقت تأكيد الطلب
      • Purchase — فقط بعد OrderStatus.DELIVERED + دفع COD

    التوكن لا يُكتب في الكود أبداً — يُقرأ من متغير بيئة.
    """
    pixel_id: str = META_PIXEL_ID
    access_token_env_var: str = "META_CAPI_ACCESS_TOKEN"  # اسم متغير البيئة فقط
    test_event_code: Optional[str] = None  # للاختبار في Events Manager
    _sent_event_ids: set = field(default_factory=set)     # منع التكرار (dedup)

    def _get_token(self) -> str:
        token = os.environ.get(self.access_token_env_var, "")
        if not token:
            raise RuntimeError(
                f"❌ التوكن مش موجود. اضبط متغير البيئة {self.access_token_env_var} "
                f"(لا تكتب التوكن في الكود أبداً)."
            )
        return token

    def _make_event_id(self, order_id: str, event_name: str) -> str:
        """event_id ثابت لكل (طلب+حدث) — يمنع التكرار بين Browser و Server."""
        return f"{event_name.lower()}_{order_id}"

    def build_purchase_event(self, order_id: str, value: float, currency: str,
                             customer: CustomerData, order_status: OrderStatus,
                             is_paid: bool) -> Dict[str, Any]:
        """
        🏆 يبني حدث Purchase — مع تطبيق القاعدة الذهبية.
        يرفض البناء لو الطلب لسه مش مُسلَّم/مدفوع.
        """
        if order_status != OrderStatus.DELIVERED or not is_paid:
            return {
                "blocked": True,
                "reason": (f"⛔ القاعدة الذهبية: Purchase ممنوع. "
                           f"الحالة={order_status.value}, مدفوع={is_paid}. "
                           f"لازم DELIVERED + paid."),
            }
        event_id = self._make_event_id(order_id, "Purchase")
        if event_id in self._sent_event_ids:
            return {"blocked": True, "reason": f"⛔ تكرار: {event_id} اتبعت قبل كده"}

        return {
            "blocked": False,
            "event_id": event_id,
            "payload": {
                "data": [{
                    "event_name": "Purchase",
                    "event_time": int(time.time()),
                    "event_id": event_id,
                    "action_source": "website",
                    "user_data": customer.to_hashed_user_data(),
                    "custom_data": {
                        "currency": currency, "value": round(value, 2),
                        "order_id": order_id,
                    },
                }],
                **({"test_event_code": self.test_event_code}
                   if self.test_event_code else {}),
            },
        }

    def send_event(self, event_package: Dict[str, Any],
                   dry_run: bool = True, max_retries: int = 3) -> Dict[str, Any]:
        """
        يرسل الحدث لـ Meta. dry_run=True (افتراضي) للاختبار الآمن بدون إرسال.

        التفعيل الحقيقي: dry_run=False (يتطلب requests + توكن في البيئة).
        """
        if event_package.get("blocked"):
            return {"status": "blocked", "reason": event_package["reason"]}

        event_id = event_package["event_id"]
        if dry_run:
            return {
                "status": "dry_run", "event_id": event_id,
                "message": "🧪 محاكاة — لم يُرسل فعلياً. اضبط dry_run=False للتفعيل.",
                "payload_preview": event_package["payload"],
            }

        # ── التفعيل الحقيقي (stub قابل للتفعيل) ──
        try:
            import requests  # noqa
        except ImportError:
            return {"status": "error", "reason": "نصّب requests: pip install requests"}

        url = META_CAPI_ENDPOINT.format(pixel_id=self.pixel_id)
        token = self._get_token()
        last_err = None
        for attempt in range(1, max_retries + 1):
            try:
                resp = requests.post(
                    url, params={"access_token": token},
                    json=event_package["payload"], timeout=15,
                )
                if resp.status_code == 200:
                    self._sent_event_ids.add(event_id)
                    return {"status": "sent", "event_id": event_id,
                            "response": resp.json()}
                last_err = f"HTTP {resp.status_code}: {resp.text[:200]}"
            except Exception as e:  # noqa
                last_err = str(e)
            time.sleep(2 * attempt)  # backoff
        return {"status": "failed", "event_id": event_id,
                "reason": last_err, "attempts": max_retries}


@dataclass
class EMQTracker:
    """
    📊 تتبّع Event Match Quality. الهدف: رفع EMQ فوق 7.
    كل ما زادت حقول الـ PII المهشّرة، زاد EMQ.
    """
    pageview_emq: float = 0.0
    viewcontent_emq: float = 0.0
    purchase_emq: float = 0.0

    def improvement_tips(self) -> List[str]:
        tips = []
        for name, v in {"PageView": self.pageview_emq,
                        "ViewContent": self.viewcontent_emq,
                        "Purchase": self.purchase_emq}.items():
            if 0 < v < 7:
                tips.append(f"{name} EMQ={v} — أضف Email + City + ZIP لرفعه فوق 7")
        return tips or ["✅ كل الأحداث EMQ ≥ 7"]


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 12 · DEEP RESEARCH ENGINE  ·  محرك البحث العميق (stubs قابلة للتفعيل)
# ═══════════════════════════════════════════════════════════════════════════════

# ⚠️ كل مفاتيح الـ API تُقرأ من البيئة (.env) — لا تُكتب في الكود أبداً.
RESEARCH_SOURCES = {
    "google": {"env": "GOOGLE_SEARCH_API_KEY", "purpose": "حجم البحث + الترند"},
    "amazon": {"env": "AMAZON_PAAPI_KEY", "purpose": "أسعار + تقييمات منافسين"},
    "noon": {"env": "NOON_API_KEY", "purpose": "أسعار السوق المصري/الخليجي"},
    "jumia": {"env": "JUMIA_API_KEY", "purpose": "أسعار + توفر محلي"},
    "meta_ad_library": {"env": "META_ADLIB_TOKEN", "purpose": "إعلانات المنافسين الشغّالة"},
    "tiktok": {"env": "TIKTOK_API_KEY", "purpose": "ترندات + كرياتيف فيرال"},
}


@dataclass
class ResearchResult:
    source: str
    activated: bool
    data: Dict[str, Any] = field(default_factory=dict)
    note: str = ""


@dataclass
class DeepResearchEngine:
    """
    🔍 محرك البحث العميق. كل مصدر stub قابل للتفعيل:
       • لو متغير البيئة موجود → ينفّذ الاستعلام الحقيقي (تضيف الكود).
       • لو مش موجود → يرجع stub توضيحي بدل ما يكسر.

    التفعيل: اضبط متغير البيئة المناسب وأكمل دالة _query_<source>.
    """

    def _is_activated(self, source: str) -> bool:
        env = RESEARCH_SOURCES.get(source, {}).get("env", "")
        return bool(env and os.environ.get(env))

    def research_product(self, product_name: str,
                         sources: Optional[List[str]] = None) -> Dict[str, ResearchResult]:
        sources = sources or list(RESEARCH_SOURCES.keys())
        results = {}
        for src in sources:
            if src not in RESEARCH_SOURCES:
                continue
            if self._is_activated(src):
                results[src] = self._query_source(src, product_name)
            else:
                results[src] = ResearchResult(
                    source=src, activated=False,
                    note=(f"⚪ غير مفعّل. اضبط {RESEARCH_SOURCES[src]['env']} "
                          f"للتفعيل. الغرض: {RESEARCH_SOURCES[src]['purpose']}"),
                )
        return results

    def _query_source(self, source: str, product_name: str) -> ResearchResult:
        """
        Stub التنفيذ الحقيقي. أضف منطق كل API هنا عند التفعيل.
        مثال (Meta Ad Library):
            import requests
            token = os.environ["META_ADLIB_TOKEN"]
            resp = requests.get("https://graph.facebook.com/v21.0/ads_archive",
                                params={"access_token": token,
                                        "search_terms": product_name,
                                        "ad_reached_countries": "EG"})
            return ResearchResult(source, True, resp.json())
        """
        return ResearchResult(
            source=source, activated=True,
            data={"query": product_name, "status": "stub_activated"},
            note=f"🟢 مفعّل — أكمل منطق _query_source لـ {source}",
        )

    def synthesize(self, results: Dict[str, ResearchResult]) -> Dict[str, Any]:
        """يلخّص نتائج البحث في تقرير موحّد."""
        active = [r.source for r in results.values() if r.activated]
        inactive = [r.source for r in results.values() if not r.activated]
        return {
            "مصادر مفعّلة": active or ["لا يوجد — كلها stubs"],
            "مصادر غير مفعّلة": inactive,
            "توصية": ("فعّل Meta Ad Library + Noon أولاً (الأهم للسوق المصري)"
                      if inactive else "كل المصادر مفعّلة"),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 13 · COMPOSITE SCORE v3  ·  الدرجة المركّبة (تحل NOTE_02 + NOTE_03)
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class CompositeScoreV3:
    """
    🎯 الدرجة المركّبة النهائية (v3.1) — تدمج كل المحركات في قرار واحد.

    ✅ NOTE_02: لو profitability=0، الدرجة متبقاش 0 تلقائياً.
    ✅ NOTE_03: Reality Validation لها وزن حقيقي وتقدر تخفض الدرجة.
    🆕 v3.1: GenerationalAlignment يدخل كـ multiplier على الدرجة النهائية.
    """
    persona_completeness: float    # 0-100
    taha_index: float              # 0-10
    profitability_score: float     # 0-10 (أو -1)
    reality_score: float           # 0-10 (أو -1)
    generational_alignment: float = 1.0  # 🆕 v3.1: 0-1 (1.0 = لا تأثير، < 1 = تخفيض)

    def calculate(self) -> Dict[str, Any]:
        components = {}
        weights = {}

        # البيرسونا (تحويل 0-100 → 0-10)
        components["persona"] = self.persona_completeness / 10
        weights["persona"] = 0.20

        # مؤشر طه
        components["taha_index"] = self.taha_index
        weights["taha_index"] = 0.30

        # الربحية (لو -1 = مفيش بيانات، نشيلها من الأوزان)
        if self.profitability_score >= 0:
            components["profitability"] = self.profitability_score
            weights["profitability"] = 0.30
        else:
            weights["taha_index"] += 0.15
            weights["persona"] += 0.15

        # الواقع (لو -1 = مفيش اختبار)
        if self.reality_score >= 0:
            components["reality"] = self.reality_score
            weights["reality"] = 0.20
        else:
            # إعادة توزيع وزن الواقع على المتاح
            extra = 0.20 / max(1, len(components))
            for k in list(components.keys()):
                weights[k] = weights.get(k, 0) + extra

        total_w = sum(weights[k] for k in components)
        score = sum(components[k] * (weights[k] / total_w) for k in components)
        raw_score = round(min(10.0, max(0.0, score)), 2)

        # 🆕 v3.1: GenerationalAlignment multiplier (0.85–1.10)
        gen_multiplier = max(0.85, min(1.10, 0.85 + (self.generational_alignment * 0.25)))
        score = round(min(10.0, max(0.0, raw_score * gen_multiplier)), 2)

        # ✅ NOTE_03: الواقع السيء يضع سقفاً على الدرجة
        capped = False
        if self.reality_score >= 0 and self.reality_score < 3.5 and score > 4:
            score = 4.0
            capped = True

        return {
            "score": score,
            "raw_score_before_generational": raw_score,
            "generational_multiplier": round(gen_multiplier, 3),
            "grade": self._grade(score),
            "components": {k: round(v, 2) for k, v in components.items()},
            "reality_capped": capped,
            "missing": [m for m, present in
                        [("ربحية", self.profitability_score >= 0),
                         ("اختبار واقع", self.reality_score >= 0)] if not present],
        }

    @staticmethod
    def _grade(score: float) -> str:
        if score >= 8.5:
            return "A — منتج بطل، وسّع بثقة"
        if score >= 7:
            return "B — منتج قوي، اختبر ووسّع"
        if score >= 5.5:
            return "C — واعد، يحتاج تحسين"
        if score >= 4:
            return "D — ضعيف، راجع جدياً"
        return "F — لا تطلق، أعد التفكير"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 14 · CONVERSION FEEDBACK PROTOCOL  ·  بروتوكول التغذية العكسية
# ═══════════════════════════════════════════════════════════════════════════════

DELIVERED_KEYWORDS = ["delivered", "تم التسليم", "مستلم", "تسليم", "completed"]
LOW_QUALITY_KEYWORDS = ["returned", "cancelled", "مرتجع", "ملغي", "رفض", "refund"]


def classify_conversion(status_text: Any) -> Dict[str, Any]:
    """
    🔄 يصنّف حالة الطلب لتحديد الحدث المناسب لـ Meta.
    ✅ إصلاح BUG3: isinstance guard ضد None/int/dict.
    """
    if not isinstance(status_text, str):
        return {
            "event": None, "quality": "invalid",
            "note": f"⚠️ حالة غير صالحة (نوع {type(status_text).__name__}) — تجاهل",
        }
    s = status_text.strip().lower()
    if any(k in s for k in LOW_QUALITY_KEYWORDS):
        return {"event": None, "quality": "low",
                "note": "❌ مرتجع/ملغي — لا تُرسل Purchase"}
    if any(k in s for k in DELIVERED_KEYWORDS):
        return {"event": "Purchase", "quality": "high",
                "note": "✅ مُسلَّم — أرسل Purchase عبر CAPI"}
    return {"event": "InitiateCheckout", "quality": "pending",
            "note": "🟡 قيد التنفيذ — InitiateCheckout فقط، مش Purchase"}


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 15 · WORKED EXAMPLES  ·  أمثلة تطبيقية كاملة
# ═══════════════════════════════════════════════════════════════════════════════

def example_1_karseell() -> Dict[str, Any]:
    """
    💇‍♀️ المثال 1: ماسك كارسيل ماكا للشعر — 650 إلى 799 ج.
    منتج عناية بالشعر، COD، السوق المصري.
    """
    persona = IntegratedPersona(
        product_name="Karseell Maca Hair Mask",
        demographic=Layer1_Demographic(
            age_range="22-40", gender="إناث", location="مصر (حضري)",
            income_class="B / C+", occupation="موظفة / طالبة / ربة منزل",
        ),
        behavioral=Layer2_Behavioral(
            browsing_habits=["إنستجرام", "تيك توك", "فيسبوك"],
            buying_behavior=["COD"], price_sensitivity="متوسطة",
            content_preferences=["Before/After", "Reels", "تجارب حقيقية"],
            triggers_attention=["نتيجة سريعة", "تخفيضات"],
        ),
        psychological=Layer3_Psychological(
            core_values=["العناية بالنفس", "الثقة"],
            pains=["شعر هايش/تالف", "إحباط من منتجات فشلت"],
            goals=["شعر ناعم لامع"], fears=["إهدار فلوس على منتج مش فعّال"],
        ),
        emotional=Layer4_Emotional(
            current_feeling="إحباط من حالة الشعر",
            desired_feeling="ثقة + إحساس بالدلع",
            emotional_needs=["تقدير", "نتيجة ملموسة"],
        ),
        motivational=Layer5_Motivational(
            purchase_triggers=["نتيجة من أول استخدام", "تركيبة ماكا"],
            decision_drivers=["COD", "ضمان الجودة", "تقييمات"],
        ),
        objections=Layer6_Objections(
            price_objections=["السعر أغلى من ماسكات تانية"],
            trust_objections=["هينفع فعلاً ولا زي الباقي؟"],
            counter_messages=["مكوّن ماكا النادر", "تجربة آلاف العملاء"],
            proof_required=["Before/After حقيقي", "تقييمات"],
        ),
        synthesis=Layer7_Synthesis(
            ideal_customer="بنت 22-40 شعرها تالف وجرّبت منتجات فشلت",
            biggest_pain="شعر هايش + إحباط متراكم",
            core_desire="شعر ناعم لامع بثقة",
            biggest_objection="هل هينفع فعلاً؟",
            strongest_trigger="نتيجة من أول استخدام + COD",
            best_marketing_angle="إثبات بصري (Before/After) + ضمان COD",
        ),
        cncr=CNCROverlay(cortisol_level=6, dopamine_level=7,
                         oxytocin_level=4, f_ego_risk=2),
    )

    eco = UnitEconomics(
        selling_price=750, cogs=180, shipping_cost=55, packaging_cost=15,
        return_rate_percentage=0.12, customer_service_cost=20,
    )
    profit = ProfitIntelligence(unit_economics=eco, expected_cac=90,
                                expected_ltv=1500, repeat_purchase_rate=0.30)

    hooks = HooksEngine()
    hooks.add_hook(HookType.PAIN, "شعرك هايش ومش عارفة تسيطري عليه؟",
                   Neurochemical.CORTISOL, PersonaLayer.EMOTIONAL)
    hooks.add_hook(HookType.RESULT, "نعومة ولمعان من أول استخدام — شغل أصول",
                   Neurochemical.DOPAMINE, PersonaLayer.MOTIVATIONAL)
    hooks.add_hook(HookType.SOCIAL_PROOF, "تجربة آلاف العملاء + تقييمات حقيقية",
                   Neurochemical.OXYTOCIN, PersonaLayer.PSYCHOLOGICAL)
    hooks.add_hook(HookType.OBJECTION_BREAK, "ادفعي عند الاستلام — مفيش مخاطرة",
                   Neurochemical.OXYTOCIN, PersonaLayer.OBJECTIONS)

    equation = GoldenEquation(
        clear_problem="شعرك تالف وجرّبتي كتير من غير نتيجة؟",
        purchase_trigger="ماسك ماكا بنتيجة من أول استخدام،",
        psychological_drive="عشان تستعيدي ثقتك",
        real_desire="بشعر ناعم لامع",
        objection_break="والدفع عند الاستلام — جربي من غير مخاطرة.",
    )

    return {
        "persona": persona, "profit": profit, "hooks": hooks, "equation": equation,
        "composite": CompositeScoreV3(
            persona_completeness=persona.completeness_score(),
            taha_index=7.5,
            profitability_score=profit.profitability_score(),
            reality_score=-1,  # لسه ماتعملش اختبار
        ).calculate(),
    }


def example_2_crochet_bag() -> Dict[str, Any]:
    """
    👜 المثال 2: شنطة كروشيه يدوي — 1800 ج (300 ج/شهر تقسيط).
    ببيانات البيرسونا الحقيقية من جدول د. إيهاب.
    """
    persona = IntegratedPersona(
        product_name="شنطة كروشيه يدوي",
        demographic=Layer1_Demographic(
            age_range="24-42", gender="إناث", income_class="B / B-",
            location="القاهرة الكبرى (مدينة نصر، التجمع، الشيخ زايد)",
            occupation="موظفة / سيدة أعمال صغيرة",
        ),
        behavioral=Layer2_Behavioral(
            browsing_habits=["إنستجرام", "تيك توك"],
            buying_behavior=["BNPL / تقسيط", "COD"],
            price_sensitivity="عالية (حساسة للسعر كاش)",
            content_preferences=["Reels", "Outfit coordination"],
            triggers_attention=["FOMO", "لقطة وتريند"],
        ),
        psychological=Layer3_Psychological(
            core_values=["التميز الطبقي", "الاستقلالية"],
            aspirations=["Identity Upgrade"],
            pains=["رعب الهبوط الطبقي", "الظهور بمظهر عادي"],
            goals=["لفت الانتباه الإيجابي"],
            fears=["تبدو تقليدية"],
        ),
        emotional=Layer4_Emotional(
            current_feeling="ضغط مالي وتوتر من التضخم",
            desired_feeling="دلع ووجاهة دون إخلال بميزانية البيت",
            emotional_needs=["تقدير اجتماعي", "طمأنينة مالية"],
        ),
        motivational=Layer5_Motivational(
            purchase_triggers=["تقسيط مرن 300ج/شهر", "ندرة (شغل يدوي)"],
            decision_drivers=["ضمان جودة الخيط", "عرض محدود"],
        ),
        objections=Layer6_Objections(
            price_objections=["السعر عالي كاش في ظل الظروف"],
            quality_objections=["هتعيش ولا الكروشيه هيفك مع الغسيل؟"],
            counter_messages=["قطن طبيعي 100% غرزة غرزة", "تقسيط يريحك"],
            proof_required=["فيديو غسيل/شد الخيط", "ضمان"],
        ),
        synthesis=Layer7_Synthesis(
            ideal_customer="سيدة 24-42 من كومباوندات القاهرة تبحث عن تميز",
            biggest_pain="رعب الظهور بمظهر عادي + ضغط مالي",
            core_desire="وجاهة وتميز دون إرهاق الميزانية",
            biggest_objection="السعر عالي كاش + هل يدوم؟",
            strongest_trigger="تقسيط 300ج/شهر + ندرة الشغل اليدوي",
            best_marketing_angle="بريستيج بالتقسيط + إثبات الجودة بالفيديو",
        ),
        cncr=CNCROverlay(cortisol_level=7, dopamine_level=8,
                         oxytocin_level=4, endorphins_level=6, f_ego_risk=7),
    )

    eco = UnitEconomics(
        selling_price=1800, cogs=550, shipping_cost=60, packaging_cost=40,
        return_rate_percentage=0.15, customer_service_cost=30,
    )
    profit = ProfitIntelligence(unit_economics=eco, expected_cac=200,
                                expected_ltv=2800, repeat_purchase_rate=0.20)

    hooks = HooksEngine()
    hooks.add_hook(HookType.PAIN,
                   "ميزانية اليومين دول مابتستحملش صدمات.. شيلنا عنك هم الحساب!",
                   Neurochemical.CORTISOL, PersonaLayer.EMOTIONAL)
    hooks.add_hook(HookType.RESULT,
                   "شغل أصول، قطن طبيعي 100% يعيش ويستحمل الغسيل",
                   Neurochemical.OXYTOCIN, PersonaLayer.OBJECTIONS)
    hooks.add_hook(HookType.OFFER,
                   "متفصلة على الفرازة بالطلب — متاح لـ 5 قطع بس الأسبوع ده",
                   Neurochemical.DOPAMINE, PersonaLayer.MOTIVATIONAL)
    hooks.add_hook(HookType.OBJECTION_BREAK,
                   "عايني الماتريال وقت الاستلام — COD أو تقسيط يريحك",
                   Neurochemical.OXYTOCIN, PersonaLayer.OBJECTIONS)

    equation = GoldenEquation(
        clear_problem="خايفة تبيني عادية في خروجاتك؟",
        purchase_trigger="شنطة كروشيه يدوي بـ 300ج/شهر،",
        psychological_drive="تليق ببريستيجك",
        real_desire="وتخليكي حتة لوحدك",
        objection_break="قطن طبيعي يدوم، والدفع عند الاستلام.",
    )

    reality = RealityValidationTest(
        product_name="شنطة كروشيه يدوي",
        main_hypothesis="شريحة الكومباوندات تشتري بريستيج بالتقسيط",
        ctr=1.8, purchases=12, cpa=180, break_even_cpa=profit.break_even_value(),
        confirmed_orders=12, delivered_orders=9,
    )

    return {
        "persona": persona, "profit": profit, "hooks": hooks, "equation": equation,
        "reality": reality,
        "reality_decision": reality.get_validation_decision(),
        "composite": CompositeScoreV3(
            persona_completeness=persona.completeness_score(),
            taha_index=8.0,
            profitability_score=profit.profitability_score(),
            reality_score=reality.calculate_reality_validation_score(),
        ).calculate(),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 16 · TESTS  ·  اختبارات شاملة (تشغّل بـ python THINC_v3_0...py --test)
# ═══════════════════════════════════════════════════════════════════════════════

def run_all_tests() -> Dict[str, Any]:
    """🧪 مجموعة اختبارات تتحقق من سلامة كل المحركات."""
    passed, failed = [], []

    def check(name: str, cond: bool):
        (passed if cond else failed).append(name)

    # T1: الهوية محمية
    check("T1 verify_attribution", verify_attribution() is True)
    check("T1b identity_hash ثابت", len(compute_identity_hash()) == 64)

    # T2: UnitEconomics يرفض البيانات الغلط
    try:
        UnitEconomics(selling_price=-10, cogs=5)
        check("T2 رفض سعر سالب", False)
    except ValueError:
        check("T2 رفض سعر سالب", True)
    try:
        UnitEconomics(selling_price=100, cogs=10, return_rate_percentage=5)  # 500%!
        check("T2b رفض نسبة > 1", False)
    except ValueError:
        check("T2b رفض نسبة > 1", True)

    # T3: break-even يرجع dict دايماً
    losing = ProfitIntelligence(UnitEconomics(selling_price=100, cogs=200))
    be = losing.calculate_break_even_cpa()
    check("T3 break-even dict", isinstance(be, dict))
    check("T3b منتج خاسر = unprofitable",
          be["status"] == "unprofitable_before_ads")

    # T4: LTV/CAC infinity عند CAC=0
    inf = ProfitIntelligence(UnitEconomics(selling_price=100, cogs=20),
                             expected_cac=0, expected_ltv=500)
    check("T4 LTV/CAC = inf", inf.ltv_cac_ratio()["value"] == float("inf"))

    # T5: classify_conversion isinstance guard
    check("T5 None لا يكسر", classify_conversion(None)["quality"] == "invalid")
    check("T5b int لا يكسر", classify_conversion(123)["quality"] == "invalid")
    check("T5c delivered = Purchase",
          classify_conversion("Order delivered")["event"] == "Purchase")
    check("T5d returned = no event",
          classify_conversion("مرتجع")["event"] is None)

    # T6: Decision Engine — بيانات قليلة = TEST مش KILL
    low_perf = CampaignPerformanceData("test", impressions=100, clicks=3, spend=20,
                                       confirmed_orders=0)
    low_profit = ProfitIntelligence(UnitEconomics(selling_price=300, cogs=100))
    dec = DecisionEngine(low_perf, low_profit).decide()
    check("T6 بيانات قليلة = TEST", "TEST" in dec["decision"])

    # T7: Reality Override يمنع SCALE على واقع سيء
    good_perf = CampaignPerformanceData("test2", impressions=5000, clicks=120,
                                        spend=300, confirmed_orders=20,
                                        delivered_orders=15, revenue=3000)
    good_profit = ProfitIntelligence(UnitEconomics(selling_price=300, cogs=80),
                                     expected_cac=15)
    bad_reality = RealityValidationTest("p", "h", ctr=0.2, purchases=1, cpa=250,
                                        break_even_cpa=50, confirmed_orders=2,
                                        delivered_orders=0)
    dec2 = DecisionEngine(good_perf, good_profit, bad_reality).decide()
    check("T7 Reality Override active", dec2["reality_override"] is True)

    # T8: كل الـ 16 محرك موجودين
    check("T8 16 محرك", len(Layer4_BehavioralTriggers.all_16_drivers()) == 16)

    # T9: CNCR toggle
    cncr_off = CNCROverlay(enabled=False)
    check("T9 CNCR معطّل",
          cncr_off.get_chemistry_recommendation().get("status") is not None)
    cncr_on = CNCROverlay(enabled=True, dopamine_level=9, f_ego_risk=8)
    check("T9b CNCR D² محسوب", cncr_on.get_dopamine_squared() > 0)
    check("T9c F_ego تحذير", "تحذير F_ego" in cncr_on.get_chemistry_recommendation())

    # T10: CNCR يرفض قيم خارج 0-10
    try:
        CNCROverlay(dopamine_level=15)
        check("T10 رفض قيمة > 10", False)
    except ValueError:
        check("T10 رفض قيمة > 10", True)

    # T11: Pixel — Purchase ممنوع قبل التسليم
    px = PixelFeedbackEngine(test_event_code="TEST123")
    cust = CustomerData(email="a@b.com", phone="01001234567", city="Cairo")
    blocked = px.build_purchase_event("ORD1", 750, "EGP", cust,
                                      OrderStatus.SHIPPED, is_paid=False)
    check("T11 Purchase ممنوع قبل التسليم", blocked.get("blocked") is True)
    allowed = px.build_purchase_event("ORD2", 750, "EGP", cust,
                                      OrderStatus.DELIVERED, is_paid=True)
    check("T11b Purchase مسموح بعد التسليم", allowed.get("blocked") is False)

    # T12: PII مهشّر (مش plain text)
    ud = cust.to_hashed_user_data()
    check("T12 email مهشّر", ud["em"][0] != "a@b.com" and len(ud["em"][0]) == 64)
    check("T12b phone مطبّع+مهشّر", ud["ph"][0] != "01001234567")

    # T13: dedup — نفس event_id مايتبعتش مرتين
    px.send_event(allowed, dry_run=False) if False else None
    px._sent_event_ids.add(allowed["event_id"])
    again = px.build_purchase_event("ORD2", 750, "EGP", cust,
                                    OrderStatus.DELIVERED, is_paid=True)
    check("T13 dedup يمنع التكرار", again.get("blocked") is True)

    # T14: Composite — profitability مفقودة متخليش الدرجة 0
    comp = CompositeScoreV3(persona_completeness=80, taha_index=8,
                            profitability_score=-1, reality_score=-1).calculate()
    check("T14 composite مش 0 رغم نقص البيانات", comp["score"] > 0)

    # T15: DeepResearch stubs مش بتكسر بدون مفاتيح
    research = DeepResearchEngine().research_product("test product")
    check("T15 stubs شغّالة بدون مفاتيح", all(not r.activated for r in research.values()))

    # T16: المثالين بيشتغلوا
    check("T16 مثال Karseell", example_1_karseell()["composite"]["score"] > 0)
    check("T16b مثال الشنطة", example_2_crochet_bag()["composite"]["score"] >= 0)

    return {
        "total": len(passed) + len(failed),
        "passed": len(passed), "failed": len(failed),
        "failed_names": failed,
        "success_rate": round(len(passed) / max(1, len(passed) + len(failed)) * 100, 1),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 17 · MAIN / DEMO  ·  التشغيل والعرض
# ═══════════════════════════════════════════════════════════════════════════════

def print_framework_summary():
    """يطبع ملخص النموذج + الـ Bootstrap + الـ Watermark."""
    print("=" * 75)
    print(f"  {FRAMEWORK_NAME}™ {FRAMEWORK_VERSION}")
    print(f"  {FRAMEWORK_FULL_NAME}")
    print(f"  © {COPYRIGHT_YEAR} {AUTHOR_NAME_AR} — {TRADEMARK_HOLDER}")
    print("=" * 75)
    print(BOOTSTRAP_PROTOCOL)
    print("\n📦 المكونات المحمّلة:")
    print("   • 8 طبقات بيرسونا (6 + خلاصة + 🆕 الذكاء الجيلي v3.1)")
    print("   • THINC Core (5 طبقات أكاديمية)")
    print("   • 🆕 GenerationalIntelligenceEngine — 4 معادلات: GDI · GVSI · FMS · CDP")
    print(f"   • 🆕 {len(EGYPTIAN_FORMATIVE_EVENTS)} حدث مصري مؤسِّس — قابل للتحديث الديناميكي")
    print(f"   • {len(Layer4_BehavioralTriggers.all_16_drivers())} محرك سلوكي")
    print("   • المعادلة الذهبية + 5 أنواع Hooks")
    print("   • Profit Intelligence + Reality Validation")
    print("   • Decision Engine (مع Reality Override)")
    print("   • Pixel Feedback Engine (Meta CAPI كامل)")
    print(f"   • Deep Research Engine ({len(RESEARCH_SOURCES)} مصادر stubs)")
    print("   • CNCR Overlay (اختياري)")
    print(get_watermark())


if __name__ == "__main__":
    import sys

    if "--test" in sys.argv:
        print("🧪 تشغيل الاختبارات...\n")
        results = run_all_tests()
        print(f"النتيجة: {results['passed']}/{results['total']} نجح "
              f"({results['success_rate']}%)")
        if results["failed"]:
            print(f"❌ فشل: {results['failed_names']}")
            sys.exit(1)
        print("✅ كل الاختبارات نجحت!")
        print(get_watermark())

    elif "--example" in sys.argv:
        ex = example_2_crochet_bag()
        print("👜 مثال: شنطة كروشيه يدوي\n")
        print(f"اكتمال البيرسونا: {ex['persona'].completeness_score()}%")
        print(f"الرسالة الذهبية: {ex['equation'].compose_message()}")
        print(f"درجة الربحية: {ex['profit'].profitability_score()}/10")
        print(f"قرار الواقع: {ex['reality_decision']['decision']}")
        print(f"الدرجة المركّبة: {ex['composite']['score']}/10 "
              f"({ex['composite']['grade']})")
        print(get_watermark())

    else:
        print_framework_summary()
