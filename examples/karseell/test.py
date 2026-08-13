# -*- coding: utf-8 -*-
"""
🧪 KARSEELL MACA COLLAGEN — REAL-WORLD THINC™ v3.1 ANALYSIS
═══════════════════════════════════════════════════════════════════════════════

تطبيق فعلي للنموذج على منتج حقيقي من متجر AlHhomz (Shopify):
  - GID:        gid://shopify/Product/10416715170107
  - Title:      حمام كريم Karseell Maca Collagen 500ml
  - Vendor:     Karseell
  - Variants:   قطعة (1090 EGP) | قطعتين (1690 EGP)
  - Inventory:  18 (6 ثنائي + 12 فردي)

النموذج: THINC™ v3.1 — Generational Intelligence Edition
الملكية:  الدكتور إيهاب طه — EgyPioneers — طلائع شباب مصر
═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

# استيراد النموذج
import sys
sys.path.insert(0, str(Path(__file__).parent))

from THINC_v3_1_Master_Framework import (
    # Persona Layers
    IntegratedPersona,
    Layer1_Demographic, Layer2_Behavioral, Layer3_Psychological,
    Layer4_Emotional, Layer5_Motivational, Layer6_Objections, Layer7_Synthesis,
    CNCROverlay,
    # Layer 8 (v3.1)
    GenerationalIntelligenceEngine,
    EgyptianGeneration,
    # THINC Core
    THINCCore, Layer1_HumanBasis, Layer2_PsychologicalCore,
    Layer3_JobsToBeDone, Layer4_BehavioralTriggers, Layer5_ArabCulturalLens,
    TahaIndex,
    # Profit
    UnitEconomics, ProfitIntelligence,
    # Hooks + Equation
    HooksEngine, Hook, HookType, Neurochemical, PersonaLayer, GoldenEquation,
    # Composite
    CompositeScoreV3,
    # Watermark
    FRAMEWORK_VERSION, compute_identity_hash, get_watermark,
)

VERSION = FRAMEWORK_VERSION
IDENTITY_HASH = compute_identity_hash()
WATERMARK = get_watermark()


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1 · بيانات المنتج الحقيقية من Shopify
# ═══════════════════════════════════════════════════════════════════════════════

PRODUCT_DATA = {
    "shopify_gid": "gid://shopify/Product/10416715170107",
    "title": "حمام كريم Karseell Maca Collagen 500ml",
    "vendor": "Karseell",
    "product_type": "ماسك شعر",
    "tags": ["Karseell", "شعر جاف", "كولاجين", "ماسك شعر", "مقوي شعر"],
    "variants": {
        "single":  {"sku": "KARSEELL-MACA-500ML-1", "price": 1090.0, "inventory": 12},
        "bundle2": {"sku": "KARSEELL-MACA-500ML-2", "price": 1690.0, "inventory": 6},
    },
    "store": "alhhomz.myshopify.com",
    "currency": "EGP",
    "market": "Egypt",
}


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2 · بناء البيرسونا المتكاملة (8 طبقات + CNCR)
# ═══════════════════════════════════════════════════════════════════════════════

def build_karseell_persona() -> IntegratedPersona:
    """يبني بيرسونا 8 طبقات للعميلة المستهدفة لمنتج Karseell."""

    # ─────── Layer 1: الديموغرافية ───────
    demographic = Layer1_Demographic(
        age_range="24-38",
        gender="إناث",
        location="مصر — حضري (القاهرة الكبرى + الإسكندرية + المدن الجامعية)",
        income_class="B / B- / C+",
        education="جامعي",
        occupation="موظفة / طالبة جامعية / ربة منزل عاملة",
        social_status="متزوجة / مخطوبة / عزباء تهتم بمظهرها",
    )

    # ─────── Layer 2: السلوكية ───────
    behavioral = Layer2_Behavioral(
        browsing_habits=["إنستجرام Reels", "تيك توك ليلاً", "فيسبوك جروبات نسائية"],
        buying_behavior=["COD", "تحويل إنستاباي", "valU/Sympl للمنتجات أغلى من 1500"],
        purchase_frequency="شهري إلى كل شهرين (دورة الـ Hair Mask)",
        price_sensitivity="متوسطة-عالية (تبحث عن قيمة، لكن السعر >1000 يثير تردد)",
        content_preferences=[
            "Before/After 30 ثانية",
            "تجارب مؤثرات Beauty على تيك توك",
            "فيديو UGC حقيقي بدون فلاتر",
            "Reels تركيب وكشف نتيجة سريعة",
        ],
        triggers_attention=[
            "كلمة 'كولاجين' و 'ماكا'",
            "وعد علاج التقصف من أول استخدام",
            "عرض القطعتين (Bundle discount)",
        ],
    )

    # ─────── Layer 3: النفسية ───────
    psychological = Layer3_Psychological(
        core_values=["العناية بالنفس", "الأنوثة", "الثقة في المظهر"],
        aspirations=["شعر صحي لامع زي الإعلانات", "إحساس بـ self-care يومي"],
        pains=[
            "تقصف الأطراف بعد الصبغة/الفرد",
            "تساقط بعد الولادة أو الرضاعة",
            "إحباط متراكم من ماسكات فشلت قبل كده",
            "خوف من الصبغة والفرد بيخرّب الشعر",
        ],
        goals=[
            "شعر ناعم لامع بدون احتياج صالون",
            "تقليل التساقط",
            "ترميم تقصف الأطراف",
        ],
        fears=[
            "إهدار 1090 ج على منتج يطلع زي الباقي",
            "حساسية فروة الرأس من مكونات غريبة",
            "الكولاجين 'مية' ومش بيوصل لجذور الشعر",
        ],
    )

    # ─────── Layer 4: العاطفية ───────
    emotional = Layer4_Emotional(
        current_feeling="إحباط من حالة الشعر + شك في كل ماسك جديد",
        desired_feeling="ثقة + دلع + إحساس إنها 'بتاخد بالها من نفسها'",
        emotional_needs=["تقدير الذات", "نتيجة ملموسة", "أمان قبل الدفع"],
        happiness_sources=[
            "روتين العناية الأسبوعي مع ماسك",
            "تعليقات الزوج/الصاحبة على نعومة الشعر",
            "صورة جديدة للسوشيال بعد التريتمنت",
        ],
        frustration_triggers=[
            "ماسك بـ900+ ج وما حصلش فرق",
            "شعر مدهن وثقيل بعد الاستخدام",
            "ريحة كيماوية قوية",
        ],
    )

    # ─────── Layer 5: المحفزات ───────
    motivational = Layer5_Motivational(
        purchase_triggers=[
            "Before/After حقيقي (مش فوتوشوب)",
            "تقييم بنت تشبه نفسها (مش مؤثرة Premium)",
            "عرض القطعتين بتوفير 490 ج",
            "ضمان COD — تعاين قبل ما تدفع",
        ],
        attractive_offers=[
            "اشتري قطعتين بـ 1690 ج (بدل 2180)",
            "شحن مجاني فوق 1500 ج",
            "هدية مشط/منشفة مع الـ Bundle",
        ],
        influential_messages=[
            "كولاجين + ماكا = تركيبة بترمم من جوه",
            "آلاف العملاء قبلك جربوا واتغير شعرهم",
            "لو ما عجبكش، ارجعيه — COD",
        ],
        decision_drivers=[
            "COD",
            "تقييمات بالعربي على Shopify",
            "وصف عربي واضح (مش مترجم آلياً)",
            "WhatsApp Support قبل الشراء",
        ],
    )

    # ─────── Layer 6: الاعتراضات ───────
    objections = Layer6_Objections(
        price_objections=[
            "1090 ج للزجاجة الواحدة — أعلى من ماسكات السوبر ماركت بكتير",
            "ليه القطعتين بـ 1690 — هل ده عرض حقيقي ولا مرفّع الأصلي؟",
        ],
        trust_objections=[
            "الكولاجين بيتمتص فعلاً من الشعر؟",
            "Karseell براند صيني — هل أصلي ولا تقليد؟",
            "هاوصل لينا في القاهرة بإمتى؟",
        ],
        quality_objections=[
            "هل بيدّي نتيجة على الشعر المصبوغ؟",
            "بيخلي الشعر مدهن ولا لأ؟",
            "ريحته إيه؟ كيماوية ولا طبيعية؟",
        ],
        counter_messages=[
            "كل زجاجة 500ml تكفي 4-5 جلسات — يعني الجلسة بـ 218 ج (أرخص من الصالون)",
            "Karseell شركة معتمدة دولياً + فيديو فك التغليف يثبت أصالة",
            "شحن لكل محافظات مصر خلال 2-4 أيام + تتبع الشحنة",
            "آمن للشعر المصبوغ والمعالج كيميائياً",
        ],
        proof_required=[
            "فيديو Before/After لعميلة مصرية",
            "Screenshots لتقييمات Shopify",
            "تركيبة مكونات واضحة بالعربي",
            "ضمان إرجاع 7 أيام",
        ],
    )

    # ─────── Layer 7: الخلاصة ───────
    synthesis = Layer7_Synthesis(
        ideal_customer=(
            "بنت 24-38، طبقة B/C+، شعرها متضرر من صبغة/فرد/ولادة، "
            "جرّبت 2-3 ماسكات قبل كده وما عجبتهاش، نشطة على إنستجرام/تيك توك، "
            "بتدفع COD أو valU، وبتدور على نتيجة 'تستاهل الفلوس'"
        ),
        biggest_pain="إحباط متراكم من ماسكات فشلت + خوف من إهدار 1090 ج تاني",
        core_desire="شعر صحي لامع يخليها واثقة في صورها وفي نفسها",
        biggest_objection="هل بـ1090 ج هيدّي فعلاً نتيجة مختلفة عن غيره؟",
        strongest_trigger="Before/After حقيقي + COD + عرض القطعتين (1690 بدل 2180)",
        best_marketing_angle=(
            "📹 إثبات بصري (UGC Before/After) + 💰 توفير عرض الـ Bundle "
            "+ 🛡️ ضمان COD يكسر اعتراض السعر والثقة معاً"
        ),
    )

    # ─────── CNCR Overlay (الكيمياء العصبية) ───────
    cncr = CNCROverlay(
        enabled=True,
        cortisol_level=6.5,        # قلق ملموس من الإحباطات السابقة وسعر 1090
        norepinephrine_level=7.0,  # Hook بصري قوي ضروري في أول 3 ثوانٍ
        dopamine_level=7.5,        # مكافأة متوقعة عالية (شعر زي الإعلانات)
        oxytocin_level=4.0,        # الثقة منخفضة في براند صيني — ترميمها أولوية
        endorphins_level=6.0,      # متعة الاقتناء (روتين self-care)
        f_ego_risk=2.5,            # خطر التعالي منخفض — رسالة دافئة قريبة
    )

    return IntegratedPersona(
        product_name=PRODUCT_DATA["title"],
        demographic=demographic,
        behavioral=behavioral,
        psychological=psychological,
        emotional=emotional,
        motivational=motivational,
        objections=objections,
        synthesis=synthesis,
        cncr=cncr,
        # Layer 8 هتنبني في الخطوة 3
    )


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3 · Layer 8 — الذكاء الجيلي
# ═══════════════════════════════════════════════════════════════════════════════

def build_karseell_layer8(birth_year: int = 1994):
    """
    يبني Layer 8 للعميلة المستهدفة الأساسية (Gen Yanayer — Millennial مصري).
    1994 = العمر 32 في 2026، وسط الـ Sweet Spot لمنتج Hair Mask بـ 1090 ج.
    """
    layer = GenerationalIntelligenceEngine.build_layer(
        birth_year=birth_year,
        # نسبة الميديا (Reels/TikTok thoroughly internalized لكن FB لسه عالي)
        media_diet={
            "tiktok": 0.45, "instagram": 0.55, "facebook": 0.70,
            "youtube": 0.50, "tv": 0.20,
        },
        # تفضيل الدفع — COD لسه السائد لكن BNPL في صعود
        payment_preference={
            "cash": 0.55, "card": 0.20, "bnpl": 0.20, "wallet": 0.05,
        },
        # القيم الحالية vs قيم الأبوين (تحول واضح لكن مش جذري)
        current_values="self_expression_skeptical",   # Millennial مصري
        parent_values="achievement_pragmatism",        # Gen X (الانفتاح)
        reference_year=2026,
    )
    return layer


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 4 · THINC Core — Taha Index
# ═══════════════════════════════════════════════════════════════════════════════

def build_karseell_thinc_core() -> tuple[THINCCore, TahaIndex]:
    """يبني الطبقات الخمس الأكاديمية ويحسب مؤشر طه."""

    core = THINCCore(
        # L1: ماسلو — تقدير الذات + الانتماء الجمالي
        human_basis=Layer1_HumanBasis(
            physiological=4.0,        # احتياج عناية بسيط، مش بقاء
            safety=5.0,                # أمان من تلف الشعر
            belonging=7.5,             # الانتماء لمعايير الجمال الاجتماعية
            esteem=8.5,                # تقدير الذات هو المحرك الأقوى
            self_actualization=6.0,    # شعر صحي = تعبير عن الذات
        ),
        # L2: نفسي عميق
        psychological=Layer2_PsychologicalCore(
            primary_motivation="استعادة الثقة في المظهر بعد ضرر تراكمي",
            cognitive_biases=[
                "Loss Aversion (خوف من إهدار فلوس تاني)",
                "Social Proof (تعليقات/تقييمات)",
                "Anchoring (سعر القطعتين 1690 يجعل القطعة 1090 تبدو مقبولة)",
                "Confirmation Bias (تبحث عن تجارب نجاح فقط)",
            ],
            decision_style="مختلط — عاطفي في الـ Trigger + منطقي قبل الـ Checkout",
        ),
        # L3: JTBD
        jtbd=Layer3_JobsToBeDone(
            functional_job="ترميم تقصف وتساقط + ترطيب عميق للشعر الجاف",
            emotional_job="استعادة الثقة بمظهر الشعر بعد فترة إحباط",
            social_job="إثبات إنها 'بتاخد بالها من نفسها' في صور السوشيال والمناسبات",
        ),
        # L4: 16 محرك (نختار الـ Top بقوة 7+)
        behavioral=Layer4_BehavioralTriggers(
            driver_scores={
                "Social Influence & Relatedness": 8.5,
                "Scarcity & Impatience": 7.0,         # عرض القطعتين محدود
                "Loss & Avoidance": 8.0,               # خوف من الإهدار
                "Social Proof": 9.0,                    # UGC + تقييمات
                "Authority": 6.5,                       # براند Karseell معتمد دولياً
                "Liking": 7.5,                          # المؤثرات اللي زيها
                "Attractive / Delighter Quality": 8.0, # ماكا + كولاجين = wow
                "Ownership & Possession": 7.5,         # روتين Self-care
            }
        ),
        # L5: العدسة العربية
        cultural=Layer5_ArabCulturalLens(
            cod_preference=True,                       # 60%+ من الطلبات COD
            social_proof_weight="عالٍ جداً",          # تقييمات الجروبات النسائية
            authenticity_value="عالٍ",                 # الخوف من 'تقليد'
            family_influence="متوسط — رأي الأم/الأخت في الشعر مهم",
            religious_cultural_notes=[
                "الشعر زينة — استثمار مقبول دينياً واجتماعياً",
                "تجنّب أي مكونات 'حرام' أو كحولية في الوصف",
            ],
            local_dialect_keywords=[
                "هتبقي تحفة", "شعرك هيرجع زي زمان", "بنحافظ عليكي",
                "جربي وأنتي مرتاحة", "العرض هيخلص", "ندامة لو فاتك",
            ],
        ),
    )

    # حساب مؤشر طه (Taha Index)
    taha = TahaIndex(
        human_basis_score=7.0,    # متوسط الـ L1 المرجح
        psychological_score=8.5,  # القلق + الـ Self-esteem محركان قويان
        jtbd_score=8.0,           # كل المهام الثلاث مغطاة
        behavioral_score=8.0,     # 8 محركات بقوة 7+
        cultural_score=8.5,       # COD + Social Proof + Authenticity — تطابق ممتاز
    )

    return core, taha


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 5 · Profit Intelligence
# ═══════════════════════════════════════════════════════════════════════════════

def build_karseell_profit_single() -> ProfitIntelligence:
    """اقتصاديات الوحدة لقطعة واحدة (1090 EGP)."""
    eco = UnitEconomics(
        selling_price=1090.0,
        cogs=380.0,                          # تكلفة من الصين + جمارك + مخزن
        shipping_cost=60.0,                  # شحن COD داخل مصر
        packaging_cost=25.0,
        payment_processing_fee=0.025,        # 2.5% Paymob/Fawry لو إلكتروني
        return_rate_percentage=0.12,         # 12% (مرتجع عادي COD)
        customer_service_cost=20.0,
        platform_commission_percentage=0.0,  # متجر Shopify خاص — لا توجد عمولة منصة
    )
    return ProfitIntelligence(
        unit_economics=eco,
        expected_cac=220.0,                  # CPA متوقع من حملات Meta
        expected_ltv=2400.0,                 # عميلة بترجع كل شهرين = 2-3 شراء/سنة
        repeat_purchase_rate=0.35,
    )


def build_karseell_profit_bundle() -> ProfitIntelligence:
    """اقتصاديات الوحدة لـ Bundle قطعتين (1690 EGP) — الهامش الأعلى."""
    eco = UnitEconomics(
        selling_price=1690.0,
        cogs=760.0,                          # 380 × 2
        shipping_cost=60.0,                  # شحنة واحدة
        packaging_cost=35.0,                 # كرتونة أكبر
        payment_processing_fee=0.025,
        return_rate_percentage=0.10,         # أقل (لأنها مرتبة Bundle مدروسة)
        customer_service_cost=25.0,
        platform_commission_percentage=0.0,
    )
    return ProfitIntelligence(
        unit_economics=eco,
        expected_cac=220.0,
        expected_ltv=3200.0,                 # AOV أعلى + ولاء أعلى
        repeat_purchase_rate=0.40,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 6 · Hooks Engine + Golden Equation
# ═══════════════════════════════════════════════════════════════════════════════

def build_karseell_hooks() -> HooksEngine:
    """5 Hooks مدمجة بالكيمياء العصبية والطبقات."""
    h = HooksEngine()
    h.add_hook(
        HookType.PAIN,
        "شعرك بقى يقع بكميات وكل ماسك بتجربيه طلع زي اللي قبله؟",
        Neurochemical.CORTISOL, PersonaLayer.EMOTIONAL,
    )
    h.add_hook(
        HookType.RESULT,
        "كولاجين + ماكا = نعومة ولمعان من أول حمام كريم — Before/After شغل أصول",
        Neurochemical.DOPAMINE, PersonaLayer.MOTIVATIONAL,
    )
    h.add_hook(
        HookType.SOCIAL_PROOF,
        "آلاف البنات قبلك جربوا Karseell ورجع شعرهم زي زمان — اقري التقييمات",
        Neurochemical.OXYTOCIN, PersonaLayer.PSYCHOLOGICAL,
    )
    h.add_hook(
        HookType.OFFER,
        "اشتري قطعتين بـ 1690 بدل 2180 — وفّري 490 ج (العرض محدود لـ 6 قطع بس)",
        Neurochemical.NOREPINEPHRINE, PersonaLayer.MOTIVATIONAL,
    )
    h.add_hook(
        HookType.OBJECTION_BREAK,
        "ادفعي عند الاستلام — تعايني الزجاجة وتفتحيها قبل ما تدفعي مليم",
        Neurochemical.OXYTOCIN, PersonaLayer.OBJECTIONS,
    )
    return h


def build_karseell_golden_equation() -> GoldenEquation:
    """المعادلة الذهبية لرسالة Karseell."""
    return GoldenEquation(
        clear_problem="شعرك تالف من الصبغة والفرد، وكل ماسك جربتيه طلع خيبة؟",
        purchase_trigger="حمام كريم كارسيل بالماكا والكولاجين بنتيجة من أول استخدام،",
        psychological_drive="عشان ترجعي تحبي شعرك وصورتك",
        real_desire="بنعومة ولمعان زي قبل ما يضرّب",
        objection_break=(
            "والقطعتين بـ 1690 بدل 2180 + الدفع عند الاستلام — "
            "تعاينيه قبل ما تدفعي."
        ),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 7 · المحرك الرئيسي — تشغيل التحليل الكامل
# ═══════════════════════════════════════════════════════════════════════════════

def run_full_analysis() -> dict:
    """يشغّل التحليل الكامل ويرجع كل النتائج في dict واحد."""

    # 1) بناء البيرسونا
    persona = build_karseell_persona()

    # 2) بناء Layer 8 — الذكاء الجيلي
    layer8 = build_karseell_layer8(birth_year=1994)
    persona.generational = layer8

    # 3) THINC Core + Taha Index
    thinc_core, taha_idx = build_karseell_thinc_core()

    # 4) Profit Intelligence — للسيناريوهين
    profit_single = build_karseell_profit_single()
    profit_bundle = build_karseell_profit_bundle()

    # 5) Hooks + Golden Equation
    hooks = build_karseell_hooks()
    equation = build_karseell_golden_equation()

    # 6) حساب التوافق الجيلي و Decision Modifiers
    gen_alignment = GenerationalIntelligenceEngine.compute_alignment(layer8)
    decision_mods = GenerationalIntelligenceEngine.get_decision_modifiers(layer8)

    # 7) Composite Score — للسيناريوهين
    composite_single = CompositeScoreV3(
        persona_completeness=persona.completeness_score(),
        taha_index=taha_idx.calculate(),
        profitability_score=profit_single.profitability_score(),
        reality_score=-1,  # لسه ماتعملش حملة اختبار
        generational_alignment=gen_alignment,
    ).calculate()

    composite_bundle = CompositeScoreV3(
        persona_completeness=persona.completeness_score(),
        taha_index=taha_idx.calculate(),
        profitability_score=profit_bundle.profitability_score(),
        reality_score=-1,
        generational_alignment=gen_alignment,
    ).calculate()

    return {
        "product": PRODUCT_DATA,
        "persona": persona,
        "thinc_core": thinc_core,
        "taha_index": taha_idx,
        "profit_single": profit_single,
        "profit_bundle": profit_bundle,
        "hooks": hooks,
        "equation": equation,
        "layer8": layer8,
        "generational_alignment": gen_alignment,
        "decision_modifiers": decision_mods,
        "composite_single": composite_single,
        "composite_bundle": composite_bundle,
        "watermark": WATERMARK,
        "version": VERSION,
        "identity_hash": IDENTITY_HASH,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 8 · توليد تقرير Markdown احترافي
# ═══════════════════════════════════════════════════════════════════════════════

def generate_markdown_report(r: dict) -> str:
    """يولّد تقرير Markdown شامل من نتائج التحليل."""

    p = r["persona"]
    e_s = r["profit_single"].unit_economics
    pi_s = r["profit_single"]
    e_b = r["profit_bundle"].unit_economics
    pi_b = r["profit_bundle"]
    bes = pi_s.calculate_break_even_cpa()
    beb = pi_b.calculate_break_even_cpa()
    cs = r["composite_single"]
    cb = r["composite_bundle"]
    l8 = r["layer8"]
    mods = r["decision_modifiers"]

    md = f"""# 🧪 تقرير THINC™ v3.1 — تحليل حقيقي لمنتج Karseell

