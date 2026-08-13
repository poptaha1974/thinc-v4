# -*- coding: utf-8 -*-
"""Tests for the main THINC Intelligence OS API.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

Covers the happy path and the rejection path for every route, plus the COD truth
rule (Purchase counts only after delivery) and the demo-mode boundary.
"""
from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient


def test_health_reports_engine_and_mode(api: TestClient) -> None:
    response = api.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["engine"]
    assert body["mode"]


def test_theory_summary_keeps_attribution(api: TestClient) -> None:
    response = api.get("/api/theories/summary")
    assert response.status_code == 200
    body = response.json()
    assert body["count"] >= 50
    assert body["domains"]
    assert "الدكتور إيهاب طه" in body["watermark"]


def test_campaign_analysis_is_decision_support_only(
    api: TestClient, campaign_payload: dict[str, Any]
) -> None:
    response = api.post("/api/campaign/analyze", json=campaign_payload)
    assert response.status_code == 200, response.text
    body = response.json()

    assert body["mode"] == "decision_support"
    assert body["campaign_name"] == "Karseell — Purchase"
    assert body["product_name"] == "Karseell Maca Collagen"
    assert 0 <= body["thinc_score"] <= 10
    assert body["decision"]
    assert body["risk_level"]
    assert isinstance(body["blind_spots"], list)
    assert isinstance(body["recommendations"], list)


def test_campaign_analysis_uses_delivered_orders_not_leads(
    api: TestClient, campaign_payload: dict[str, Any]
) -> None:
    """COD truth rule: real CPA is spend per delivered order, never per lead."""

    body = api.post("/api/campaign/analyze", json=campaign_payload).json()

    spend = campaign_payload["campaign"]["spend"]
    delivered = campaign_payload["campaign"]["delivered_orders"]
    leads = campaign_payload["campaign"]["meta_leads"]

    assert body["real_cpa"] == round(spend / delivered, 2)
    assert body["meta_cpa"] == round(spend / leads, 2)
    assert body["real_cpa"] > body["meta_cpa"]
    assert body["delivery_rate"] == round(delivered / campaign_payload["campaign"]["confirmed_orders"] * 100, 2)


def test_campaign_analysis_rejects_impossible_order_flow(
    api: TestClient, campaign_payload: dict[str, Any]
) -> None:
    """More delivered than confirmed orders is a data error, not a great funnel."""

    campaign_payload["campaign"]["delivered_orders"] = 90
    campaign_payload["campaign"]["confirmed_orders"] = 60

    response = api.post("/api/campaign/analyze", json=campaign_payload)

    assert response.status_code == 422
    assert "delivered_orders" in response.text


def test_campaign_analysis_rejects_negative_spend(
    api: TestClient, campaign_payload: dict[str, Any]
) -> None:
    campaign_payload["campaign"]["spend"] = -100
    assert api.post("/api/campaign/analyze", json=campaign_payload).status_code == 422


def test_founder_readiness_scores_and_advises(api: TestClient) -> None:
    response = api.post(
        "/api/founder/readiness",
        json={
            "execution_score": 8,
            "discipline_score": 7,
            "learning_speed_score": 9,
            "resilience_score": 6,
            "focus_score": 5,
            "financial_discipline_score": 7,
        },
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert 0 <= body["score"] <= 10
    assert body["verdict"]
    assert isinstance(body["recommendations"], list)


def test_founder_readiness_rejects_out_of_range_scores(api: TestClient) -> None:
    response = api.post(
        "/api/founder/readiness",
        json={
            "execution_score": 42,
            "discipline_score": 7,
            "learning_speed_score": 9,
            "resilience_score": 6,
            "focus_score": 5,
            "financial_discipline_score": 7,
        },
    )
    assert response.status_code == 422


def test_social_culture_options_are_enumerated(api: TestClient) -> None:
    body = api.get("/api/social-culture/options").json()
    assert body
    for values in body.values():
        assert isinstance(values, list)
        assert values


def test_social_culture_profile_returns_cohort_language(api: TestClient) -> None:
    options = api.get("/api/social-culture/options").json()
    cohort = options["cohorts"][0]
    life_stage = options["life_stages"][0]

    response = api.post(
        "/api/social-culture/profile",
        json={"cohort": cohort, "life_stage": life_stage},
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["cohort"] == cohort
    assert body["dominant_mindset"]
    assert body["words_to_use"] and body["words_to_avoid"]
    assert body["trust_signals"]


def test_social_culture_profile_rejects_unknown_cohort(api: TestClient) -> None:
    response = api.post(
        "/api/social-culture/profile",
        json={"cohort": "not_a_cohort", "life_stage": "student"},
    )
    assert response.status_code == 422
    assert "Invalid value" in response.text


def test_gift_fit_surfaces_cohort_specific_guidance(api: TestClient) -> None:
    """The cohort profile must influence the output, not be computed and dropped."""

    options = api.get("/api/social-culture/options").json()
    payload = {
        "cohort": options["cohorts"][0],
        "life_stage": options["life_stages"][0],
        "occasion": options["occasions"][0],
        "price_band": options["price_bands"][0],
        "has_packaging": False,
        "has_exchange_policy": False,
        "has_social_proof": False,
        "is_practical": True,
        "looks_more_expensive_than_price": False,
        "has_clear_use_case": False,
    }

    response = api.post("/api/social-culture/gift-fit", json=payload)
    assert response.status_code == 200, response.text
    body = response.json()

    assert 0 <= body["score"] <= 10
    assert body["risk_level"]
    assert body["positioning_sentence"]
    joined = " ".join(body["blind_spots"] + body["recommendations"])
    assert "تجنّب في الرسالة" in joined
    assert "قنوات مفضّلة للعرض" in joined


def test_integrations_are_all_demo_until_credentials_exist(api: TestClient) -> None:
    """The dashboard must never claim a live integration that is not configured."""

    body = api.get("/api/integrations/status").json()
    assert body["items"]
    for item in body["items"]:
        assert item["mode"] == "demo"
        assert item["connected"] is False
        assert item["message"]
