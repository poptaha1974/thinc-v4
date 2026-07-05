# -*- coding: utf-8 -*-
"""Egyptian Social-Cultural Intelligence Engine for THINC v4.0.

This module upgrades the existing Egyptianization layer from language adaptation
into social-context intelligence.

It is designed for Egyptian and Arab ecommerce decisions where buying behavior is
not driven by price alone, but also by:

- family influence,
- occasion norms,
- respectability,
- embarrassment risk,
- gift etiquette,
- trust signals,
- religious and seasonal moments,
- social class nuance,
- and local channel behavior.

Important caution:
    These profiles are decision-support heuristics. They are not deterministic
    labels for individuals. Always validate against live campaign and sales data.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List


class EgyptianGenerationalCohort(Enum):
    """Local Egyptian generational cohorts with practical marketing labels."""

    INFTAH_SATELLITE = "جيل الانفتاح والفضائيات — تقريبًا 1965-1980"
    INTERNET_TRANSITION = "جيل انتقال الإنترنت والموبايل — تقريبًا 1981-1996"
    SOCIAL_NATIVE = "جيل السوشيال والموبايل — تقريبًا 1997-2012"
    POST_COVID_EARLY = "جيل ما بعد الكورونا والذكاء الاصطناعي — تقريبًا 2013+"
    MIXED_HOUSEHOLD = "جمهور عائلي مختلط القرار"


class LifeStage(Enum):
    STUDENT = "طالب / طالبة"
    EARLY_CAREER = "بداية شغل"
    ENGAGED = "مخطوب / مخطوبة"
    NEWLY_MARRIED = "متزوج حديثًا"
    PARENT = "أب / أم"
    FAMILY_DECISION_MAKER = "صاحب قرار عائلي"
    BUSINESS_OWNER = "صاحب مشروع / محل"
    CORPORATE_BUYER = "مسؤول مشتريات / هدايا شركات"


class GiftOccasion(Enum):
    BIRTHDAY = "عيد ميلاد"
    MOTHERS_DAY = "عيد الأم"
    ENGAGEMENT = "خطوبة"
    WEDDING = "جواز / كتب كتاب"
    ANNIVERSARY = "عيد جواز / ذكرى ارتباط"
    GRADUATION = "نجاح / تخرج"
    NEW_BABY = "مولود جديد"
    FAMILY_VISIT = "زيارة عائلية"
    WORK_COLLEAGUE = "هدية زميل شغل"
    MANAGER_OR_TEACHER = "هدية مدير / مدرس"
    CLIENT_APPRECIATION = "هدية عميل / شكر"
    RAMADAN_EID = "رمضان / العيد"
    APOLOGY_THANKS = "اعتذار / شكر / مجاملة"


class PriceBand(Enum):
    SYMBOLIC = "رمزية — أقل من 300 جنيه"
    PRACTICAL = "عملية محترمة — 300 إلى 600 جنيه"
    PREMIUM_AFFORDABLE = "شكلها أغلى من سعرها — 600 إلى 1000 جنيه"
    ABOVE_POSITIONING = "خارج تموضع تحت الألف — أعلى من 1000 جنيه"


class SocialRisk(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class SocialNormProfile:
    cohort: EgyptianGenerationalCohort
    life_stage: LifeStage
    dominant_mindset: str
    interests: List[str]
    buying_style: str
    family_influence: str
    status_sensitivity: str
    embarrassment_triggers: List[str]
    trust_signals: List[str]
    preferred_channels: List[str]
    words_to_use: List[str]
    words_to_avoid: List[str]
    notes: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class OccasionProfile:
    occasion: GiftOccasion
    expected_emotional_job: str
    acceptable_price_bands: List[PriceBand]
    packaging_expectation: str
    respectability_rule: str
    common_anxieties: List[str]
    decision_influencers: List[str]
    recommended_message_angles: List[str]
    forbidden_or_sensitive_angles: List[str]


@dataclass(frozen=True)
class GiftSocialFitInput:
    cohort: EgyptianGenerationalCohort
    life_stage: LifeStage
    occasion: GiftOccasion
    price_band: PriceBand
    has_packaging: bool
    has_exchange_policy: bool
    has_social_proof: bool
    is_practical: bool
    looks_more_expensive_than_price: bool
    has_clear_use_case: bool


@dataclass(frozen=True)
class GiftSocialFitResult:
    score: float
    risk_level: SocialRisk
    positioning_sentence: str
    blind_spots: List[str]
    recommendations: List[str]
    suggested_hooks: List[str]


class EgyptianSocialCulturalEngine:
    """Decision-support layer for Egyptian social norms and occasion-based buying."""

    @staticmethod
    def build_cohort_profile(
        cohort: EgyptianGenerationalCohort,
        life_stage: LifeStage,
    ) -> SocialNormProfile:
        base: Dict[EgyptianGenerationalCohort, Dict[str, object]] = {
            EgyptianGenerationalCohort.SOCIAL_NATIVE: {
                "mindset": "سريع، بصري، حساس للشكل والترند، لكنه يتجنب الإحراج الاجتماعي.",
                "interests": ["تيك توك", "إنستجرام", "ترندات", "هدايا مختلفة", "تجربة تصوير", "تخصيص بسيط"],
                "buying": "اندفاع محسوب: ينجذب للشكل والهوك، ثم يسأل عن السعر والتوصيل.",
                "family": "يتأثر بالأصدقاء والسوشيال أكثر من العائلة، لكن في الهدايا الكبيرة يرجع لرأي الأم/الأخت/الشريك.",
                "status": "يهتم أن الهدية تبان لطيفة ومواكبة، لا يريدها تقليدية أو محرجة.",
                "embarrassment": ["هدية شكلها رخيص", "تغليف ضعيف", "منتج مكرر جدًا", "تأخير في التسليم قبل المناسبة"],
                "trust": ["فيديو حقيقي", "تعليقات العملاء", "صور قبل التغليف وبعده", "دفع عند الاستلام"],
                "channels": ["TikTok", "Instagram Reels", "WhatsApp"],
                "use": ["شيك", "ينفع يتصور", "مش تقليدي", "تحت الألف", "هدية مختلفة"],
                "avoid": ["فاخر جدًا", "كلاسيكي أوي", "محاضرة طويلة", "رسمي زيادة"],
            },
            EgyptianGenerationalCohort.INTERNET_TRANSITION: {
                "mindset": "عملي، مشغول، يبحث عن هدية محترمة بدون وجع دماغ وبميزانية واضحة.",
                "interests": ["الأسرة", "العمل", "الاستقرار", "الهدايا العملية", "العروض", "التوصيل السريع"],
                "buying": "يقارن السعر والقيمة، ويحب الترشيح المختصر بدل كثرة الاختيارات.",
                "family": "قرار الهدية غالبًا يتأثر بالزوج/الزوجة أو الأخ/الأخت، خصوصًا في المناسبات العائلية.",
                "status": "يريد هدية تبدو محترمة ولا تظهر كأنها اختيار رخيص.",
                "embarrassment": ["الهدية لا تليق بالمناسبة", "شكلها أقل من المتوقع", "مفيش تغليف", "مفيش ضمان أو استبدال"],
                "trust": ["مكان واضح", "واتساب سريع", "سياسة استبدال", "ترشيح حسب الميزانية"],
                "channels": ["Facebook", "WhatsApp", "Instagram"],
                "use": ["عملية", "محترمة", "من غير حيرة", "حسب الميزانية", "شكلها أغلى من سعرها"],
                "avoid": ["ترند وخلاص", "أرخص حاجة", "ثراء سريع", "مبالغة"],
            },
            EgyptianGenerationalCohort.INFTAH_SATELLITE: {
                "mindset": "رصين، يقدّر السمعة والاحترام ويخاف من المخاطرة أو الإحراج.",
                "interests": ["الأسرة", "الزيارات", "المجاملات", "المنتجات العملية", "المكان الموثوق"],
                "buying": "قرار أبطأ، يحتاج ثقة ومكان واضح وربما مكالمة أو واتساب محترم.",
                "family": "العائلة مؤثرة جدًا؛ رأي الزوجة/الأبناء قد يحسم الاختيار.",
                "status": "حساس جدًا لمدى احترام الهدية للمقام والمناسبة.",
                "embarrassment": ["هدية تقلل من المقام", "تغليف مبهرج", "منتج بلا استخدام واضح", "محل غير موثوق"],
                "trust": ["مكان فعلي", "مكالمة محترمة", "ضمان", "تغليف هادئ", "تجارب ناس حقيقية"],
                "channels": ["Facebook", "WhatsApp", "Phone Call"],
                "use": ["محترمة", "موثوقة", "عملية", "تليق بالمناسبة", "مكان معروف"],
                "avoid": ["تريند", "هوجة", "رخيص", "مغامرة"],
            },
            EgyptianGenerationalCohort.POST_COVID_EARLY: {
                "mindset": "متأثر بالأهل وبالسوشيال؛ قرار الشراء غالبًا ليس مستقلًا.",
                "interests": ["ألعاب", "إكسسوارات", "مدرسة", "ترند", "هدايا صغيرة"],
                "buying": "قرار غير مستقل؛ المحتوى يخاطب الطفل/المراهق لكن الدفع من الأسرة.",
                "family": "الأهل هم أصحاب القرار المالي النهائي.",
                "status": "الشكل والترند مهمان، لكن الأهل يراجعون السعر والفائدة.",
                "embarrassment": ["هدية لا تناسب السن", "منتج غير آمن", "محتوى مبالغ فيه"],
                "trust": ["موافقة الأهل", "استخدام واضح", "أمان", "سعر منطقي"],
                "channels": ["TikTok", "YouTube Shorts", "Parent WhatsApp"],
                "use": ["مناسب للسن", "آمن", "عملي", "يفرحه", "سعره منطقي"],
                "avoid": ["استهداف مباشر بوعود مبالغ فيها", "ضغط على الطفل للشراء"],
            },
            EgyptianGenerationalCohort.MIXED_HOUSEHOLD: {
                "mindset": "قرار جماعي؛ شخص يرى الإعلان وشخص آخر يوافق أو يدفع.",
                "interests": ["البيت", "المناسبات", "القيمة", "الضمان", "الهدايا الآمنة اجتماعيًا"],
                "buying": "يحتاج رسالة تجمع بين الشكل والقيمة والثقة.",
                "family": "العائلة جزء أساسي من القرار، خصوصًا في هدايا الأم والزيارات والجواز.",
                "status": "لازم الهدية تبان لائقة أمام أكثر من طرف.",
                "embarrassment": ["اختيار غير مناسب للمناسبة", "سعر ظاهر أنه رخيص", "عدم وجود تغليف"],
                "trust": ["ترشيحات حسب المناسبة", "صور حقيقية", "سياسة استبدال", "تغليف"],
                "channels": ["Facebook", "WhatsApp", "Instagram"],
                "use": ["مناسبة", "عملية", "لائقة", "هدية جاهزة", "تحت الألف"],
                "avoid": ["اختيار عشوائي", "سعر وخلاص", "مبالغة في الفخامة"],
            },
        }
        data = base[cohort]

        stage_notes = {
            LifeStage.STUDENT: ["حساسية سعر عالية؛ الهدايا الرمزية والعملية أنسب."],
            LifeStage.EARLY_CAREER: ["يريد هدية محترمة بدون ضغط مالي؛ 300-600 منطقة قوية."],
            LifeStage.ENGAGED: ["حساسية الإحراج عالية؛ التغليف والشكل أهم من السعر وحده."],
            LifeStage.NEWLY_MARRIED: ["يميل لهدايا البيت والعناية والشكل الراقي تحت الألف."],
            LifeStage.PARENT: ["يهتم بالأمان والفائدة واستخدام الهدية فعليًا."],
            LifeStage.FAMILY_DECISION_MAKER: ["يراجع المقام الاجتماعي والمناسبة قبل السعر."],
            LifeStage.BUSINESS_OWNER: ["يفضل هدايا قابلة للتكرار للعملاء والموظفين."],
            LifeStage.CORPORATE_BUYER: ["يحتاج كميات، تغليف موحد، وفاتورة/تنظيم."],
        }[life_stage]

        return SocialNormProfile(
            cohort=cohort,
            life_stage=life_stage,
            dominant_mindset=str(data["mindset"]),
            interests=list(data["interests"]),
            buying_style=str(data["buying"]),
            family_influence=str(data["family"]),
            status_sensitivity=str(data["status"]),
            embarrassment_triggers=list(data["embarrassment"]),
            trust_signals=list(data["trust"]),
            preferred_channels=list(data["channels"]),
            words_to_use=list(data["use"]),
            words_to_avoid=list(data["avoid"]),
            notes=stage_notes,
        )

    @staticmethod
    def build_occasion_profile(occasion: GiftOccasion) -> OccasionProfile:
        profiles: Dict[GiftOccasion, OccasionProfile] = {
            GiftOccasion.BIRTHDAY: OccasionProfile(
                occasion,
                "إظهار الاهتمام الشخصي بدون مبالغة.",
                [PriceBand.SYMBOLIC, PriceBand.PRACTICAL, PriceBand.PREMIUM_AFFORDABLE],
                "تغليف لطيف يصلح للتصوير.",
                "الهدية لازم تبان مختارة للشخص، مش أي منتج وخلاص.",
                ["اختيار تقليدي", "هدية لا تناسب السن", "الشكل أرخص من السعر"],
                ["الأصدقاء", "الأخت", "الشريك"],
                ["هدية حسب الشخصية", "شكلها يفرح", "تحت الألف ومش تقليدية"],
                ["رخيص", "أي حاجة", "آخر لحظة بدون اهتمام"],
            ),
            GiftOccasion.MOTHERS_DAY: OccasionProfile(
                occasion,
                "تقدير وامتنان واحترام للأم.",
                [PriceBand.PRACTICAL, PriceBand.PREMIUM_AFFORDABLE],
                "تغليف محترم وهادئ، بعيد عن المبالغة الصارخة.",
                "لازم الهدية تبان تقدير، مش واجب اتعمل وخلاص.",
                ["هدية لا تليق بالأم", "هدية بلا قيمة استخدام", "تغليف ضعيف"],
                ["الأبناء", "الأب", "الإخوة"],
                ["هدية لمامتك تستخدمها وتفتكرك", "تقدير بسيط بس محترم", "شكلها شيك وسعرها مناسب"],
                ["رخيص", "خلص الواجب", "أي هدية للأم"],
            ),
            GiftOccasion.ENGAGEMENT: OccasionProfile(
                occasion,
                "تأكيد الاهتمام والذوق أمام الطرف الآخر والعائلة.",
                [PriceBand.PREMIUM_AFFORDABLE],
                "تغليف راقٍ جدًا؛ الشكل هنا جزء من الرسالة.",
                "الإحراج عالي؛ الهدية لازم تبان أرقى من سعرها.",
                ["تبان رخيصة", "لا تناسب الذوق", "تغليف غير لائق"],
                ["الخطيبة", "الأخت", "الأم", "الصديقات"],
                ["هدية شكلها أغلى من سعرها", "تليق بالمناسبة", "اختيار آمن وشيك"],
                ["أرخص اختيار", "هزار", "مغامرة بذوق غريب"],
            ),
            GiftOccasion.WEDDING: OccasionProfile(
                occasion,
                "مجاملة رسمية محترمة وذكرى عملية.",
                [PriceBand.PRACTICAL, PriceBand.PREMIUM_AFFORDABLE],
                "تغليف رسمي وهادئ.",
                "لازم الهدية تحترم مقام الجواز أو كتب الكتاب.",
                ["هدية صغيرة جدًا على المقام", "اختيار شخصي زيادة", "منتج غير عملي"],
                ["الأسرة", "الأصدقاء المقربون"],
                ["هدية بيت عملية", "هدية محترمة تحت الألف", "تصلح لجواز/كتب كتاب"],
                ["ترند عابر", "مزحة", "رخيص"],
            ),
            GiftOccasion.GRADUATION: OccasionProfile(
                occasion,
                "احتفال بإنجاز وبداية مرحلة جديدة.",
                [PriceBand.SYMBOLIC, PriceBand.PRACTICAL, PriceBand.PREMIUM_AFFORDABLE],
                "تغليف مبهج وحديث.",
                "الهدية يفضل ترتبط بالبداية الجديدة أو الشغل أو الدراسة.",
                ["هدية طفولية", "غير مناسبة للسن", "لا معنى لها"],
                ["الأصدقاء", "الأهل", "الشريك"],
                ["هدية لبداية جديدة", "عملية للشغل أو الجامعة", "تفرح وتتنفع"],
                ["نجاح وخلاص", "أي حاجة للتهنئة"],
            ),
            GiftOccasion.FAMILY_VISIT: OccasionProfile(
                occasion,
                "عدم الذهاب بيد فارغة وإظهار الذوق.",
                [PriceBand.SYMBOLIC, PriceBand.PRACTICAL],
                "تغليف بسيط ونظيف.",
                "الهدية يجب أن تكون آمنة اجتماعيًا ومناسبة لبيت كامل.",
                ["اختيار شخصي جدًا", "حاجة قد تسبب إحراج", "منتج بلا استخدام"],
                ["الزوجة", "الأم", "الأخت"],
                ["هدية زيارة عملية", "مجاملة شيك من غير مبالغة", "تنفع لأي بيت"],
                ["هدية جريئة", "مبالغة", "رخيص بشكل ظاهر"],
            ),
            GiftOccasion.WORK_COLLEAGUE: OccasionProfile(
                occasion,
                "مجاملة مهنية لطيفة بدون رسائل شخصية زائدة.",
                [PriceBand.SYMBOLIC, PriceBand.PRACTICAL],
                "تغليف بسيط ومحايد.",
                "لازم تكون الهدية مهنية وغير محرجة.",
                ["هدية شخصية زيادة", "سعر مبالغ فيه", "رسالة عاطفية غير مناسبة"],
                ["زملاء الفريق", "HR", "المدير المباشر"],
                ["هدية زميل شغل محترمة", "عملية ومناسبة للمكتب", "مجاملة خفيفة"],
                ["رومانسي", "غالي جدًا", "محرج"],
            ),
            GiftOccasion.MANAGER_OR_TEACHER: OccasionProfile(
                occasion,
                "احترام وتقدير بدون مبالغة أو شبهة منفعة.",
                [PriceBand.PRACTICAL, PriceBand.PREMIUM_AFFORDABLE],
                "تغليف رسمي ومحترم.",
                "الهدية يجب أن تكون لائقة ومحايدة.",
                ["هدية شخصية", "مبالغة تفهم غلط", "تغليف مبهرج"],
                ["الزملاء", "الأسرة", "الطلاب"],
                ["هدية تقدير محترمة", "عملية وشيك", "مناسبة لمدير أو مدرس"],
                ["رشوة", "مصلحة", "مجاملة مبالغ فيها"],
            ),
            GiftOccasion.CLIENT_APPRECIATION: OccasionProfile(
                occasion,
                "تقوية العلاقة التجارية وإظهار الاحتراف.",
                [PriceBand.PRACTICAL, PriceBand.PREMIUM_AFFORDABLE],
                "تغليف موحد مع إمكانية كارت شكر.",
                "لازم الهدية تمثل البراند بشكل محترم.",
                ["هدية ضعيفة تؤثر على صورة الشركة", "عدم وجود كميات", "لا يوجد تخصيص بسيط"],
                ["صاحب المشروع", "المبيعات", "الإدارة"],
                ["هدايا عملاء تحت الألف", "مجاملة تجارية محترمة", "تغليف موحد"],
                ["رخيص", "عشوائي", "بلا هوية"],
            ),
            GiftOccasion.RAMADAN_EID: OccasionProfile(
                occasion,
                "صلة وكرم ومجاملة موسمية.",
                [PriceBand.SYMBOLIC, PriceBand.PRACTICAL, PriceBand.PREMIUM_AFFORDABLE],
                "تغليف موسمي راقٍ ومناسب.",
                "الهدية يجب أن تحترم الطابع العائلي والديني للموسم.",
                ["رسالة غير مناسبة للموسم", "مبالغة استهلاكية", "تأخير التسليم"],
                ["العائلة", "الأصدقاء", "العملاء"],
                ["هدية رمضان/العيد", "مجاملة موسمية شيك", "تحت الألف وتليق"],
                ["استغلال الموسم", "ضغط شراء مبالغ فيه"],
            ),
        }

        return profiles.get(
            occasion,
            OccasionProfile(
                occasion,
                "مجاملة اجتماعية مناسبة بدون إحراج.",
                [PriceBand.SYMBOLIC, PriceBand.PRACTICAL, PriceBand.PREMIUM_AFFORDABLE],
                "تغليف نظيف ومناسب للمقام.",
                "الهدية يجب أن تكون لائقة وواضحة الاستخدام.",
                ["عدم مناسبة الهدية", "ضعف التغليف", "غياب سياسة الاستبدال"],
                ["العائلة", "الأصدقاء", "الشريك"],
                ["هدية مناسبة", "شكلها حلو", "عملية وتحت الألف"],
                ["رخيص", "عشوائي", "أي حاجة"],
            ),
        )

    @staticmethod
    def evaluate_gift_social_fit(data: GiftSocialFitInput) -> GiftSocialFitResult:
        cohort = EgyptianSocialCulturalEngine.build_cohort_profile(data.cohort, data.life_stage)
        occasion = EgyptianSocialCulturalEngine.build_occasion_profile(data.occasion)

        score = 5.0
        blind_spots: List[str] = []
        recommendations: List[str] = []

        if data.price_band in occasion.acceptable_price_bands:
            score += 1.0
        else:
            score -= 1.0
            blind_spots.append("الفئة السعرية قد لا تناسب مقام المناسبة اجتماعيًا.")
            recommendations.append("عدّل الباقة أو غيّر زاوية المناسبة بدل التركيز على السعر فقط.")

        if data.has_packaging:
            score += 1.2
        else:
            score -= 1.5
            blind_spots.append("غياب التغليف يضعف إحساس الهدية ويرفع خطر الإحراج.")
            recommendations.append("أضف تغليف هدية واضح حتى لو بسيط؛ التغليف جزء من المنتج في سوق الهدايا.")

        if data.has_exchange_policy:
            score += 0.7
        else:
            score -= 0.4
            blind_spots.append("عدم وضوح الاستبدال يقلل الأمان عند شراء الهدايا.")
            recommendations.append("اعرض سياسة استبدال بسيطة لأن مشتري الهدية يخاف من عدم مناسبة الذوق أو المقاس.")

        if data.has_social_proof:
            score += 0.7
        else:
            score -= 0.3
            blind_spots.append("لا يوجد إثبات اجتماعي كافٍ يجعل العميل يطمئن للاختيار.")
            recommendations.append("اعرض صور عملاء/تغليف/آراء حقيقية لكل مناسبة.")

        if data.is_practical:
            score += 0.8
        else:
            score -= 0.2
            blind_spots.append("الهدية قد تكون شكلية فقط؛ بعض الشرائح المصرية تفضل الاستخدام العملي.")
            recommendations.append("اربط الهدية باستخدام يومي أو لحظة عاطفية واضحة.")

        if data.looks_more_expensive_than_price:
            score += 1.0
        else:
            blind_spots.append("الهدية لا تُظهر قيمة بصرية أعلى من سعرها، وهذا مهم في تموضع تحت الألف.")
            recommendations.append("حسّن التصوير والتغليف والباقة لتظهر الهدية أغلى من سعرها دون ادعاء كاذب.")

        if data.has_clear_use_case:
            score += 0.6
        else:
            score -= 0.4
            blind_spots.append("الاستخدام غير واضح؛ العميل قد لا يفهم لماذا هذه هدية مناسبة.")
            recommendations.append("اكتب الهدية لمين؟ وفي أي مناسبة؟ ولماذا تصلح؟")

        score = round(max(0.0, min(10.0, score)), 2)
        risk = SocialRisk.LOW if score >= 8 else SocialRisk.MEDIUM if score >= 6 else SocialRisk.HIGH if score >= 4 else SocialRisk.CRITICAL

        hooks = [
            f"هدية {data.occasion.value} تحت الألف… شكلها حلو وتنفع بجد.",
            f"قولنا المناسبة والميزانية، ونرشحلك هدية تليق من غير حيرة.",
            f"{occasion.recommended_message_angles[0]} — بتغليف محترم وسعر مناسب.",
        ]

        positioning = (
            "هدايا عملية محترمة تحت 1000 جنيه، مختارة حسب المناسبة والميزانية، "
            "بتغليف يليق ويقلل حيرة الاختيار."
        )

        if not blind_spots:
            blind_spots.append("لا توجد بقعة عمياء اجتماعية حرجة بناءً على البيانات المدخلة.")
        if not recommendations:
            recommendations.append("استمر في اختبار الرسائل حسب المناسبة والجيل، ولا تعتمد على السعر وحده.")

        return GiftSocialFitResult(
            score=score,
            risk_level=risk,
            positioning_sentence=positioning,
            blind_spots=blind_spots,
            recommendations=recommendations,
            suggested_hooks=hooks,
        )

    @staticmethod
    def blind_spot_checklist() -> List[str]:
        return [
            "هل الهدية مناسبة للمقام الاجتماعي؟",
            "هل شكل الهدية لا يسبب إحراجًا رغم أنها تحت الألف؟",
            "هل التغليف يحول المنتج إلى هدية فعلًا؟",
            "هل يوجد استخدام واضح للمنتج؟",
            "هل يوجد إثبات اجتماعي بصور وتجارب حقيقية؟",
            "هل توجد سياسة استبدال تطمئن مشتري الهدية؟",
            "هل الرسالة تخاطب المشتري أم متلقي الهدية أم صاحب قرار الدفع؟",
            "هل مناسبة الشراء موسمية أو دينية أو عائلية؟",
            "هل السعر مناسب للعلاقة: أم، خطيبة، زميل، مدير، عميل؟",
            "هل القناة مناسبة للجيل: تيك توك، فيسبوك، واتساب، مكالمة؟",
            "هل هناك فرق بين القاهرة/المدن الكبرى والمحافظات في الذوق والسعر؟",
            "هل الهدية محايدة وآمنة اجتماعيًا أم شخصية زيادة؟",
        ]