> **التاريخ:** {datetime.now().strftime("%Y-%m-%d %H:%M")} (توقيت القاهرة)
> **المنتج:** {r['product']['title']}
> **المتجر:** {r['product']['store']} | **العملة:** {r['product']['currency']}
> **النموذج:** THINC™ {r['version']}
> **Identity Hash:** `{r['identity_hash'][:16]}...`

---

## 🎯 الملخص التنفيذي (TL;DR)

| السيناريو | السعر | Composite Score | الدرجة | الربحية | Break-Even CPA |
|---|---|---|---|---|---|
| **قطعة واحدة** | 1090 EGP | **{cs['score']}** | {cs['grade'].split('—')[0].strip()} | {pi_s.profitability_score()}/10 | {bes['value']} EGP |
| **Bundle قطعتين** ⭐ | 1690 EGP | **{cb['score']}** | {cb['grade'].split('—')[0].strip()} | {pi_b.profitability_score()}/10 | {beb['value']} EGP |

**🏆 التوصية النهائية:** _ادفع Bundle (1690 EGP) كـ Default Offer — هامش أعلى، ولاء أعلى، Reality أعلى._

---

## 📦 بيانات المنتج (من Shopify Live)

- **GID:** `{r['product']['shopify_gid']}`
- **Vendor:** {r['product']['vendor']} | **Type:** {r['product']['product_type']}
- **Tags:** {", ".join(r['product']['tags'])}
- **Variants:**
  - 🔵 قطعة واحدة: **1090 EGP** | SKU: `KARSEELL-MACA-500ML-1` | مخزون: 12
  - 🟢 قطعتين (Bundle): **1690 EGP** | SKU: `KARSEELL-MACA-500ML-2` | مخزون: 6

