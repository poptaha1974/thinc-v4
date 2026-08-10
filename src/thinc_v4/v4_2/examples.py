# -*- coding: utf-8 -*-
"""Reference examples for the THINC v4.2 layer.

THINC™ v4.2 — Invented by Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 Dr. Ehab Taha — Egy-Pioneers Academy.
"""
from __future__ import annotations

from .competitive import (
    CompetitiveIntelligence,
    CompetitorProfile,
)
from .composite import (
    THINCV4Engine,
    THINCV4ProjectInput,
    THINCV4Report,
)
from .creative_models import (
    EgyptianConsumerPersona,
    ProductFeature,
    ProductIntelligenceInput,
    ProductProblem,
)
from .egyptianization import (
    AudienceSkillLevel,
    EgyptianAudienceGeneration,
)
from .founder import FounderOS
from .media_models import (
    EvidenceMode,
    MediaEconomicsInput,
    MediaTestConfig,
    MediaTestProtocolReport,
    SalesChannel,
)
from .media_protocol import MediaTestProtocolEngine
from .reporting import (
    CreativeIntelligenceReport,
    THINCCreativeIntelligenceLayer,
)


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
