# -*- coding: utf-8 -*-
"""Tests for THINC v4.1 — outcomes registry, Bayesian calibration, retention engine.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from thinc_v4.calibration import accuracy_report, bayesian_calibrate, load_weights
from thinc_v4.framework import (
    CompetitiveIntelligence,
    DifferentiationAsset,
    THINCV4Engine,
    THINCV4ProjectInput,
    load_component_weights,
)
from thinc_v4.outcomes import (
    OutcomeRecord,
    OutcomeRegistry,
    PredictionRecord,
    anonymize_student,
)
from thinc_v4.retention import RepeatPurchaseSnapshot, RetentionEngine


def _make_prediction(score: float, cohort: str = "cohort_1") -> PredictionRecord:
    return PredictionRecord(
        student_ref=anonymize_student(f"student-{score}"),
        cohort_id=cohort,
        final_score=score,
        grade="B",
        components={
            "v3_behavioral_commerce_core": score,
            "founder_os": score,
            "business_architecture": score,
            "category_design": score,
            "competitive_differentiation": score,
            "academy_operating_system": score,
        },
        target_generation="Mixed Egyptian Audience",
        skill_level="مبتدئ",
        model_version="THINC v4.0",
        weights_version="test",
    )


def _make_outcome(prediction_id: str, delivered: int, positive_ue: bool, active: bool = True) -> OutcomeRecord:
    return OutcomeRecord(
        prediction_id=prediction_id,
        window_days=60,
        orders_delivered=delivered,
        orders_returned=0,
        revenue_egp=delivered * 500,
        ad_spend_egp=1000,
        unit_economics_positive=positive_ue,
        first_sale_achieved=delivered > 0,
        student_still_active=active,
    )


# ---------------------------------------------------------------- outcomes --

def test_anonymize_student_is_stable_and_opaque() -> None:
    a = anonymize_student("Ahmed Ali 01012345678")
    b = anonymize_student("ahmed ali 01012345678")
    assert a == b
    assert a.startswith("st_")
    assert "Ahmed" not in a


def test_prediction_and_outcome_roundtrip(tmp_path: Path) -> None:
    registry = OutcomeRegistry(tmp_path)
    pred = _make_prediction(8.0)
    pid = registry.log_prediction(pred)
    registry.log_outcome(_make_outcome(pid, delivered=15, positive_ue=True))
    pairs = registry.paired()
    assert len(pairs) == 1
    assert pairs[0]["outcome"]["success"] == "True"


def test_outcome_rejects_unknown_prediction(tmp_path: Path) -> None:
    registry = OutcomeRegistry(tmp_path)
    with pytest.raises(ValueError):
        registry.log_outcome(_make_outcome("pred_nonexistent", 5, True))


def test_outcome_validates_inputs(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        OutcomeRecord(
            prediction_id="x", window_days=45, orders_delivered=1, orders_returned=0,
            revenue_egp=0, ad_spend_egp=0, unit_economics_positive=True,
            first_sale_achieved=True, student_still_active=True,
        )


def test_coverage_report(tmp_path: Path) -> None:
    registry = OutcomeRegistry(tmp_path)
    p1 = registry.log_prediction(_make_prediction(7.0))
    registry.log_prediction(_make_prediction(6.0))
    registry.log_outcome(_make_outcome(p1, 12, True))
    report = registry.coverage_report()
    assert report["total_predictions"] == 2
    assert report["with_outcome"] == 1
    assert report["coverage_pct"] == 50.0


def test_assess_logs_prediction_when_registry_given(tmp_path: Path) -> None:
    registry = OutcomeRegistry(tmp_path)
    report = THINCV4Engine.assess(
        THINCV4ProjectInput(project_name="اختبار تسجيل"),
        outcome_registry=registry,
        cohort_id="cohort_test",
    )
    assert report.prediction_id
    assert registry.predictions()[0]["cohort_id"] == "cohort_test"
    assert registry.predictions()[0]["prediction_id"] == report.prediction_id


# ------------------------------------------------------------- calibration --

def _seed_registry(tmp_path: Path, n_good: int = 15, n_bad: int = 15) -> OutcomeRegistry:
    registry = OutcomeRegistry(tmp_path)
    for i in range(n_good):
        pid = registry.log_prediction(_make_prediction(8.0 + (i % 3) * 0.3))
        registry.log_outcome(_make_outcome(pid, delivered=12 + i, positive_ue=True))
    for i in range(n_bad):
        pid = registry.log_prediction(_make_prediction(4.0 + (i % 3) * 0.3))
        registry.log_outcome(_make_outcome(pid, delivered=2, positive_ue=False, active=False))
    return registry


def test_accuracy_report_on_separable_data(tmp_path: Path) -> None:
    registry = _seed_registry(tmp_path)
    report = accuracy_report(registry)
    assert report.n_pairs == 30
    assert report.accuracy == 1.0
    assert report.auc == 1.0
    assert len(report.calibration_bins) >= 2


def test_calibration_respects_minimum_sample(tmp_path: Path) -> None:
    registry = _seed_registry(tmp_path, n_good=3, n_bad=3)
    result = bayesian_calibrate(registry, min_outcomes=25, dry_run=True)
    assert result["status"] == "skipped"


def test_calibration_caps_weight_shift(tmp_path: Path) -> None:
    registry = _seed_registry(tmp_path, n_good=20, n_bad=20)
    result = bayesian_calibrate(registry, min_outcomes=25, dry_run=True)
    assert result["status"] == "dry_run"
    old, new = result["old_weights"], result["new_weights"]
    assert abs(sum(new.values()) - 1.0) < 1e-6
    for key in old:
        # cap is ±20% before renormalization; allow small drift from renormalizing
        assert new[key] <= old[key] * 1.20 * 1.05
        assert new[key] >= old[key] * 0.80 * 0.95


def test_weights_file_loads_and_sums_to_one() -> None:
    payload = load_weights()
    assert abs(sum(payload["weights"].values()) - 1.0) < 1e-6
    weights, version = load_component_weights()
    assert version == payload["version"]
    assert set(weights) == set(payload["weights"])


# --------------------------------------------------------------- retention --

def test_student_retention_by_cohort(tmp_path: Path) -> None:
    registry = OutcomeRegistry(tmp_path)
    p1 = registry.log_prediction(_make_prediction(8.0, cohort="c1"))
    p2 = registry.log_prediction(_make_prediction(7.0, cohort="c1"))
    registry.log_outcome(_make_outcome(p1, 12, True, active=True))
    registry.log_outcome(_make_outcome(p2, 3, False, active=False))
    curves = RetentionEngine(registry).student_retention_by_cohort()
    assert curves["c1"]["day_60"]["n"] == 2
    assert curves["c1"]["day_60"]["active_rate"] == 0.5


def test_repeat_purchase_scale_gate() -> None:
    snapshots = [
        RepeatPurchaseSnapshot("p1", "month_1", unique_customers=40, returning_customers=8),
    ]
    summary = RetentionEngine.project_repeat_purchase(snapshots)
    assert summary["overall_repeat_rate"] == 0.2
    gate = RetentionEngine.scale_decision_gate(True, summary)
    assert gate["scale_allowed"] is True

    empty_gate = RetentionEngine.scale_decision_gate(True, RetentionEngine.project_repeat_purchase([]))
    assert empty_gate["scale_allowed"] is False

    non_repeatable = RetentionEngine.scale_decision_gate(False, {})
    assert non_repeatable["scale_allowed"] is True


def test_repeat_snapshot_validation() -> None:
    with pytest.raises(ValueError):
        RepeatPurchaseSnapshot("p1", "month_1", unique_customers=5, returning_customers=9)


# ------------------------------------------------- differentiation matrix --

def test_differentiation_asset_requires_evidence() -> None:
    with pytest.raises(ValueError):
        DifferentiationAsset("real_operations", "تشغيل فعلي", present=True, evidence="")


def test_structured_differentiation_overrides_keyword_heuristic() -> None:
    ci = CompetitiveIntelligence(
        market_gap="مدعوم تشغيل مكان فعلي نادي ai ذكاء أول عملية بيع",  # keyword-stuffed
        differentiation_assets=[
            DifferentiationAsset("real_operations", "تشغيل فعلي", present=True, evidence="عقود موردين"),
            DifferentiationAsset("physical_location", "مكان فعلي", present=False),
        ],
    )
    # keyword stuffing must NOT inflate the structured score (3 base + 1 proven = 4)
    assert ci.differentiation_score() == 4.0


# --- writable weights location (v4.2 packaging safety) -----------------------


def test_weights_path_resolution_order(tmp_path: Path, monkeypatch) -> None:
    from thinc_v4.calibration import (
        PACKAGED_WEIGHTS_PATH,
        WEIGHTS_PATH_ENV,
        resolve_weights_path,
    )

    monkeypatch.delenv(WEIGHTS_PATH_ENV, raising=False)
    assert resolve_weights_path() == PACKAGED_WEIGHTS_PATH

    external = tmp_path / "state" / "weights.json"
    monkeypatch.setenv(WEIGHTS_PATH_ENV, str(external))
    assert resolve_weights_path() == external

    explicit = tmp_path / "explicit.json"
    assert resolve_weights_path(explicit) == explicit


def test_save_weights_creates_the_override_directory(tmp_path: Path, monkeypatch) -> None:
    from thinc_v4.calibration import WEIGHTS_PATH_ENV, load_weights, save_weights

    target = tmp_path / "nested" / "dir" / "weights.json"
    monkeypatch.setenv(WEIGHTS_PATH_ENV, str(target))

    payload = load_weights()  # falls back to the packaged file until one is written
    save_weights(payload)

    assert target.exists()
    assert abs(sum(load_weights()["weights"].values()) - 1.0) < 1e-6


def test_save_weights_reports_a_read_only_target(tmp_path: Path, monkeypatch) -> None:
    import os

    if hasattr(os, "geteuid") and os.geteuid() == 0:
        pytest.skip("root ignores directory write permissions — cannot simulate a read-only target")

    from thinc_v4.calibration import WEIGHTS_PATH_ENV, load_weights, save_weights

    read_only = tmp_path / "locked"
    read_only.mkdir()
    payload = load_weights()
    read_only.chmod(0o500)
    monkeypatch.setenv(WEIGHTS_PATH_ENV, str(read_only / "weights.json"))
    try:
        with pytest.raises(RuntimeError, match=WEIGHTS_PATH_ENV):
            save_weights(payload)
    finally:
        read_only.chmod(0o700)