---

## 🎭 البيرسونا المتكاملة (8 طبقات + CNCR)

**نسبة الاكتمال:** {p.completeness_score()}%

### الطبقة 1 — الديموغرافية
{p.demographic.summary()}

### الطبقة 7 — الخلاصة (Synthesis)
- **العميلة المثالية:** {p.synthesis.ideal_customer}
- **أكبر ألم:** {p.synthesis.biggest_pain}
- **الرغبة الجوهرية:** {p.synthesis.core_desire}
- **أقوى اعتراض:** {p.synthesis.biggest_objection}
- **أقوى محفز:** {p.synthesis.strongest_trigger}
- **🎯 أفضل زاوية تسويقية:** {p.synthesis.best_marketing_angle}

### الطبقة 8 — الذكاء الجيلي (v3.1)
{l8.to_summary()}

- **الجيل:** {l8.identity.generation_code.value}
- **مرحلة الحياة:** {l8.identity.current_life_stage.value}
- **البصمة الاقتصادية:** `{l8.memory.economic_imprint}` — صدمة التضخم بصمت العقل الشرائي
- **التوافق الجيلي (Alignment):** **{r['generational_alignment']:.3f}** / 1.000

### CNCR Overlay — الكيمياء العصبية
| المؤشر | القيمة | التفسير |
|---|---|---|
| Cortisol (التوتر) | {p.cncr.cortisol_level}/10 | قلق ملموس — يحتاج Oxytocin Hook |
| Norepinephrine (الانتباه) | {p.cncr.norepinephrine_level}/10 | Hook بصري قوي في أول 3 ثوانٍ |
| Dopamine (المكافأة) | {p.cncr.dopamine_level}/10 | D² = {p.cncr.get_dopamine_squared()} |
| Oxytocin (الثقة) | {p.cncr.oxytocin_level}/10 | **منخفضة — أولوية الترميم** |
| Endorphins (المتعة) | {p.cncr.endorphins_level}/10 | روتين Self-care |
| F_ego (خطر التعالي) | {p.cncr.f_ego_risk}/10 | آمن — رسالة دافئة قريبة |

