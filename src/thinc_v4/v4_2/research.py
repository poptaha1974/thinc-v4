# -*- coding: utf-8 -*-
"""Auto-update research layer (safe stubs, no silent model changes).

THINC™ v4.2 — Invented by Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 Dr. Ehab Taha — Egy-Pioneers Academy.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, List
from .market_signals import AutomatedProvider
from .theories import UpdateCadence


@dataclass
class ResearchSourceSpec:
    name: str
    env_key: str
    purpose: str
    update_cadence: UpdateCadence
    configured: bool = False
    provider_implemented: bool = False
    enabled: bool = False


class AutoUpdateResearchLayer:
    """Safe auto-update skeleton. Actual APIs must be configured by environment variables."""

    @staticmethod
    def default_sources() -> List[ResearchSourceSpec]:
        U = UpdateCadence
        sources = [
            ResearchSourceSpec("CAPMAS", "CAPMAS_API_KEY", "Egyptian demographic and economic updates", U.MONTHLY),
            ResearchSourceSpec("Arab Barometer", "ARAB_BAROMETER_API_KEY", "Arab cultural and social indicators", U.QUARTERLY),
            ResearchSourceSpec("Meta Ad Library", "META_ADLIB_TOKEN", "Competitor creative intelligence", U.LIVE),
            ResearchSourceSpec("TikTok Creative Center", "TIKTOK_API_KEY", "Trend and creative insights", U.WEEKLY),
            ResearchSourceSpec("Google Trends", "GOOGLE_TRENDS_KEY", "Demand and search trends", U.WEEKLY),
            ResearchSourceSpec("Noon/Jumia/Amazon", "ECOM_PRICE_API_KEY", "Prices and availability", U.LIVE),
        ]
        for s in sources:
            s.configured = bool(os.environ.get(s.env_key))
            s.enabled = s.configured and s.provider_implemented
        return sources

    @staticmethod
    def status() -> Dict[str, Any]:
        sources = AutoUpdateResearchLayer.default_sources()
        return {
            "enabled": [s.name for s in sources if s.enabled],
            "disabled": [s.name for s in sources if not s.enabled],
            "configured_credentials": [s.name for s in sources if s.configured],
            "market_signal_providers": {
                "google_trends": AutomatedProvider.status(
                    "GOOGLE_TRENDS_KEY", provider_implemented=False
                ),
                "meta_ad_library": AutomatedProvider.status(
                    "META_ADLIB_TOKEN", provider_implemented=False
                ),
            },
            "note": (
                "Browser-assisted research and file ingestion are available. "
                "Automated providers remain pending; credentials alone are not evidence."
            ),
        }
