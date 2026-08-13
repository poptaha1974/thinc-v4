# -*- coding: utf-8 -*-
"""Tests for the Adaptive Market Learning API.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
"""
from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

OPTIONS = "/api/adaptive-learning/options"
EVALUATE = "/api/adaptive-learning/evaluate"


@pytest.fixture
def drifted_payload(learning_api: TestClient) -> dict[str, Any]:
    """A prediction that was clearly too optimistic versus reality."""

    options = learning_api.get(OPTIONS).json()
    return {
        "context_name": "Karseell — August scale test",
        "prediction": {
            "expected_score": 8.0,
            "expected_real_cpa": 60.0,
            "expected_conversion_rate": 0.05,
            "expected_delivery_rate": 0.85,
            "expected_net_profit": 12000.0,
            "expected_objections": ["السعر مرتفع"],
        },
        "actual": {
            "actual_score": 5.0,
            "actual_real_cpa": 130.0,
            "actual_conversion_rate": 0.02,
            "actual_delivery_rate": 0.62,
            "actual_net_profit": -3000.0,
            "observed_objections": ["مش واثق في المنتج", "الشيبينج غالي"],
            "comments_sentiment": "mixed",
            "repeat_purchase_rate": 0.05,
            "refund_or_return_rate": 0.22,
        },
        "signals": [
            {
                "signal_type": options["signal_types"][0],
                "description": "منافس جديد نزل بسعر أقل",
                "evidence": "لقطات من Meta Ad Library",
                "severity": options["severities"][-1],
            }
        ],
        "current_weights": options["default_weights"],
    }


def test_options_expose_signal_types_and_default_weights(learning_api: TestClient) -> None:
    body = learning_api.get(OPTIONS).json()
    assert body["signal_types"]
    assert body["severities"]
    assert body["default_weights"]
    assert all(isinstance(value, float | int) for value in body["default_weights"].values())


def test_health_endpoint(learning_api: TestClient) -> None:
    body = learning_api.get("/health").json()
    assert body["status"] == "ok"


def test_evaluate_detects_drift_and_recommends_action(
    learning_api: TestClient, drifted_payload: dict[str, Any]
) -> None:
    response = learning_api.post(EVALUATE, json=drifted_payload)
    assert response.status_code == 200, response.text
    body = response.json()

    assert 0 <= body["learning_score"] <= 10
    assert body["severity"]
    assert body["action"]
    assert body["prediction_gap_summary"], "a 60→130 CPA miss must be reported"
    assert isinstance(body["rule_updates"], dict)
    assert isinstance(body["experiments_to_run"], list)
    assert isinstance(body["human_review_notes"], list)


def test_accurate_prediction_scores_better_than_a_drifted_one(
    learning_api: TestClient, drifted_payload: dict[str, Any]
) -> None:
    drifted = learning_api.post(EVALUATE, json=drifted_payload).json()["learning_score"]

    accurate = dict(drifted_payload)
    accurate["actual"] = dict(drifted_payload["actual"])
    accurate["actual"].update(
        {
            "actual_score": 7.9,
            "actual_real_cpa": 61.0,
            "actual_conversion_rate": 0.049,
            "actual_delivery_rate": 0.84,
            "actual_net_profit": 11500.0,
            "observed_objections": ["السعر مرتفع"],
            "refund_or_return_rate": 0.03,
        }
    )

    assert learning_api.post(EVALUATE, json=accurate).json()["learning_score"] != drifted


def test_evaluate_without_signals_still_works(
    learning_api: TestClient, drifted_payload: dict[str, Any]
) -> None:
    drifted_payload["signals"] = []
    assert learning_api.post(EVALUATE, json=drifted_payload).status_code == 200


def test_unknown_signal_type_is_a_client_error(
    learning_api: TestClient, drifted_payload: dict[str, Any]
) -> None:
    drifted_payload["signals"][0]["signal_type"] = "not_a_signal_type"

    response = learning_api.post(EVALUATE, json=drifted_payload)

    assert response.status_code == 422
    assert response.json()["error"] == "invalid_input"


def test_negative_cpa_is_rejected(learning_api: TestClient, drifted_payload: dict[str, Any]) -> None:
    drifted_payload["actual"]["actual_real_cpa"] = -5
    assert learning_api.post(EVALUATE, json=drifted_payload).status_code == 422


def test_missing_context_name_is_rejected(
    learning_api: TestClient, drifted_payload: dict[str, Any]
) -> None:
    drifted_payload.pop("context_name")
    assert learning_api.post(EVALUATE, json=drifted_payload).status_code == 422