**توصيات الكيمياء:**
{chr(10).join(f"- **{k}:** {v}" for k, v in p.cncr.get_chemistry_recommendation().items())}

---

## 📊 مؤشر طه (Taha Index)

| الطبقة | الدرجة |
|---|---|
| L1 — الأساس الإنساني (ماسلو) | {r['taha_index'].human_basis_score} |
| L2 — الدوافع النفسية | {r['taha_index'].psychological_score} |
| L3 — المهام المنجزة (JTBD) | {r['taha_index'].jtbd_score} |
| L4 — المحركات السلوكية | {r['taha_index'].behavioral_score} |
| L5 — العدسة الثقافية | {r['taha_index'].cultural_score} |
| **🏆 Taha Index** | **{r['taha_index'].calculate()}/10** |

> **JTBD ثلاثي الأبعاد:** {r['thinc_core'].jtbd.summary()}

---

## 💰 ذكاء الربحية (Profit Intelligence)

### سيناريو 1: قطعة واحدة (1090 EGP)
- **Gross Profit/Order:** {e_s.gross_profit()} EGP ({e_s.gross_margin_pct()}%)
- **Break-Even CPA:** **{bes['value']} EGP** ({bes['status']})
- **Net Profit/Order @ CPA=220:** {pi_s.net_profit_per_order()} EGP
- **LTV/CAC:** {pi_s.ltv_cac_ratio()['display']} — {pi_s.ltv_cac_ratio()['message']}
- **Profitability Score:** **{pi_s.profitability_score()}/10**

