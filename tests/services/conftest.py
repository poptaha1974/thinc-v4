# -*- coding: utf-8 -*-
"""Shared fixtures for the THINC API tests.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
"""
from __future__ import annotations

from typing import Any

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi.testclient import TestClient  # noqa: E402


@pytest.fixture(scope="module")
def api() -> TestClient:
    """Client for the main THINC Intelligence OS app."""

    from services.api.main import app

    return TestClient(app)


@pytest.fixture(scope="module")
def learning_api() -> TestClient:
    from services.api.learning_app import app

    return TestClient(app)


@pytest.fixture(scope="module")
def research_api() -> TestClient:
    from services.api.research_app import app

    return TestClient(app)


@pytest.fixture
def campaign_payload() -> dict[str, Any]:
    """A realistic Egyptian COD campaign: Meta leads → confirmed → delivered."""

    return {
        "product": {
            "name": "Karseell Maca Collagen",
            "cost": 577.0,
            "price": 899.0,
            "inventory_units": 120,
            "category": "hair_care",
            "target_market": "Egypt",
        },
        "campaign": {
            "name": "Karseell — Purchase",
            "spend": 4000.0,
            "meta_leads": 120,
            "confirmed_orders": 60,
            "delivered_orders": 48,
            "returned_orders": 6,
            "channel": "Meta Ads",
        },
        "economics": {
            "product_cost": 577.0,
            "shipping_success_cost": 80.0,
            "shipping_return_cost": 40.0,
            "packaging_cost_per_order": 15.0,
        },
    }
