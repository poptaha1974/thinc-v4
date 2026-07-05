# -*- coding: utf-8 -*-
"""Gift Decision Intelligence Layer for THINC v4.0.

This layer closes the main remaining blind spots for Egyptian ecommerce gift
positioning, especially offers under 1000 EGP.

It combines:
- product-to-occasion fit,
- buyer / recipient / payer split,
- gender and relationship safety,
- geography and class sensitivity,
- seasonality,
- packaging quality,
- trust and scam-fear reduction,
- delivery urgency,
- objection handling,
- and repeat-occasion CRM logic.

Important caution:
    This is a decision-support engine. It does not guarantee sales or remove
    the need for live validation through campaign, WhatsApp, delivery, and
    repeat-purchase data.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List

from thinc_v4.egyptian_social_culture import GiftOccasion, PriceBand, SocialRisk


class EgyptianGeoSegment(Enum):
    GREATER_CAIRO = "القاهرة الكبرى"
    ALEXANDRIA = "الإسكندرية"
    DELTA = "الدلتا"
    UPPER_EGYPT = "الصعيد"
    CANAL_CITIES = "مدن القناة"
    NEW_CITIES = "المدن الجديدة"
    COASTAL_SEASONAL = "الساحل / مناطق موسمية"
    MIXED_NATIONAL = "جمهور مصري مختلط"


class SocialClassSignal(Enum):
    VALUE_SENSITIVE = "حساس للسعر والقيمة"
    MIDDLE_MAINSTREAM = "متوسط عام"
    ASPIRATIONAL = "طموح اجتماعيًا"
    PREMIUM_LEANING = "يميل للراقي"
    CORPORATE = "شركات / مشتريات مؤسسية"


class RecipientGenderContext(Enum):
    MALE = "رجل"
    FEMALE = "سيدة"
    CHILD = "طفل / طفلة"
    NEUTRAL = "محايد"
    MIXED_GROUP = "مجموعة مختلطة"


class RelationshipContext(Enum):
    MOTHER = "أم"
    FATHER = "أب"
    WIFE = "زوجة"
    HUSBAND = "زوج"
    FIANCEE = "خطيبة"
    FIANCE = "خطيب"
    FRIEND = "صديق / صديقة"
    WORK_COLLEAGUE = "زميل / زميلة شغل"
    MANAGER = "مدير"
    TEACHER = "مدرس / مدرسة"
    CLIENT = "عميل"
    MOTHER_IN_LAW = "حماة / حماتك"
    CHILD = "طفل / طفلة"
    FAMILY = "العائلة"
    SELF = "شراء لنفسي"


class BuyerRole(Enum):
    BUYER = "المشتري"
    RECIPIENT = "متلقي الهدية"
    PAYER = "الدافع"
    INFLUENCER = "المؤثر في القرار"
    MIXED = "أدوار مختلطة"


class ProductCategory(Enum):
    DRINKWARE = "مج / كوباية / ترمس"
    BEAUTY_CARE = "عناية شخصية / جمال"
    HOME_DECOR = "ديكور منزلي"
    HOME_APPLIANCE = "جهاز منزلي صغير"
    OFFICE_ACCESSORY = "إكسسوار مكتب"
    LEATHER_GOODS = "جلديات / محافظ / شنط"
    PERFUME = "عطور"
    KIDS_GIFT = "هدايا أطفال"
    FOOD_GIFT = "حلويات / بوكس أكل"
    CUSTOMIZED = "تخصيص / اسم / حروف"
    GENERIC = "منتج عام"


class GiftSafetyClass(Enum):
    SAFE_NEUTRAL = "آمنة ومحايدة"
    PRACTICAL_SAFE = "عملية وآمنة"
    PERSONAL = "شخصية"
    ROMANTIC = "رومانسية"
    FORMAL = "رسمية"
    RISKY_MISUNDERSTOOD = "قد تُفهم غلط"


class SeasonalityMoment(Enum):
    ALWAYS_ON = "دائم"
    RAMADAN = "رمضان"
    EID = "العيد"
    MOTHERS_DAY = "عيد الأم"
    VALENTINE = "الفلانتين"
    GRADUATION_SEASON = "موسم التخرج"
    BACK_TO_SCHOOL = "بداية الدراسة"
    WEDDING_SEASON = "موسم الخطوبات والجواز"
    YEAR_END_CORPORATE = "نهاية السنة للشركات"
    SUMMER_VISITS = "زيارات ومصايف الصيف"


class DeliveryUrgency(Enum):
    SAME_DAY = "نفس اليوم"
    NEXT_DAY = "خلال 24 ساعة"
    TWO_TO_THREE_DAYS = "2-3 أيام"
    WEEK_PLUS = "أسبوع أو أكثر"
    NOT_TIME_SENSITIVE = "غير حساس للوقت"


@dataclass(frozen=True)
class GiftProductProfile:
    name: str
    category: ProductCategory
    price_band: PriceBand
    safety_class: GiftSafetyClass
    perceived_value_score: float
    practicality_score: float
    packaging_score: float
    trust_score: float
    margin_score: float
    stock_ready: bool


@dataclass(frozen=True)
class GiftDecisionInput:
    product: GiftProductProfile
    occasion: GiftOccasion
    relationship: RelationshipContext
    recipient_gender: RecipientGenderContext
    geo_segment: EgyptianGeoSegment
    social_class_signal: SocialClassSignal
    buyer_role: BuyerRole
    seasonality: SeasonalityMoment
    delivery_urgency: DeliveryUrgency
    has_exchange_policy: bool
    has_real_photos: bool
    has_reviews: bool
    can_personalize: bool
    buyer_knows_recipient_taste: bool


@dataclass(frozen=True)
class GiftDecisionResult:
    score: float
    risk_level: SocialRisk
    product_occasion_fit: float
    safety_verdict: str
    positioning: str
    recommended_angle: str
    blind_spots: List[str]
    recommendations: List[str]
    objections: List[str]
    whatsapp_replies: List[str]
    crm_followups: List[str]
    next_best_actions: List[str]


class GiftDecisionIntelligenceEngine:
    """Full gift-commerce decision layer for THINC v4."""

    @staticmethod
    def _bounded_score(value: float) -> float:
        return round(max(0.0, min(10.0, value)), 2)

    @staticmethod
    def options() -> Dict[str, List[str]]:
        return {
            "geo_segments": [item.value for item in EgyptianGeoSegment],
            "social_class_signals": [item.value for item in SocialClassSignal],
            "recipient_gender_contexts": [item.value for item in RecipientGenderContext],
            "relationships": [item.value for item in RelationshipContext],
            "buyer_roles": [item.value for item in BuyerRole],
            "product_categories": [item.value for item in ProductCategory],
            "gift_safety_classes": [item.value for item in GiftSafetyClass],
            "seasonality_moments": [item.value for item in SeasonalityMoment],
            "delivery_urgencies": [item.value for item in DeliveryUrgency],
        }

    @staticmethod
    def product_to_occasion_fit(category: ProductCategory, occasion: GiftOccasion, relationship: RelationshipContext) -> float:
        strong: Dict[GiftOccasion, List[ProductCategory]] = {
            GiftOccasion.BIRTHDAY: [ProductCategory.DRINKWARE, ProductCategory.BEAUTY_CARE, ProductCategory.LEATHER_GOODS, ProductCategory.CUSTOMIZED],
            GiftOccasion.MOTHERS_DAY: [ProductCategory.BEAUTY_CARE, ProductCategory.HOME_DECOR, ProductCategory.HOME_APPLIANCE, ProductCategory.LEATHER_GOODS],
            GiftOccasion.ENGAGEMENT: [ProductCategory.BEAUTY_CARE, ProductCategory.LEATHER_GOODS, ProductCategory.PERFUME, ProductCategory.CUSTOMIZED],
            GiftOccasion.WEDDING: [ProductCategory.HOME_APPLIANCE, ProductCategory.HOME_DECOR, ProductCategory.FOOD_GIFT],
            GiftOccasion.GRADUATION: [ProductCategory.OFFICE_ACCESSORY, ProductCategory.LEATHER_GOODS, ProductCategory.DRINKWARE, ProductCategory.CUSTOMIZED],
            GiftOccasion.FAMILY_VISIT: [ProductCategory.FOOD_GIFT, ProductCategory.HOME_DECOR, ProductCategory.HOME_APPLIANCE],
            GiftOccasion.WORK_COLLEAGUE: [ProductCategory.OFFICE_ACCESSORY, ProductCategory.DRINKWARE, ProductCategory.FOOD_GIFT],
            GiftOccasion.MANAGER_OR_TEACHER: [ProductCategory.OFFICE_ACCESSORY, ProductCategory.LEATHER_GOODS, ProductCategory.FOOD_GIFT],
            GiftOccasion.CLIENT_APPRECIATION: [ProductCategory.OFFICE_ACCESSORY, ProductCategory.LEATHER_GOODS, ProductCategory.CUSTOMIZED],
            GiftOccasion.RAMADAN_EID: [ProductCategory.FOOD_GIFT, ProductCategory.HOME_DECOR, ProductCategory.HOME_APPLIANCE],
        }
        sensitive_relationships = {RelationshipContext.MANAGER, RelationshipContext.TEACHER, RelationshipContext.WORK_COLLEAGUE, RelationshipContext.CLIENT}
        intimate_categories = {ProductCategory.PERFUME, ProductCategory.BEAUTY_CARE, ProductCategory.CUSTOMIZED}

        score = 6.0
        if category in strong.get(occasion, []):
            score += 2.0
        if relationship in sensitive_relationships and category in intimate_categories:
            score -= 2.5
        if relationship in {RelationshipContext.WIFE, RelationshipContext.FIANCEE, RelationshipContext.MOTHER} and category in intimate_categories:
            score += 1.0
        if category == ProductCategory.GENERIC:
            score -= 1.0
        return GiftDecisionIntelligenceEngine._bounded_score(score)

    @staticmethod
    def safety_verdict(data: GiftDecisionInput) -> str:
        if data.relationship in {RelationshipContext.MANAGER, RelationshipContext.TEACHER, RelationshipContext.WORK_COLLEAGUE, RelationshipContext.CLIENT}:
            if data.product.safety_class in {GiftSafetyClass.PERSONAL, GiftSafetyClass.ROMANTIC, GiftSafetyClass.RISKY_MISUNDERSTOOD}:
                return "خطر اجتماعي: الهدية شخصية زيادة وقد تُفهم غلط في سياق رسمي."
            return "آمنة رسميًا: مناسبة لعلاقة مهنية أو مجاملة محترمة."
        if data.relationship in {RelationshipContext.WIFE, RelationshipContext.HUSBAND, RelationshipContext.FIANCEE, RelationshipContext.FIANCE}:
            return "مناسبة لعلاقة شخصية، لكن يجب ضبط الذوق والتغليف والتوقيت."
        if data.relationship in {RelationshipContext.MOTHER, RelationshipContext.MOTHER_IN_LAW, RelationshipContext.FAMILY}:
            return "مناسبة عائليًا إذا ظهرت محترمة وعملية وليست رخيصة بصريًا."
        return "آمنة بشرط وضوح الاستخدام والتغليف وسياسة الاستبدال."

    @staticmethod
    def objections_for(data: GiftDecisionInput) -> List[str]:
        objections = [
            "مش عارف هتعجبه ولا لا.",
            "مش هتبان بسيطة؟",
            "ينفع تتغلف؟",
            "ينفع أبدلها لو مش مناسبة؟",
        ]
        if data.delivery_urgency in {DeliveryUrgency.SAME_DAY, DeliveryUrgency.NEXT_DAY}:
            objections.append("محتاجها بسرعة، هتلحق توصل قبل المناسبة؟")
        if data.relationship in {RelationshipContext.MANAGER, RelationshipContext.TEACHER}:
            objections.append("تنفع لمدير/مدرس من غير ما تبان مبالغ فيها؟")
        if data.relationship == RelationshipContext.MOTHER_IN_LAW:
            objections.append("تنفع لحماتي ومتبانش قليلة؟")
        if not data.buyer_knows_recipient_taste:
            objections.append("أنا مش عارف ذوقه/ذوقها، أختار إيه؟")
        if data.social_class_signal in {SocialClassSignal.VALUE_SENSITIVE, SocialClassSignal.MIDDLE_MAINSTREAM}:
            objections.append("السعر مناسب ولا أقدر أجيب حاجة أحسن؟")
        return objections

    @staticmethod
    def whatsapp_replies_for(data: GiftDecisionInput) -> List[str]:
        return [
            "تمام، قولنا المناسبة والميزانية والهدية لمين، ونرشحلك 3 اختيارات آمنة ومناسبة.",
            "الاختيار ده مناسب لأنه عملي وشكله محترم، وكمان نقدر نغلفه كهدية جاهزة.",
            "لو مش متأكد من الذوق، نرشحلك اختيارات آمنة اجتماعيًا ومش شخصية زيادة.",
            "في حالة الهدية للمناسبة القريبة، هنأكدلك التوفر والتغليف وميعاد التسليم قبل ما تطلب.",
        ]

    @staticmethod
    def seasonality_guidance(season: SeasonalityMoment) -> List[str]:
        guidance = {
            SeasonalityMoment.RAMADAN: ["ابدأ التحضير قبل رمضان بـ 21 يومًا.", "ركز على الهدايا العائلية والمجاملة والكرم."],
            SeasonalityMoment.EID: ["جهز عروض قبل العيد بـ 10-14 يومًا.", "ركز على التغليف الجاهز والتوصيل السريع."],
            SeasonalityMoment.MOTHERS_DAY: ["ابدأ حملات عيد الأم قبلها بـ 3 أسابيع.", "ركز على الامتنان والتقدير وليس الخصم فقط."],
            SeasonalityMoment.VALENTINE: ["افصل بين الهدايا الرومانسية والآمنة المحايدة.", "لا تستخدم زوايا محرجة لجمهور رسمي."],
            SeasonalityMoment.GRADUATION_SEASON: ["ركز على البداية الجديدة والشغل والجامعة.", "اعرض هدايا عملية قابلة للتصوير."],
            SeasonalityMoment.YEAR_END_CORPORATE: ["ركز على كميات الشركات والتغليف الموحد.", "وفر فاتورة وتنظيم تسليم."],
        }
        return guidance.get(season, ["اختبر الطلب بمحتوى دائم حسب المناسبة والميزانية.", "راقب بيانات واتساب والطلبات لتحديد الموسم الأقوى."])

    @staticmethod
    def crm_followups_for(data: GiftDecisionInput) -> List[str]:
        return [
            f"سجل المناسبة: {data.occasion.value}.",
            f"سجل العلاقة: {data.relationship.value}.",
            "سجل الميزانية والفئة السعرية المختارة.",
            "سجل تاريخ المناسبة لتذكير العميل قبلها بـ 14 يومًا في السنة القادمة.",
            "سجل هل العميل فضّل هدية عملية، رسمية، رومانسية، أو محايدة.",
        ]

    @staticmethod
    def evaluate(data: GiftDecisionInput) -> GiftDecisionResult:
        blind_spots: List[str] = []
        recommendations: List[str] = []

        product_fit = GiftDecisionIntelligenceEngine.product_to_occasion_fit(data.product.category, data.occasion, data.relationship)
        score = product_fit

        score += (data.product.perceived_value_score - 5) * 0.5
        score += (data.product.practicality_score - 5) * 0.35
        score += (data.product.packaging_score - 5) * 0.6
        score += (data.product.trust_score - 5) * 0.45
        score += (data.product.margin_score - 5) * 0.25

        if not data.product.stock_ready:
            score -= 1.2
            blind_spots.append("المنتج غير جاهز في المخزون؛ الإعلان عليه قد يخلق طلبًا لا يمكن تلبيته.")
            recommendations.append("لا تطلق إعلانًا قبل تأكيد المخزون والتغليف والقدرة على التسليم.")

        if not data.has_exchange_policy:
            score -= 0.8
            blind_spots.append("غياب سياسة الاستبدال يزيد خوف مشتري الهدية.")
            recommendations.append("أضف سياسة استبدال واضحة ومحدودة لتقليل تردد العميل.")

        if not data.has_real_photos:
            score -= 0.7
            blind_spots.append("غياب الصور الحقيقية يرفع خوف العميل من أن المنتج لا يشبه الإعلان.")
            recommendations.append("استخدم صور حقيقية للمنتج والتغليف قبل وبعد التحضير.")

        if not data.has_reviews:
            score -= 0.4
            blind_spots.append("لا يوجد إثبات اجتماعي كافٍ.")
            recommendations.append("اعرض آراء عملاء أو صور تسليم حقيقية لكل مناسبة.")

        if data.delivery_urgency in {DeliveryUrgency.SAME_DAY, DeliveryUrgency.NEXT_DAY}:
            score -= 0.6
            blind_spots.append("الهدية مرتبطة بموعد قريب؛ فشل التسليم يقتل قيمة الهدية.")
            recommendations.append("أظهر وعد تسليم واقعي ومناطق متاحة بوضوح، ولا تعد بتوصيل غير مضمون.")

        if not data.buyer_knows_recipient_taste:
            score -= 0.3
            blind_spots.append("المشتري لا يعرف ذوق متلقي الهدية؛ يحتاج ترشيحات آمنة بدل منتج واحد.")
            recommendations.append("اعرض 3 اختيارات: آمن، عملي، وشكله أغلى من سعره.")

        safety = GiftDecisionIntelligenceEngine.safety_verdict(data)
        if "خطر" in safety:
            score -= 1.5
            blind_spots.append(safety)
            recommendations.append("بدّل المنتج لهدية محايدة أو رسمية لتجنب سوء الفهم.")

        if data.geo_segment in {EgyptianGeoSegment.UPPER_EGYPT, EgyptianGeoSegment.DELTA} and data.product.safety_class == GiftSafetyClass.RISKY_MISUNDERSTOOD:
            score -= 0.8
            blind_spots.append("بعض المناطق أكثر حساسية للهدايا الشخصية أو غير المحايدة.")
            recommendations.append("استخدم هدايا عملية ومحترمة وابتعد عن الرسائل الشخصية الزائدة.")

        if data.social_class_signal == SocialClassSignal.VALUE_SENSITIVE and data.product.price_band == PriceBand.PREMIUM_AFFORDABLE:
            recommendations.append("برر السعر بالقيمة البصرية، التغليف، الاستخدام، وسياسة الاستبدال.")

        score = GiftDecisionIntelligenceEngine._bounded_score(score)
        risk = SocialRisk.LOW if score >= 8 else SocialRisk.MEDIUM if score >= 6 else SocialRisk.HIGH if score >= 4 else SocialRisk.CRITICAL

        if not blind_spots:
            blind_spots.append("لا توجد ثغرة حرجة ظاهرة، لكن يجب اختبار العرض بالبيانات الفعلية.")
        if not recommendations:
            recommendations.append("ابدأ باختبار صغير وراقب واتساب، التسليم، المرتجعات، وتكرار الشراء.")

        angle = f"هدية {data.occasion.value} {data.product.price_band.value}، مناسبة لـ {data.relationship.value}، بتغليف يليق واختيار يقلل الحيرة."
        positioning = "هدية عملية ومحترمة، مختارة حسب المناسبة والعلاقة والميزانية، لا تُباع كمنتج فقط بل كحل اجتماعي آمن."

        next_actions = [
            "اعمل Product-to-Occasion Matrix قبل الإعلان.",
            "جهز 3 اختيارات واتساب لكل مناسبة: آمن / عملي / شكله أغلى من سعره.",
            "اعرض التغليف والصور الحقيقية في الإعلان.",
            "ثبت سياسة استبدال بسيطة ومفهومة.",
            "سجل المناسبة في CRM لتذكير العميل لاحقًا.",
        ]
        next_actions.extend(GiftDecisionIntelligenceEngine.seasonality_guidance(data.seasonality))

        return GiftDecisionResult(
            score=score,
            risk_level=risk,
            product_occasion_fit=product_fit,
            safety_verdict=safety,
            positioning=positioning,
            recommended_angle=angle,
            blind_spots=blind_spots,
            recommendations=recommendations,
            objections=GiftDecisionIntelligenceEngine.objections_for(data),
            whatsapp_replies=GiftDecisionIntelligenceEngine.whatsapp_replies_for(data),
            crm_followups=GiftDecisionIntelligenceEngine.crm_followups_for(data),
            next_best_actions=next_actions,
        )

    @staticmethod
    def completeness_checklist() -> List[str]:
        return [
            "Product-to-Occasion Fit Matrix موجودة؟",
            "Buyer / Recipient / Payer Split واضح؟",
            "Gender & Relationship Safety متقيّم؟",
            "Geography & Class Lens متطبق؟",
            "Seasonality Window محدد؟",
            "Packaging Quality Score محسوب؟",
            "Trust & Scam Fear Signals موجودة؟",
            "Delivery Urgency Risk محسوب؟",
            "Objection Library جاهزة حسب العلاقة والمناسبة؟",
            "WhatsApp Replies جاهزة؟",
            "CRM Repeat Occasion Follow-up متسجل؟",
            "Stock Readiness متأكد قبل الإعلان؟",
            "Margin Score متوافق مع تكلفة الإعلان؟",
            "Real Photos/Reviews/Exchange Policy موجودين؟",
            "الرسالة لا تقول رخيص، بل قيمة ذكية وشكل محترم؟",
        ]
