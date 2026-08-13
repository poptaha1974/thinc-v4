# -*- coding: utf-8 -*-
"""THINC v4.1 — Outcome Tracking Registry (Phase 1 of the calibration plan).

سجل تتبع النتائج: العمود الفقري لتحويل THINC من إطار خبرة إلى نموذج مُعايَر.

- Prediction Log: يُكتب لحظة تقييم المشروع ولا يُعدَّل أبدًا (append-only).
- Outcome Log: يُكتب بعد 30/60/90 يومًا من الإطلاق ويُربط بالتوقع عبر prediction_id.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 Dr. Ehab Taha — Egy-Pioneers Academy. All rights reserved.
"""
from __future__ import annotations

import csv
import hashlib
import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

PREDICTIONS_FILENAME = "thinc_predictions.csv"
OUTCOMES_FILENAME = "thinc_outcomes.csv"

PREDICTION_FIELDS = [
    "prediction_id",
    "student_ref",
    "cohort_id",
    "assessed_at",
    "model_version",
    "weights_version",
    "final_score",
    "grade",
    "component_v3_core",
    "component_founder_os",
    "component_business_architecture",
    "component_category_design",
    "component_competitive_differentiation",
    "component_academy_os",
    "target_generation",
    "skill_level",
    "assessor_id",
]

OUTCOME_FIELDS = [
    "prediction_id",
    "measured_at",
    "window_days",
    "orders_delivered",
    "orders_returned",
    "revenue_egp",
    "ad_spend_egp",
    "unit_economics_positive",
    "first_sale_achieved",
    "student_still_active",
    "kill_fix_scale_decision",
    "success",
    "notes",
]

# تعريف النجاح الرسمي (المرحلة 0 من الخطة): قابل للتعديل من مكان واحد فقط،
# ويجب ألا يتغير أثناء نافذة قياس جارية.
SUCCESS_MIN_DELIVERED_ORDERS = 10
SUCCESS_WINDOW_DAYS = 60


def anonymize_student(raw_identifier: str) -> str:
    """تجهيل هوية الطالب: يُخزَّن هاش قصير بدلًا من أي معرف شخصي."""
    digest = hashlib.sha256(raw_identifier.strip().lower().encode("utf-8")).hexdigest()
    return f"st_{digest[:12]}"


@dataclass(frozen=True)
class PredictionRecord:
    """توقع THINC لحظة التقييم — لا يُعدَّل بعد الكتابة."""

    student_ref: str
    cohort_id: str
    final_score: float
    grade: str
    components: Dict[str, float]
    target_generation: str
    skill_level: str
    model_version: str
    weights_version: str
    assessor_id: str = "unassigned"
    prediction_id: str = field(default_factory=lambda: f"pred_{uuid.uuid4().hex[:16]}")
    assessed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_row(self) -> Dict[str, Any]:
        return {
            "prediction_id": self.prediction_id,
            "student_ref": self.student_ref,
            "cohort_id": self.cohort_id,
            "assessed_at": self.assessed_at,
            "model_version": self.model_version,
            "weights_version": self.weights_version,
            "final_score": self.final_score,
            "grade": self.grade,
            "component_v3_core": self.components.get("v3_behavioral_commerce_core", ""),
            "component_founder_os": self.components.get("founder_os", ""),
            "component_business_architecture": self.components.get("business_architecture", ""),
            "component_category_design": self.components.get("category_design", ""),
            "component_competitive_differentiation": self.components.get("competitive_differentiation", ""),
            "component_academy_os": self.components.get("academy_operating_system", ""),
            "target_generation": self.target_generation,
            "skill_level": self.skill_level,
            "assessor_id": self.assessor_id,
        }


