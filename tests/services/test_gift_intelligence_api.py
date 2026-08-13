# -*- coding: utf-8 -*-
"""Tests for the Gift Decision Intelligence API.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
"""
from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

OPTIONS = "/api/gift-intelligence/options"
EVALUATE = "/api/gift-intelligence/evaluate"


@pytest.fixture
def gift_payload(api: TestClient) -> dict[str, Any]:
    options = api.get(OPTIONS).json()
    return {
        "product": {
            "name": "كوباية حرارية بتغليف هدية",
            "category": options["product_categories"][0],
            "price_band": options["price_bands"][1],
            "safety_class": options["gift_safety_classes"][0],
            "perceived_value_score": 7.5,
            "practicality_score": 8.0,
            "packaging_score": 7.0,
            "trust_score": 6.5,
            "margin_score": 7.0,
            "stock_ready": True,
        },
        "occasion": options["occasions"][0],
        "relationship": options["relationships"][0],
        "recipient_gender": options["recipient_gender_contexts"][0],
        "geo_segment": options["geo_segments"][0],
        "social_class_signal": options["social_class_signals"][1],
        "buyer_role": options["buyer_roles"][0],
        "seasonality": options["seasonality_moments"][0],
        "delivery_urgency": options["delivery_urgencies"][2],
        "has_exchange_policy": True,
        "has_real_photos": True,
        "has_reviews": False,
        "can_personalize": False,
        "buyer_knows_recipient_taste": False,
    }


def test_options_expose_every_decision_dimension(api: TestClient) -> None:
    body = api.get(OPTIONS).json()
    for key in (
        "occasions",
        "price_bands",
        "relationships",
        "buyer_roles",
        "geo_segments",
        "product_categories",
        "gift_safety_classes",
        "delivery_urgencies",
        "completeness_checklist",
    ):
        assert body[key], key


def test_evaluate_returns_a_scored_decision(api: TestClient, gift_payload: dict[str, Any]) -> None:
    response = api.post(EVALUATE, json=gift_payload)
    assert response.status_code == 200, response.text
    body = response.json()

    assert 0 <= body["score"] <= 10
    assert 0 <= body["product_occasion_fit"] <= 10
    assert body["risk_level"]
    assert body["safety_verdict"]
    assert body["positioning"]
    assert body["recommended_angle"]
    for key in ("blind_spots", "recommendations", "objections"):
        assert isinstance(body[key], list)


def test_missing_reviews_and_personalisation_produce_recommendations(
    api: TestClient, gift_payload: dict[str, Any]
) -> None:
    body = api.post(EVALUATE, json=gift_payload).json()
    assert body["recommendations"], "a gift with no reviews must get concrete advice"


def test_weak_offer_scores_below_a_strong_one(api: TestClient, gift_payload: dict[str, Any]) -> None:
    strong = api.post(EVALUATE, json=gift_payload).json()["score"]

    weak_payload = dict(gift_payload)
    weak_payload["product"] = dict(gift_payload["product"])
    weak_payload["product"].update(
        {
            "perceived_value_score": 2.0,
            "practicality_score": 2.0,
            "packaging_score": 1.0,
            "trust_score": 2.0,
            "stock_ready": False,
        }
    )
    weak_payload.update({"has_exchange_policy": False, "has_real_photos": False})

    weak = api.post(EVALUATE, json=weak_payload).json()["score"]
    assert weak < strong


def test_unknown_occasion_is_a_client_error_not_a_server_error(
    api: TestClient, gift_payload: dict[str, Any]
) -> None:
    gift_payload["occasion"] = "مناسبة غير موجودة"

    response = api.post(EVALUATE, json=gift_payload)

    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "invalid_input"
    assert "Invalid value" in body["detail"]


def test_out_of_range_product_score_is_rejected(
    api: TestClient, gift_payload: dict[str, Any]
) -> None:
    gift_payload["product"]["trust_score"] = 99
    assert api.post(EVALUATE, json=gift_payload).status_code == 422


def test_empty_product_name_is_rejected(api: TestClient, gift_payload: dict[str, Any]) -> None:
    gift_payload["product"]["name"] = ""
    assert api.post(EVALUATE, json=gift_payload).status_code == 422