### سيناريو 2: Bundle قطعتين (1690 EGP) ⭐ الموصى به
- **Gross Profit/Order:** {e_b.gross_profit()} EGP ({e_b.gross_margin_pct()}%)
- **Break-Even CPA:** **{beb['value']} EGP** ({beb['status']})
- **Net Profit/Order @ CPA=220:** {pi_b.net_profit_per_order()} EGP
- **LTV/CAC:** {pi_b.ltv_cac_ratio()['display']} — {pi_b.ltv_cac_ratio()['message']}
- **Profitability Score:** **{pi_b.profitability_score()}/10**

**🔑 الفرق:** Bundle يمنحك **{round(e_b.gross_profit() - e_s.gross_profit(), 2)} EGP** ربح إضافي لكل طلب + هامش CPA أكبر بـ **{round(beb['value'] - bes['value'], 2)} EGP**.

---

## 🪝 محرك الـ Hooks (5 أنواع مغطاة)

"""
    for hook in r["hooks"].hooks:
        md += f"### {hook.hook_type.value} → {hook.target_neurochemical.value if hook.target_neurochemical else '—'}\n"
        md += f"> {hook.text}\n\n"

    md += f"""---

## 🏆 المعادلة الذهبية (Golden Equation)

**الرسالة المُركَّبة:**
> {r['equation'].compose_message()}