@dataclass(frozen=True)
class OutcomeRecord:
    """النتيجة الفعلية بعد نافذة القياس — تُربط بالتوقع عبر prediction_id."""

    prediction_id: str
    window_days: int
    orders_delivered: int
    orders_returned: int
    revenue_egp: float
    ad_spend_egp: float
    unit_economics_positive: bool
    first_sale_achieved: bool
    student_still_active: bool
    kill_fix_scale_decision: str = ""
    notes: str = ""
    measured_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self) -> None:
        if self.orders_delivered < 0 or self.orders_returned < 0:
            raise ValueError("Order counts must be >= 0")
        if self.revenue_egp < 0 or self.ad_spend_egp < 0:
            raise ValueError("Money amounts must be >= 0")
        if self.window_days not in (30, 60, 90):
            raise ValueError("window_days must be one of 30, 60, 90")

    @property
    def success(self) -> bool:
        """التعريف الكمي الرسمي للنجاح (لا يتغير أثناء القياس)."""
        return (
            self.orders_delivered >= SUCCESS_MIN_DELIVERED_ORDERS
            and self.unit_economics_positive
        )

    def to_row(self) -> Dict[str, Any]:
        row = asdict(self)
        row["success"] = self.success
        return {key: row[key] for key in OUTCOME_FIELDS}


class OutcomeRegistry:
    """تخزين CSV بسيط وقابل للمراجعة اليدوية (يمكن الترقية لاحقًا إلى SQLite)."""

    def __init__(self, data_dir: str | Path):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.predictions_path = self.data_dir / PREDICTIONS_FILENAME
        self.outcomes_path = self.data_dir / OUTCOMES_FILENAME

    # -- helpers ---------------------------------------------------------
    @staticmethod
    def _append(path: Path, fieldnames: List[str], row: Dict[str, Any]) -> None:
        exists = path.exists()
        with path.open("a", newline="", encoding="utf-8-sig") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            if not exists:
                writer.writeheader()
            writer.writerow(row)

    @staticmethod
    def _read(path: Path) -> List[Dict[str, str]]:
        if not path.exists():
            return []
        with path.open(encoding="utf-8-sig", newline="") as fh:
            return list(csv.DictReader(fh))

    # -- predictions -----------------------------------------------------
    def log_prediction(self, record: PredictionRecord) -> str:
        self._append(self.predictions_path, PREDICTION_FIELDS, record.to_row())
        return record.prediction_id

    def predictions(self) -> List[Dict[str, str]]:
        return self._read(self.predictions_path)

    # -- outcomes --------------------------------------------------------
    def log_outcome(self, record: OutcomeRecord) -> None:
        known = {p["prediction_id"] for p in self.predictions()}
        if record.prediction_id not in known:
            raise ValueError(
                f"Unknown prediction_id {record.prediction_id!r} — "
                "كل نتيجة لازم تترتبط بتوقع مسجل."
            )
        self._append(self.outcomes_path, OUTCOME_FIELDS, record.to_row())

    def outcomes(self) -> List[Dict[str, str]]:
        return self._read(self.outcomes_path)

    # -- pairing & coverage ----------------------------------------------
    def paired(self, window_days: int | None = None) -> List[Dict[str, Any]]:
        """أزواج (توقع، نتيجة) — المادة الخام لتقرير الدقة والمعايرة."""
        outcome_map: Dict[str, Dict[str, str]] = {}
        for o in self.outcomes():
            if window_days is not None and int(o["window_days"]) != window_days:
                continue
            outcome_map[o["prediction_id"]] = o
        pairs: List[Dict[str, Any]] = []
        for p in self.predictions():
            matched = outcome_map.get(p["prediction_id"])
            if matched is not None:
                pairs.append({"prediction": p, "outcome": matched})
        return pairs

    def coverage_report(self, max_pending_days: int = 90) -> Dict[str, Any]:
        """تقرير التغطية: KPI المرحلة 1 (الهدف ≥ 90%)."""
        preds = self.predictions()
        outcome_ids = {o["prediction_id"] for o in self.outcomes()}
        now = datetime.now(timezone.utc)
        overdue: List[str] = []
        for p in preds:
            if p["prediction_id"] in outcome_ids:
                continue
            assessed = datetime.fromisoformat(p["assessed_at"])
            if (now - assessed).days > max_pending_days:
                overdue.append(p["prediction_id"])
        total = len(preds)
        covered = len([p for p in preds if p["prediction_id"] in outcome_ids])
        return {
            "total_predictions": total,
            "with_outcome": covered,
            "coverage_pct": round(covered / total * 100, 1) if total else 0.0,
            "overdue_prediction_ids": overdue,
        }

    def export_summary(self) -> str:
        report = self.coverage_report()
        return json.dumps(report, ensure_ascii=False, indent=2)
