# -*- coding: utf-8 -*-
"""Creative intelligence engines: deconstruction, angles, montage, experiments, winners.

THINC™ v4.2 — Invented by Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 Dr. Ehab Taha — Egy-Pioneers Academy.
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple
from .creative_models import (
    AdvertisingAngle,
    AngleArchetype,
    CreativeBlueprint,
    CreativeFormat,
    CreativePerformance,
    CreativeVariant,
    EgyptianConsumerPersona,
    ProductIntelligenceInput,
    StoryboardBeat,
    WinnerDecision,
)


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
