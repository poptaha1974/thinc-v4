# -*- coding: utf-8 -*-
"""Tests for the External Social Research & Daily Intelligence API.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

Includes the regression for the domain/source-type mix-up: the engine used to
compare an observation's *domain* against `SEARCH_TRENDS`, which is a
`ResearchSourceType` member, so every request carrying a search signal raised
`AttributeError` and returned a 500.
"""
from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

OPTIONS = "/api/external-research/options"
DAILY = "/api/external-research/daily-egypt-intelligence"


@pytest.fixture
def daily_payload(research_api: TestClient) -> dict[str, Any]:
    options = research_api.get(OPTIONS).json()
    return {
        "intelligence_date": "2026-08-13",
        "observations": [
            {
                "domain": "inflation_prices",
                "summary": "ارتفاع أسعار مستلزمات العناية المستوردة",
                "evidence": "نشرة الجهاز المركزي للتعبئة والإحصاء",
                "direction": "up",
                "evidence_strength": options["evidence_strengths"][0],
                "market_impact": "high",
                "commercial_implications": ["price_sensitivity"],
                "affected_segments": ["S2"],
                "affected_categories": ["hair_care"],
                "source": {
                    "title": "تقرير التضخم الشهري",
                    "source_name": "CAPMAS",
                    "source_type": "official_statistics",
                    "reliability_score": 9.0,
                },
            }
        ],
        "baseline_weights": options["default_weights"],
    }


def search_observation(direction: str = "up") -> dict[str, Any]:
    """An observation whose *source* is search trends (not a domain)."""

    return {
        "domain": "product_category_trend",
        "summary": "ارتفاع البحث على كارسيل في مصر",
        "evidence": "Google Trends — EG — 12 شهرًا",
        "direction": direction,
        "evidence_strength": "medium",
        "market_impact": "medium",
        "commercial_implications": ["category_demand_up"],
        "affected_segments": ["S2"],
        "affected_categories": ["hair_care"],
        "source": {
            "title": "Karseell — Egypt interest",
            "source_name": "Google Trends",
            "source_type": "search_trends",
            "reliability_score": 6.0,
        },
    }


def test_options_expose_domains_and_source_types_separately(research_api: TestClient) -> None:
    body = research_api.get(OPTIONS).json()

    assert "search_trends" in body["source_types"]
    assert "search_trends" not in body["domains"], "search trends is a source, not a domain"
    assert body["directions"] and body["market_impacts"]
    assert body["default_weights"]


def test_health_endpoint(research_api: TestClient) -> None:
    assert research_api.get("/health").json()["status"] == "ok"


def test_daily_intelligence_returns_a_full_briefing(
    research_api: TestClient, daily_payload: dict[str, Any]
) -> None:
    response = research_api.post(DAILY, json=daily_payload)
    assert response.status_code == 200, response.text
    body = response.json()

    assert body["intelligence_date"] == "2026-08-13"
    assert 0 <= body["confidence_score"] <= 10
    for key in (
        "top_signals",
        "behavior_shifts",
        "commercial_risks",
        "commercial_opportunities",
        "campaign_guidance",
        "research_gaps",
        "required_human_review",
        "source_audit",
    ):
        assert isinstance(body[key], list), key
    assert isinstance(body["recommended_weight_updates"], dict)


def test_search_trend_observation_does_not_crash_the_endpoint(
    research_api: TestClient, daily_payload: dict[str, Any]
) -> None:
    """Regression: this request used to raise AttributeError and return 500."""

    daily_payload["observations"].append(search_observation())

    response = research_api.post(DAILY, json=daily_payload)

    assert response.status_code == 200, response.text
    body = response.json()
    joined = " ".join(
        body["commercial_opportunities"] + body["behavior_shifts"] + body["campaign_guidance"]
    ).lower()
    assert "search" in joined


def test_rising_search_interest_raises_search_trend_momentum(
    research_api: TestClient, daily_payload: dict[str, Any]
) -> None:
    without = research_api.post(DAILY, json=daily_payload).json()
    baseline = without["recommended_weight_updates"]["search_trend_momentum"]

    daily_payload["observations"].append(search_observation())
    with_search = research_api.post(DAILY, json=daily_payload).json()

    assert with_search["recommended_weight_updates"]["search_trend_momentum"] > baseline


def test_missing_search_coverage_is_reported_as_a_research_gap(
    research_api: TestClient, daily_payload: dict[str, Any]
) -> None:
    gaps = research_api.post(DAILY, json=daily_payload).json()["research_gaps"]
    assert any("search trend momentum" in gap for gap in gaps)

    daily_payload["observations"].append(search_observation())
    gaps_with_search = research_api.post(DAILY, json=daily_payload).json()["research_gaps"]
    assert not any("search trend momentum" in gap for gap in gaps_with_search)


def test_political_context_always_requires_human_review(
    research_api: TestClient, daily_payload: dict[str, Any]
) -> None:
    daily_payload["observations"].append(
        {
            "domain": "political_context",
            "summary": "حالة عامة حساسة",
            "evidence": "تغطية إخبارية",
            "direction": "mixed",
            "evidence_strength": "low",
            "market_impact": "medium",
            "commercial_implications": ["brand_tone_adjustment"],
            "source": {
                "title": "مراجعة إخبارية",
                "source_name": "News desk",
                "source_type": "news",
                "reliability_score": 4.0,
            },
        }
    )

    body = research_api.post(DAILY, json=daily_payload).json()

    assert body["required_human_review"]
    assert any("olitical" in note or "eview" in note for note in body["required_human_review"])


def test_unknown_domain_is_a_client_error_not_a_server_error(
    research_api: TestClient, daily_payload: dict[str, Any]
) -> None:
    daily_payload["observations"][0]["domain"] = "not_a_domain"

    response = research_api.post(DAILY, json=daily_payload)

    assert response.status_code == 422
    assert response.json()["error"] == "invalid_input"


def test_search_trends_is_rejected_as_a_domain(
    research_api: TestClient, daily_payload: dict[str, Any]
) -> None:
    """It is a source type; sending it as a domain must be a clean 422."""

    daily_payload["observations"][0]["domain"] = "search_trends"

    response = research_api.post(DAILY, json=daily_payload)

    assert response.status_code == 422
    assert "Invalid value" in response.json()["detail"]


def test_reliability_score_out_of_range_is_rejected(
    research_api: TestClient, daily_payload: dict[str, Any]
) -> None:
    daily_payload["observations"][0]["source"]["reliability_score"] = 50
    assert research_api.post(DAILY, json=daily_payload).status_code == 422


def test_empty_observation_list_is_handled(
    research_api: TestClient, daily_payload: dict[str, Any]
) -> None:
    daily_payload["observations"] = []

    response = research_api.post(DAILY, json=daily_payload)

    assert response.status_code == 200, response.text
    assert response.json()["research_gaps"]