**اكتمال:** {"✅ كاملة (5/5)" if r['equation'].is_complete() else "⚠️ ناقصة"}

---

## 🗿 معدّلات القرار من الطبقة الجيلية (Decision Modifiers)

- **Force Reality Check:** {"✅ نعم" if mods['force_reality_check'] else "❌ لا"}
- **Mandatory Hook:** {mods['mandatory_hook'] or "غير إلزامي"}
- **Framing الموصى:** {", ".join(mods['framing']) if mods['framing'] else "—"}
- **Payment Integrations المقترحة:** {", ".join(mods['payment_integrations']) if mods['payment_integrations'] else "—"}
- **تحذيرات:**
{chr(10).join(f"  - ⚠️ {w}" for w in mods['warnings']) if mods['warnings'] else "  - لا توجد"}

---

## 🎯 Composite Score v3.1 — الدرجة المركّبة النهائية

### سيناريو القطعة الواحدة
- **Raw Score (قبل الجيل):** {cs['raw_score_before_generational']}
- **Generational Multiplier:** ×{cs['generational_multiplier']}
- **🎯 Final Score:** **{cs['score']}/10**
- **Grade:** {cs['grade']}
- **مكونات الدرجة:** {cs['components']}
{"- **⚠️ Missing:** " + ", ".join(cs['missing']) if cs['missing'] else ""}

