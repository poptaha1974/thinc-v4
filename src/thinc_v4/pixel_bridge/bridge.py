# -*- coding: utf-8 -*-
"""
🌉 PIXEL FEEDBACK BRIDGE — حلقة التغذية العكسية بين Meta Pixel و Layer 8
═══════════════════════════════════════════════════════════════════════════════

الفلسفة:
  Meta Pixel/CAPI بيرسل أحداث الشراء الحقيقية (Purchase events)، كل حدث بيحتوي:
    - بيانات العميل المهشّرة (age, city, payment_method)
    - قيمة الطلب (value, currency)
    - حالة التسليم (delivered/cancelled)

  الجسر (Bridge) بياخد دفعات من الأحداث دي ويستخرج منها:
    1. التوزيع السلوكي الفعلي لكل جيل (media_diet, payment_preference)
    2. تحوّلات Generational Value Shift Index (GVSI) من سلوك حقيقي
    3. أحداث مؤسِّسة جديدة (Formative Events) لو رصد تغيّر مفاجئ في النمط

  ثم يحدث Layer 8 تلقائياً عبر:
    - GenerationalIntelligenceEngine.update_norms_from_research()
    - GenerationalIntelligenceEngine.register_new_formative_event()

ملكية: د. إيهاب طه — EgyPioneers — طلائع شباب مصر
الإصدار: v3.1 — Generational Intelligence Edition
═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Allow imports from the bundled v3.1 framework regardless of how the package
# is consumed (editable install, CI checkout, or zip snapshot).
_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parents[3]
_LEGACY_DIR = _REPO_ROOT / "thinc_v4_0_final_verified_20260620" / "thinc_v4_final"
for _candidate in (_HERE, _REPO_ROOT, _LEGACY_DIR):
    if _candidate.exists() and str(_candidate) not in sys.path:
        sys.path.insert(0, str(_candidate))

try:
    from THINC_v3_1_Master_Framework import (
        EGYPTIAN_FORMATIVE_EVENTS,
        GENERATIONAL_NORMS,
        EgyptianGeneration,
        GenerationalIntelligenceEngine,
        OrderStatus,
        get_watermark,
    )
except Exception:  # pragma: no cover - fallback to legacy bundled name
    from THINC_v3_1_Master_Framework_Chatgpt import (
        EGYPTIAN_FORMATIVE_EVENTS,
        GENERATIONAL_NORMS,
        EgyptianGeneration,
        GenerationalIntelligenceEngine,
        OrderStatus,
        get_watermark,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 1) PIXEL EVENT MODEL — صياغة موحّدة لحدث Meta
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class PixelPurchaseEvent:
    """
    📡 حدث Purchase موحّد قادم من Meta CAPI أو Shopify Webhook.

    ما نخزّنش PII خام — نحتفظ فقط بحقول التحليل المجمّع.
    """
    event_time: datetime
    order_id: str
    value: float
    currency: str = "EGP"

    # حقول جيلية (لا تحتوي PII — كلها فئات/buckets)
    birth_year: int | None = None      # نشتقها من سنة الميلاد المسجّلة في Shopify
    age_bucket: str = ""                  # "18-24", "25-34", "35-44", "45+"
    city: str = ""                        # القاهرة / الجيزة / الإسكندرية ... (مش zip)
    governorate: str = ""

    payment_method: str = ""              # cash / card / bnpl / wallet
    device_type: str = ""                 # mobile / desktop / tablet
    traffic_source: str = ""              # tiktok / instagram / facebook / youtube / direct

    delivery_status: str = "pending"      # delivered / cancelled / returned / pending
    delivered_at: datetime | None = None

    is_repeat_customer: bool = False

    def is_completed(self) -> bool:
        """هل الحدث قابل للحساب الجيلي؟ (مُسلَّم + غير ملغي)"""
        return self.delivery_status.lower() in ("delivered", "تم التسليم", "مستلم")

    def derive_birth_year(self, current_year: int = 2026) -> int | None:
        """يستنتج سنة الميلاد من age_bucket لو مش متاحة."""
        if self.birth_year:
            return self.birth_year
        bucket_to_year = {
            "13-17": current_year - 15,
            "18-24": current_year - 21,
            "25-34": current_year - 29,
            "35-44": current_year - 39,
            "45-54": current_year - 49,
            "55-64": current_year - 59,
            "65+":   current_year - 70,
        }
        return bucket_to_year.get(self.age_bucket)


# ═══════════════════════════════════════════════════════════════════════════════
# 2) GENERATIONAL ROLLUP — تجميع الأحداث حسب الجيل
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class GenerationalRollup:
    """📊 تجميع إحصائي لجيل واحد عبر فترة زمنية."""
    generation_code: str
    total_purchases: int = 0
    total_value: float = 0.0
    delivery_rate: float = 0.0

    payment_distribution: Dict[str, float] = field(default_factory=dict)
    traffic_distribution: Dict[str, float] = field(default_factory=dict)
    device_distribution: Dict[str, float] = field(default_factory=dict)
    top_cities: List[Tuple[str, int]] = field(default_factory=list)

    repeat_rate: float = 0.0
    avg_order_value: float = 0.0

    def has_significant_sample(self, min_n: int = 30) -> bool:
        """🔬 لا نحدث الـ norms بعينة أقل من 30 طلب — Statistical Significance."""
        return self.total_purchases >= min_n


# ═══════════════════════════════════════════════════════════════════════════════
# 3) PIXEL FEEDBACK BRIDGE — المحرك الرئيسي
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class PixelFeedbackBridge:
    """
    🌉 الجسر بين Pixel Reality و Layer 8 Theory.

    دورة الحياة:
      1. ingest_events(events)              ← يستقبل دفعة Purchase events
      2. rollup_by_generation()             ← يجمّع إحصائياً حسب الجيل
      3. detect_anomalies()                 ← يرصد تحولات مفاجئة (>30% shift)
      4. update_generational_norms()        ← يحدث GENERATIONAL_NORMS تلقائياً
      5. propose_new_formative_events()     ← يقترح أحداث مؤسِّسة جديدة
      6. generate_feedback_report()         ← تقرير تنفيذي

    العتبة الإحصائية:
      - تحديث norms يحتاج ≥30 حدث/جيل
      - رصد تحول جذري (anomaly) يحتاج ≥50% تغيير عن baseline
      - اقتراح Formative Event جديد يحتاج إجماع 3 أجيال على نفس النمط
    """
    min_sample_per_generation: int = 30
    anomaly_threshold: float = 0.50      # 50% تغيّر = anomaly
    reference_year: int = 2026

    _events: List[PixelPurchaseEvent] = field(default_factory=list)
    _rollups: Dict[str, GenerationalRollup] = field(default_factory=dict)
    _anomalies: List[Dict[str, Any]] = field(default_factory=list)
    _norms_updated: List[str] = field(default_factory=list)
    _events_registered: List[str] = field(default_factory=list)

    # ─────────────────────────────────────────────────────────────────────────
    # PHASE 1 · INGEST
    # ─────────────────────────────────────────────────────────────────────────

    def ingest_events(self, events: List[PixelPurchaseEvent]) -> Dict[str, Any]:
        """يستقبل أحداث Purchase ويفلتر المُسلَّم منها فقط (Golden Rule)."""
        before = len(self._events)
        delivered = [e for e in events if e.is_completed()]
        self._events.extend(delivered)
        return {
            "ingested_raw": len(events),
            "ingested_delivered": len(delivered),
            "rejected_pending_or_cancelled": len(events) - len(delivered),
            "total_in_bridge": len(self._events),
            "added_this_batch": len(self._events) - before,
        }

    # ─────────────────────────────────────────────────────────────────────────
    # PHASE 2 · ROLLUP
    # ─────────────────────────────────────────────────────────────────────────

    def rollup_by_generation(self) -> Dict[str, GenerationalRollup]:
        """يجمّع الأحداث حسب الجيل ويحسب التوزيعات الفعلية."""
        buckets: Dict[str, List[PixelPurchaseEvent]] = defaultdict(list)

        for evt in self._events:
            by = evt.derive_birth_year(self.reference_year)
            if by is None:
                continue
            gen = GenerationalIntelligenceEngine.detect_generation(
                by, self.reference_year
            )
            buckets[gen.generation_code.name].append(evt)

        rollups: Dict[str, GenerationalRollup] = {}
        for gen_code, evts in buckets.items():
            n = len(evts)
            total_value = sum(e.value for e in evts)
            delivered = sum(1 for e in evts if e.is_completed())

            payment_counter = Counter(e.payment_method for e in evts if e.payment_method)
            traffic_counter = Counter(e.traffic_source for e in evts if e.traffic_source)
            device_counter = Counter(e.device_type for e in evts if e.device_type)
            city_counter = Counter(e.city for e in evts if e.city)

            def _normalize(c: Counter[str]) -> Dict[str, float]:
                total = sum(c.values()) or 1
                return {k: round(v / total, 3) for k, v in c.items()}

            rollups[gen_code] = GenerationalRollup(
                generation_code=gen_code,
                total_purchases=n,
                total_value=round(total_value, 2),
                delivery_rate=round(delivered / n, 3) if n else 0.0,
                payment_distribution=_normalize(payment_counter),
                traffic_distribution=_normalize(traffic_counter),
                device_distribution=_normalize(device_counter),
                top_cities=city_counter.most_common(5),
                repeat_rate=round(
                    sum(1 for e in evts if e.is_repeat_customer) / n, 3
                ) if n else 0.0,
                avg_order_value=round(total_value / n, 2) if n else 0.0,
            )
        self._rollups = rollups
        return rollups

    # ─────────────────────────────────────────────────────────────────────────
    # PHASE 3 · ANOMALY DETECTION
    # ─────────────────────────────────────────────────────────────────────────

    def detect_anomalies(self) -> List[Dict[str, Any]]:
        """
        يرصد تحوّلات > anomaly_threshold بين الواقع الفعلي والـ baseline في
        GENERATIONAL_NORMS — هذه الإشارة الأقوى لوجود حدث مؤسِّس جديد.
        """
        anomalies = []
        for gen_code, rollup in self._rollups.items():
            if not rollup.has_significant_sample(self.min_sample_per_generation):
                continue
            baseline = GENERATIONAL_NORMS.get(gen_code, {})
            baseline_payment = baseline.get("payment", {})

            for method, actual_share in rollup.payment_distribution.items():
                baseline_share = baseline_payment.get(method, 0.0)
                if baseline_share == 0 and actual_share >= 0.20:
                    # طريقة دفع ظهرت من الصفر بنسبة كبيرة
                    anomalies.append({
                        "type": "payment_method_emergence",
                        "generation": gen_code,
                        "method": method,
                        "baseline_share": baseline_share,
                        "actual_share": actual_share,
                        "shift_pct": "∞ (emerged from 0)",
                        "severity": "HIGH",
                    })
                elif baseline_share > 0:
                    shift = abs(actual_share - baseline_share) / baseline_share
                    if shift >= self.anomaly_threshold:
                        anomalies.append({
                            "type": "payment_method_shift",
                            "generation": gen_code,
                            "method": method,
                            "baseline_share": baseline_share,
                            "actual_share": actual_share,
                            "shift_pct": round(shift * 100, 1),
                            "direction": "UP" if actual_share > baseline_share else "DOWN",
                            "severity": "HIGH" if shift >= 1.0 else "MEDIUM",
                        })
        self._anomalies = anomalies
        return anomalies

    # ─────────────────────────────────────────────────────────────────────────
    # PHASE 4 · UPDATE NORMS
    # ─────────────────────────────────────────────────────────────────────────

    def update_generational_norms(self, force: bool = False) -> Dict[str, Any]:
        """
        🔄 يحدث GENERATIONAL_NORMS تلقائياً من الواقع الفعلي.

        قواعد الأمان:
          - فقط الأجيال بعينة كافية (≥30)
          - فقط لو الفرق عن baseline ≥ 20% (تجنّب الضوضاء)
          - force=True يتجاوز قاعدة 20% (لاختبارات يدوية فقط)
        """
        updated: List[str] = []
        skipped: List[str] = []

        for gen_code, rollup in self._rollups.items():
            if not rollup.has_significant_sample(self.min_sample_per_generation):
                skipped.append(f"{gen_code}: عينة {rollup.total_purchases} < {self.min_sample_per_generation}")
                continue

            baseline = GENERATIONAL_NORMS.get(gen_code, {}).get("payment", {})
            new_payment = rollup.payment_distribution

            # احسب الانحراف الكلي
            all_keys = set(baseline.keys()) | set(new_payment.keys())
            total_drift = sum(
                abs(new_payment.get(k, 0) - baseline.get(k, 0)) for k in all_keys
            )

            if total_drift < 0.20 and not force:
                skipped.append(f"{gen_code}: انحراف {total_drift:.2f} < 0.20 (ضوضاء)")
                continue

            # حدث القيم
            success = GenerationalIntelligenceEngine.update_norms_from_research(
                generation_code=gen_code,
                updated_norms={"payment": new_payment}
            )
            if success:
                updated.append(gen_code)
                self._norms_updated.append(
                    f"{gen_code} @ {datetime.now().isoformat()} | drift={total_drift:.2f}"
                )

        return {
            "updated": updated,
            "skipped": skipped,
            "timestamp": datetime.now().isoformat(),
        }

    # ─────────────────────────────────────────────────────────────────────────
    # PHASE 5 · PROPOSE FORMATIVE EVENTS
    # ─────────────────────────────────────────────────────────────────────────

    def propose_new_formative_events(
        self,
        event_id: str,
        year: int,
        description: str,
        economic_imprint: str = "unknown",
        intensity: float = 0.70,
        min_affected_generations: int = 2,
    ) -> Dict[str, Any]:
        """
        🆕 يقترح ويسجّل حدثاً مؤسِّساً جديداً إذا رصدنا anomalies في ≥2 أجيال.

        الاستخدام النموذجي:
          - بعد تعويم جديد للجنيه: rollup يكشف تحول BNPL/cash في Yanayer + TikTok
          - بعد تريند فيرال: rollup يكشف ظهور payment method جديد
          - بعد قانون جديد: rollup يكشف تغيير traffic source
        """
        # تجميع الأجيال المتأثرة من anomalies
        affected_gens = list({a["generation"] for a in self._anomalies})

        if len(affected_gens) < min_affected_generations:
            return {
                "registered": False,
                "reason": (f"عدد الأجيال المتأثرة ({len(affected_gens)}) "
                           f"< الحد الأدنى ({min_affected_generations})"),
                "affected_gens": affected_gens,
            }

        success = GenerationalIntelligenceEngine.register_new_formative_event(
            event_id=event_id,
            year=year,
            intensity=intensity,
            affected_generations=affected_gens,
            economic_imprint=economic_imprint,
            description=description,
        )

        if success:
            self._events_registered.append(event_id)
            return {
                "registered": True,
                "event_id": event_id,
                "affected_generations": affected_gens,
                "evidence_anomalies": len(self._anomalies),
            }
        return {
            "registered": False,
            "reason": f"event_id={event_id} موجود مسبقاً في EGYPTIAN_FORMATIVE_EVENTS",
        }

    # ─────────────────────────────────────────────────────────────────────────
    # PHASE 6 · REPORT
    # ─────────────────────────────────────────────────────────────────────────

    def generate_feedback_report(self) -> str:
        """تقرير Markdown تنفيذي عن دورة التغذية العكسية."""
        lines = [
            "# 🌉 تقرير Pixel Feedback Bridge → Layer 8",
            "",
            f"> **التوقيت:** {datetime.now().strftime('%Y-%m-%d %H:%M')} (القاهرة)",
            f"> **الأحداث المعالجة:** {len(self._events)} (مُسلَّم فقط)",
            f"> **الأجيال المرصودة:** {len(self._rollups)}",
            "",
            "---",
            "",
            "## 📊 تجميع الأجيال (Generational Rollups)",
            "",
        ]

        for gen_code, r in self._rollups.items():
            significant = "✅ كافية" if r.has_significant_sample(self.min_sample_per_generation) else "⚠️ غير كافية"
            lines.extend([
                f"### {gen_code}",
                f"- **عدد الطلبات:** {r.total_purchases} ({significant})",
                f"- **القيمة الإجمالية:** {r.total_value} EGP",
                f"- **متوسط قيمة الطلب (AOV):** {r.avg_order_value} EGP",
                f"- **نسبة التسليم:** {r.delivery_rate * 100:.1f}%",
                f"- **نسبة العودة (Repeat Rate):** {r.repeat_rate * 100:.1f}%",
                f"- **توزيع الدفع:** {r.payment_distribution}",
                f"- **توزيع المصدر:** {r.traffic_distribution}",
                f"- **أعلى المدن:** {r.top_cities}",
                "",
            ])

        lines.extend([
            "---",
            "",
            "## 🚨 الانحرافات المرصودة (Anomalies)",
            "",
        ])
        if not self._anomalies:
            lines.append("لا توجد انحرافات حادة عن baseline.")
        else:
            for a in self._anomalies:
                lines.append(
                    f"- **{a['severity']}** | {a['generation']} | {a['type']} | "
                    f"`{a['method']}`: baseline={a['baseline_share']:.2f} → "
                    f"actual={a['actual_share']:.2f} (Δ={a.get('shift_pct', '∞')})"
                )

        lines.extend([
            "",
            "---",
            "",
            "## 🔄 تحديثات Layer 8",
            "",
            f"- **GENERATIONAL_NORMS تم تحديثها:** {self._norms_updated or 'لم يحدث'}",
            f"- **EGYPTIAN_FORMATIVE_EVENTS مسجّلة جديداً:** {self._events_registered or 'لم يحدث'}",
            "",
            get_watermark(),
        ])

        return "\n".join(lines)

    def save_state(self, path: str) -> None:
        """يحفظ snapshot من الجسر لـ JSON (للديباج والتتبع)."""
        state = {
            "timestamp": datetime.now().isoformat(),
            "events_count": len(self._events),
            "rollups": {
                k: {
                    "total_purchases": v.total_purchases,
                    "total_value": v.total_value,
                    "payment_distribution": v.payment_distribution,
                    "traffic_distribution": v.traffic_distribution,
                    "delivery_rate": v.delivery_rate,
                    "avg_order_value": v.avg_order_value,
                } for k, v in self._rollups.items()
            },
            "anomalies": self._anomalies,
            "norms_updated": self._norms_updated,
            "events_registered": self._events_registered,
        }
        Path(path).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


# ═══════════════════════════════════════════════════════════════════════════════
# 4) DEMO — محاكاة حلقة كاملة على Karseell
# ═══════════════════════════════════════════════════════════════════════════════

def simulate_karseell_pixel_feedback() -> Dict[str, Any]:
    """
    🧪 محاكاة دفعة 60 طلب Karseell على مدار 30 يوم —
    عيّنة واقعية تظهر تحوّلاً سلوكياً قابلاً للرصد.
    """
    import random
    random.seed(42)  # نتائج قابلة للتكرار

    events: List[PixelPurchaseEvent] = []
    now = datetime.now()

    # 35 طلب من Gen Yanayer (Millennials) — البصمة الأساسية
    for i in range(35):
        events.append(PixelPurchaseEvent(
            event_time=now - timedelta(days=random.randint(0, 30)),
            order_id=f"ORD-Y{i:03d}",
            value=random.choice([1090, 1690]),
            age_bucket="25-34",
            city=random.choice(["القاهرة", "الجيزة", "الإسكندرية", "المنصورة"]),
            governorate="القاهرة الكبرى",
            # تحول واضح نحو BNPL بسبب صدمة التضخم
            payment_method=random.choices(
                ["cash", "bnpl", "card", "wallet"],
                weights=[0.35, 0.40, 0.15, 0.10]  # baseline cash=0.40, bnpl=0.20
            )[0],
            device_type=random.choice(["mobile", "mobile", "mobile", "desktop"]),
            traffic_source=random.choice(["tiktok", "instagram", "facebook", "tiktok"]),
            delivery_status="delivered",
            delivered_at=now - timedelta(days=random.randint(0, 28)),
            is_repeat_customer=random.random() < 0.35,
        ))

    # 32 طلب من Gen TikTok (Gen Z) — انفجار BNPL
    for i in range(32):
        events.append(PixelPurchaseEvent(
            event_time=now - timedelta(days=random.randint(0, 30)),
            order_id=f"ORD-Z{i:03d}",
            value=random.choice([1090, 1690]),
            age_bucket="18-24",
            city=random.choice(["القاهرة", "الجيزة", "الإسكندرية", "أسيوط", "طنطا"]),
            governorate="القاهرة الكبرى",
            # baseline bnpl=0.40 — لكن دلوقتي بقى 0.65 (تحول حاد)
            payment_method=random.choices(
                ["bnpl", "cash", "wallet", "card"],
                weights=[0.65, 0.20, 0.10, 0.05]
            )[0],
            device_type="mobile",
            traffic_source=random.choices(
                ["tiktok", "instagram", "facebook"],
                weights=[0.70, 0.25, 0.05]
            )[0],
            delivery_status=random.choices(
                ["delivered", "cancelled"], weights=[0.85, 0.15]
            )[0],
            delivered_at=now - timedelta(days=random.randint(0, 28)),
            is_repeat_customer=random.random() < 0.20,
        ))

    # 8 طلبات ملغية (الجسر هيرفضها)
    for i in range(8):
        events.append(PixelPurchaseEvent(
            event_time=now - timedelta(days=random.randint(0, 30)),
            order_id=f"ORD-X{i:03d}",
            value=1090,
            age_bucket="25-34",
            payment_method="cash",
            delivery_status="cancelled",
        ))

    # ─────── تشغيل الجسر ───────
    bridge = PixelFeedbackBridge(min_sample_per_generation=30, anomaly_threshold=0.40)
    ingest_report = bridge.ingest_events(events)
    rollups = bridge.rollup_by_generation()
    anomalies = bridge.detect_anomalies()
    norms_update = bridge.update_generational_norms()

    formative_proposal = bridge.propose_new_formative_events(
        event_id="BNPL_SURGE_2026",
        year=2026,
        description="انفجار استخدام BNPL في مصر بعد دخول valU/Sympl/Tabby للسوق",
        economic_imprint="bnpl_normalization",
        intensity=0.75,
        min_affected_generations=1,
    )

    report_md = bridge.generate_feedback_report()
    report_path = Path(__file__).parent / "pixel_feedback_report.md"
    report_path.write_text(report_md, encoding="utf-8")

    state_path = Path(__file__).parent / "pixel_feedback_state.json"
    bridge.save_state(str(state_path))

    return {
        "ingest_report": ingest_report,
        "rollups_count": len(rollups),
        "anomalies": anomalies,
        "norms_update": norms_update,
        "formative_proposal": formative_proposal,
        "report_path": str(report_path),
        "state_path": str(state_path),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 5) MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 75)
    print("🌉 Pixel Feedback Bridge — محاكاة حلقة كاملة على Karseell")
    print("=" * 75)

    result = simulate_karseell_pixel_feedback()

    print("\n📥 INGEST:")
    for k, v in result["ingest_report"].items():
        print(f"   {k}: {v}")

    print(f"\n📊 ROLLUPS: {result['rollups_count']} أجيال مرصودة")

    print(f"\n🚨 ANOMALIES: {len(result['anomalies'])} انحراف")
    for a in result["anomalies"][:5]:
        print(f"   - {a['severity']} | {a['generation']} | {a['method']}: "
              f"{a['baseline_share']:.2f} → {a['actual_share']:.2f}")

    print("\n🔄 NORMS UPDATE:")
    print(f"   updated: {result['norms_update']['updated']}")
    print(f"   skipped: {result['norms_update']['skipped']}")

    print("\n🆕 FORMATIVE EVENT PROPOSAL:")
    for k, v in result["formative_proposal"].items():
        print(f"   {k}: {v}")

    print(f"\n📄 تقرير: {result['report_path']}")
    print(f"📊 State: {result['state_path']}")
    print(f"\n{get_watermark()}")
