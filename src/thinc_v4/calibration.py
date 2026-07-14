# -*- coding: utf-8 -*-
"""THINC v4.1 — Predictive Accuracy Report & Bayesian Weight Calibration (Phase 2).

يطبق على النموذج نفسه ما يوصي به للطلاب:
- قياس الدقة التنبؤية أولًا (Reality Validation للنموذج).
- تحديث الأوزان بايزيًا: Prior = خبرة المؤسس، Likelihood = نتائج ميدانية.
- حد أمان: لا يتغير أي وزن أكثر من ±20% في دورة المعايرة الواحدة.

CLI:
    python -m thinc_v4.calibration --report --data-dir data/
    python -m thinc_v4.calibration --calibrate --data-dir data/ --min-outcomes 25

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 Dr. Ehab Taha — Egy-Pioneers Academy. All rights reserved.
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .outcomes import OutcomeRegistry

WEIGHTS_PATH = Path(__file__).resolve().parent / "weights.json"
MAX_WEIGHT_SHIFT = 0.20  # ±20% حد أمان لكل دورة
MIN_OUTCOMES_FOR_CALIBRATION = 25
SUCCESS_SCORE_THRESHOLD = 7.0  # درجة THINC التي تُعتبر توقعًا بالنجاح

COMPONENT_COLUMNS = {
    "v3_behavioral_commerce_core": "component_v3_core",
    "founder_os": "component_founder_os",
    "business_architecture": "component_business_architecture",
    "category_design": "component_category_design",
    "competitive_differentiation": "component_competitive_differentiation",
    "academy_operating_system": "component_academy_os",
}


def load_weights(path: Path = WEIGHTS_PATH) -> Dict[str, Any]:
    with path.open(encoding="utf-8") as fh:
        payload: Dict[str, Any] = json.load(fh)
    total = sum(payload["weights"].values())
    if abs(total - 1.0) > 1e-6:
        raise ValueError(f"Weights must sum to 1.0, got {total}")
    return payload


def save_weights(payload: Dict[str, Any], path: Path = WEIGHTS_PATH) -> None:
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


@dataclass
class AccuracyReport:
    n_pairs: int
    accuracy: float
    precision: float
    recall: float
    auc: float
    calibration_bins: List[Dict[str, Any]]
    component_correlations: Dict[str, float]
    weights_version: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "n_pairs": self.n_pairs,
            "accuracy": self.accuracy,
            "precision": self.precision,
            "recall": self.recall,
            "auc": self.auc,
            "calibration_bins": self.calibration_bins,
            "component_correlations": self.component_correlations,
            "weights_version": self.weights_version,
            "success_score_threshold": SUCCESS_SCORE_THRESHOLD,
        }


def _pairs_to_xy(pairs: List[Dict[str, Any]]) -> Tuple[List[float], List[bool], List[Dict[str, float]]]:
    scores: List[float] = []
    successes: List[bool] = []
    components: List[Dict[str, float]] = []
    for pair in pairs:
        pred, out = pair["prediction"], pair["outcome"]
        scores.append(float(pred["final_score"]))
        successes.append(str(out["success"]).strip().lower() == "true")
        comp: Dict[str, float] = {}
        for name, column in COMPONENT_COLUMNS.items():
            raw = pred.get(column, "")
            comp[name] = float(raw) if raw not in ("", None) else 0.0
        components.append(comp)
    return scores, successes, components


def _auc(scores: List[float], successes: List[bool]) -> float:
    """Mann-Whitney AUC بدون اعتماد على مكتبات خارجية."""
    pos = [s for s, y in zip(scores, successes, strict=False) if y]
    neg = [s for s, y in zip(scores, successes, strict=False) if not y]
    if not pos or not neg:
        return float("nan")
    wins = 0.0
    for p in pos:
        for n in neg:
            if p > n:
                wins += 1.0
            elif p == n:
                wins += 0.5
    return round(wins / (len(pos) * len(neg)), 3)


def _pearson(xs: List[float], ys: List[float]) -> float:
    n = len(xs)
    if n < 3:
        return float("nan")
    mx, my = sum(xs) / n, sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=False))
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx == 0 or vy == 0:
        return float("nan")
    return round(float(cov) / (math.sqrt(float(vx)) * math.sqrt(float(vy))), 3)


def accuracy_report(registry: OutcomeRegistry) -> AccuracyReport:
    """تقرير الدقة التنبؤية — يُنفَّذ قبل أي معايرة (Baseline أولًا)."""
    pairs = registry.paired()
    scores, successes, components = _pairs_to_xy(pairs)
    n = len(pairs)

    tp = sum(1 for s, y in zip(scores, successes, strict=False) if s >= SUCCESS_SCORE_THRESHOLD and y)
    fp = sum(1 for s, y in zip(scores, successes, strict=False) if s >= SUCCESS_SCORE_THRESHOLD and not y)
    fn = sum(1 for s, y in zip(scores, successes, strict=False) if s < SUCCESS_SCORE_THRESHOLD and y)
    tn = n - tp - fp - fn

    accuracy = round((tp + tn) / n, 3) if n else float("nan")
    precision = round(tp / (tp + fp), 3) if (tp + fp) else float("nan")
    recall = round(tp / (tp + fn), 3) if (tp + fn) else float("nan")

    bins: List[Dict[str, Any]] = []
    for lo, hi in [(0, 4), (4, 5.5), (5.5, 7), (7, 8.5), (8.5, 10.01)]:
        members = [(s, y) for s, y in zip(scores, successes, strict=False) if lo <= s < hi]
        if members:
            bins.append({
                "score_range": f"{lo}–{min(hi, 10)}",
                "n": len(members),
                "success_rate": round(sum(1 for _, y in members if y) / len(members), 3),
            })

    correlations: Dict[str, float] = {}
    ys = [1.0 if y else 0.0 for y in successes]
    for name in COMPONENT_COLUMNS:
        xs = [c[name] for c in components]
        correlations[name] = _pearson(xs, ys)

    return AccuracyReport(
        n_pairs=n,
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        auc=_auc(scores, successes),
        calibration_bins=bins,
        component_correlations=correlations,
        weights_version=load_weights()["version"],
    )


def bayesian_calibrate(
    registry: OutcomeRegistry,
    min_outcomes: int = MIN_OUTCOMES_FOR_CALIBRATION,
    weights_path: Path = WEIGHTS_PATH,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """دورة معايرة واحدة.

    الفكرة: قوة ارتباط كل مكوّن بالنجاح الفعلي (Pearson موجب) تُستخدم كإشارة
    Likelihood، وتُدمج مع الـ Prior (الأوزان الحالية) بوزن يتناسب مع حجم العينة،
    ثم يُطبَّق حد الأمان ±20% ويعاد التطبيع ليبقى المجموع 1.0.
    """
    payload = load_weights(weights_path)
    prior: Dict[str, float] = payload["weights"]
    pairs = registry.paired()
    n = len(pairs)
    if n < min_outcomes:
        return {
            "status": "skipped",
            "reason": f"عدد النتائج المكتملة {n} أقل من الحد الأدنى {min_outcomes}.",
            "weights_version": payload["version"],
        }

    report = accuracy_report(registry)
    corr = report.component_correlations

    # إشارة likelihood: الارتباطات السالبة أو غير المحسوبة لا ترفع الوزن
    signal = {k: max(0.0, v if v == v else 0.0) for k, v in corr.items()}  # NaN → 0
    signal_total = sum(signal.values())
    if signal_total == 0:
        return {
            "status": "skipped",
            "reason": "لا توجد إشارة ارتباط موجبة كافية للمعايرة.",
            "weights_version": payload["version"],
        }
    likelihood = {k: v / signal_total for k, v in signal.items()}

    # قوة البيانات تزيد مع حجم العينة وتُشبع عند 200 نتيجة
    data_strength = min(0.5, n / 200)

    blended = {
        k: (1 - data_strength) * prior[k] + data_strength * likelihood[k]
        for k in prior
    }
    # حد الأمان ±20% لكل وزن ثم إعادة تطبيع
    capped = {
        k: min(prior[k] * (1 + MAX_WEIGHT_SHIFT), max(prior[k] * (1 - MAX_WEIGHT_SHIFT), v))
        for k, v in blended.items()
    }
    total = sum(capped.values())
    posterior = {k: round(v / total, 4) for k, v in capped.items()}
    # امتصاص فرق التقريب في أكبر وزن حتى يبقى المجموع 1.0 بالضبط
    largest = max(posterior, key=lambda k: posterior[k])
    posterior[largest] = round(posterior[largest] + (1.0 - sum(posterior.values())), 4)

    old_version = payload["version"]
    cycle = int(old_version.split("-c")[-1]) + 1 if "-c" in old_version else 1
    new_payload = {
        "version": f"v4.1.0-c{cycle}",
        "calibrated_on_n_outcomes": n,
        "calibrated_at": datetime.now(timezone.utc).isoformat(),
        "note": payload.get("note", ""),
        "previous_version": old_version,
        "previous_weights": prior,
        "weights": posterior,
    }
    if not dry_run:
        save_weights(new_payload, weights_path)
    return {
        "status": "calibrated" if not dry_run else "dry_run",
        "n_outcomes": n,
        "data_strength": round(data_strength, 3),
        "old_weights": prior,
        "new_weights": posterior,
        "old_version": old_version,
        "new_version": new_payload["version"],
        "accuracy_before": report.to_dict(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="THINC v4.1 calibration engine")
    parser.add_argument("--data-dir", default="data", help="Directory holding the outcome registry CSVs")
    parser.add_argument("--report", action="store_true", help="Print predictive accuracy report")
    parser.add_argument("--calibrate", action="store_true", help="Run one Bayesian calibration cycle")
    parser.add_argument("--dry-run", action="store_true", help="Calibrate without saving weights")
    parser.add_argument("--min-outcomes", type=int, default=MIN_OUTCOMES_FOR_CALIBRATION)
    args = parser.parse_args()

    registry = OutcomeRegistry(args.data_dir)
    if args.report:
        print(json.dumps(accuracy_report(registry).to_dict(), ensure_ascii=False, indent=2))
    if args.calibrate:
        result = bayesian_calibrate(registry, min_outcomes=args.min_outcomes, dry_run=args.dry_run)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    if not args.report and not args.calibrate:
        print(json.dumps(registry.coverage_report(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