### سيناريو Bundle
- **Raw Score:** {cb['raw_score_before_generational']}
- **Generational Multiplier:** ×{cb['generational_multiplier']}
- **🎯 Final Score:** **{cb['score']}/10**
- **Grade:** {cb['grade']}
- **مكونات الدرجة:** {cb['components']}

---

## 📋 خطة التنفيذ التالية (Action Plan)

### المرحلة 1 — قبل الإعلان (هذا الأسبوع)
1. ✅ تحضير **3 فيديوهات UGC** Before/After من 30 ثانية (شكل تيك توك)
2. ✅ كتابة **6 Primary Texts** بالكيمياء الكلامية (2 Cortisol + 2 Dopamine + 2 Oxytocin)
3. ✅ تجهيز صفحة المنتج بترجمة عربية احترافية + 4 تقييمات حقيقية بصور
4. ✅ تفعيل **valU + Sympl** على Bundle (1690 EGP يدخل في Eligible Range)

### المرحلة 2 — Reality Validation (أسبوع كامل، ميزانية 1500 EGP)
- **الفرضية:** UGC Before/After + COD يمكن أن يدفع CPA ≤ {bes['value']} EGP
- **الكرياتيف:** 4 فيديوهات × 4 زوايا = 16 إعلان
- **الجمهور:** Cold 50% / Lookalike 30% / Retargeting 20%
- **الـ KPI الحاسم:** Delivered CPA ≤ **{round(bes['value'] * 0.7, 2)} EGP** = Scale Ready

### المرحلة 3 — Scale (بعد Validation ناجح)
- وسّع 25% أسبوعياً بنفس الكرياتيف الفائز
- ابدأ TikTok Ads بعد ما Meta يثبت Profitability
- اطلق **حملة WhatsApp Retargeting** للعملاء اللي عاينوا ولم يشتروا

---

## 🔬 الفرضيات للاختبار (Reality Validation Hypotheses)

| # | النوع | الفرضية | KPI المتوقع |
|---|---|---|---|
| H1 | CREATIVE | UGC Before/After أقوى من فيديو احترافي | CTR ≥ 1.5% |
| H2 | OFFER | Bundle 1690 سيمثّل 60%+ من المبيعات | Bundle Share ≥ 60% |
| H3 | PRICE | 1090 سعر مقبول مع COD رغم التضخم | Conversion ≥ 1.8% |
| H4 | TRUST | تقييمات Shopify بالعربي تقلل اعتراض الثقة | Bounce Rate ≤ 60% |
| H5 | CHANNEL | TikTok Ads أرخص CPC من Meta لشعر | TikTok CPA ≤ Meta CPA |

---

## ⚠️ نقاط الانتباه (Warnings)

1. **خطر اسم البراند:** Karseell صيني — يجب التأكد من **GTIN/Trademark protection** قبل التوسع لـ Amazon Egypt
2. **مخزون محدود:** 6 Bundle + 12 Single = إذا CPA = 220، فأسبوع توسع كافي لاستنزاف المخزون
3. **{l8.memory.economic_imprint}:** البصمة التضخمية تعني أن **Framing القيمة (Value Protection) أهم من Framing السعر**
4. **Oxytocin منخفض:** أي رسالة بـ "أصلي 100%" أو "بدون تقليد" هتفتح ثغرة ثقة قاتلة

---

{r['watermark']}
"""
    return md


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 9 · MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 75)
    print("🧪 THINC™ v3.1 — تحليل حقيقي على Karseell Maca Collagen")
    print("=" * 75)

    results = run_full_analysis()

    # طباعة الملخص في الـ stdout
    p = results["persona"]
    cs = results["composite_single"]
    cb = results["composite_bundle"]
    print(f"\n✅ Persona Completeness: {p.completeness_score()}%")
    print(f"✅ Taha Index: {results['taha_index'].calculate()}/10")
    print(f"✅ Generational Alignment: {results['generational_alignment']:.3f}")
    print("\n📊 SCENARIO 1 — Single (1090 EGP):")
    print(f"   Composite Score: {cs['score']}/10 — {cs['grade']}")
    print(f"   Break-Even CPA: {results['profit_single'].break_even_value()} EGP")
    print(f"   Profitability: {results['profit_single'].profitability_score()}/10")
    print("\n📊 SCENARIO 2 — Bundle (1690 EGP):")
    print(f"   Composite Score: {cb['score']}/10 — {cb['grade']}")
    print(f"   Break-Even CPA: {results['profit_bundle'].break_even_value()} EGP")
    print(f"   Profitability: {results['profit_bundle'].profitability_score()}/10")

    # حفظ التقرير Markdown
    report_md = generate_markdown_report(results)
    report_path = Path(__file__).parent / "karseell_thinc_v31_report.md"
    report_path.write_text(report_md, encoding="utf-8")
    print(f"\n📄 التقرير محفوظ: {report_path}")

    # حفظ JSON snapshot
    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "product_title": PRODUCT_DATA["title"],
        "scenarios": {
            "single": {
                "price": 1090, "composite_score": cs["score"], "grade": cs["grade"],
                "break_even_cpa": results["profit_single"].break_even_value(),
                "profitability": results["profit_single"].profitability_score(),
                "gross_profit": results["profit_single"].unit_economics.gross_profit(),
            },
            "bundle": {
                "price": 1690, "composite_score": cb["score"], "grade": cb["grade"],
                "break_even_cpa": results["profit_bundle"].break_even_value(),
                "profitability": results["profit_bundle"].profitability_score(),
                "gross_profit": results["profit_bundle"].unit_economics.gross_profit(),
            },
        },
        "generational_alignment": results["generational_alignment"],
        "persona_completeness": p.completeness_score(),
        "taha_index": results["taha_index"].calculate(),
        "decision_modifiers": results["decision_modifiers"],
        "version": results["version"],
        "identity_hash": results["identity_hash"],
    }
    json_path = Path(__file__).parent / "karseell_thinc_v31_snapshot.json"
    json_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"📊 JSON snapshot: {json_path}")
    print(f"\n{results['watermark']}")
