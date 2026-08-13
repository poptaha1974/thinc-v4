from __future__ import annotations

import json
import os
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from thinc_v4.v4_2.master_framework import AutoUpdateResearchLayer
from thinc_v4.v4_2.media_runner import build_report


KARSEELL_REFERENCE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "v4_2"
    / "Karseell_THINC_v4_2_input_2026-08-09.json"
)


def _karseell_payload():
    """The Karseell reference capture exactly as archived on 2026-08-09."""

    return json.loads(KARSEELL_REFERENCE.read_text(encoding="utf-8"))


def _rebased_karseell_payload(reference_age=timedelta(hours=6)):
    """Return the reference capture with its evidence timestamps rebased.

    Freshness limits are relative to *now* (1-7 days depending on the source),
    so an archived fixture would decay into `STALE` as time passes and make this
    test fail on a calendar date rather than on a behavior change. The capture is
    shifted forward as a block - relative spacing between the observations is
    preserved - so the newest observation sits `reference_age` before now.
    """

    payload = _karseell_payload()
    evidence = payload.get("market_evidence") or []
    stamps = [
        datetime.fromisoformat(item["collected_at"])
        for item in evidence
        if item.get("collected_at")
    ]
    if not stamps:
        return payload
    shift = (datetime.now(timezone.utc) - reference_age) - max(stamps)
    for item in evidence:
        collected_at = item.get("collected_at")
        if collected_at:
            item["collected_at"] = (datetime.fromisoformat(collected_at) + shift).isoformat()
    return payload


def base_payload():
    return {
        "economics": {
            "selling_price": 1000,
            "product_cost": 500,
            "packaging_cost": 20,
            "company_shipping_cost": 70,
            "collection_fees": 20,
            "expected_return_cost_per_order": 30,
            "variable_operations_cost": 10,
            "confirmation_rate_pct": 80,
            "delivery_rate_from_confirmed_pct": 75,
            "safety_margin_pct": 30,
        },
        "config": {
            "sales_channel": "website",
            "total_daily_budget": 1000,
            "pixel_ready": True,
            "capi_ready": True,
            "purchase_event_configured": True,
            "budget_mode": "Controlled ABO",
            "evidence_mode": "standard",
        },
    }


def complete_niche_payload(**overrides):
    payload = {
        "discovery_path": {
            "market": "Beauty & Personal Care",
            "niche": "Hair Care",
            "micro_niche": "Egyptian women seeking home care for dry and frizzy hair",
            "persona": "Trust-sensitive Egyptian woman buying hair care online",
            "problem_jtbd": "Improve softness and appearance while avoiding counterfeit products",
            "product": "Sample Hair Mask",
        },
        "reverse_validation_path": {
            "product": "Sample Hair Mask",
            "problem_jtbd": "Improve softness and appearance while avoiding counterfeit products",
            "persona": "Trust-sensitive Egyptian woman buying hair care online",
            "micro_niche": "Egyptian women seeking home care for dry and frizzy hair",
            "niche": "Hair Care",
            "market": "Beauty & Personal Care",
        },
        "product_solves_problem": True,
        "persona_matches_problem": True,
        "offer_strength": "strong",
        "economics_viable": True,
        "critical_risks": [],
        "unresolved_evidence": [],
    }
    payload.update(overrides)
    return payload


def fresh_market_payload():
    collected_at = datetime.now(timezone.utc).isoformat()
    common = {
        "status": "COLLECTED",
        "query": "sample product",
        "country": "Egypt",
        "collected_at": collected_at,
        "collection_method": "file_upload",
    }
    return [
        {
            **common,
            "source": "google_trends",
            "timeframe": "past 12 months and past 5 years",
            "source_reference": "google-trends-sample.csv",
            "summary": "Normalized interest and seasonality were documented.",
            "metrics": {
                "relative_interest_index": 61,
                "signal_direction": "positive",
            },
        },
        {
            **common,
            "source": "meta_ad_library",
            "timeframe": "active ads observed on collection date",
            "source_reference": "meta-ad-library-sample.json",
            "summary": "Active ads were documented without profitability claims.",
            "metrics": {
                "active_ads_observed": 4,
                "signal_direction": "positive",
            },
        },
        {
            **common,
            "source": "marketplace",
            "timeframe": "current listings on collection date",
            "source_reference": "marketplace-sample.json",
            "summary": "Listings, prices, and published proof were documented.",
            "metrics": {
                "listing_count_observed": 3,
                "signal_direction": "positive",
            },
        },
    ]


def fresh_scale_payload(**metric_overrides):
    evidence = fresh_market_payload()
    metrics = {
        "spend": 2400,
        "orders": 20,
        "confirmed_orders": 16,
        "delivered_orders": 12,
        "delivered_cpa": 200.0,
        "delivery_rate_pct": 75.0,
        "returns": 1,
        "delivered_profit": 2400.0,
        "signal_direction": "positive",
    }
    metrics.update(metric_overrides)
    evidence.append(
        {
            "source": "first_party_campaign",
            "status": "COLLECTED",
            "query": "campaign delivered-order cohort",
            "country": "Egypt",
            "timeframe": "past 24 hours",
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "collection_method": "file_upload",
            "source_reference": "campaign-outcomes-sample.json",
            "summary": "Delivered-order and profit outcomes were exported.",
            "metrics": metrics,
        }
    )
    return evidence


class MarketSignalIntegrationTests(unittest.TestCase):
    def test_runner_without_market_evidence_returns_hold_report(self):
        report = build_report(base_payload())

        self.assertIn("market_signal_gate", report)
        self.assertEqual(report["decision"], "INCOMPLETE")
        self.assertEqual(
            report["market_signal_gate"]["decision"],
            "HOLD_FOR_RESEARCH",
        )
        self.assertEqual(report["analysis_status"], "INCOMPLETE")
        self.assertIn("niche_validation", report["completeness_gate"]["missing_components"])
        self.assertEqual(
            report["economics"]["target_purchase_cpa"],
            147.0,
        )

    def test_market_pass_without_niche_is_incomplete(self):
        payload = base_payload()
        payload["market_evidence"] = fresh_market_payload()

        report = build_report(payload)

        self.assertIn("market_signal_gate", report)
        self.assertEqual(report["decision"], "INCOMPLETE")
        self.assertEqual(report["media_protocol_decision"], "PASS")
        self.assertEqual(report["market_signal_gate"]["decision"], "PASS")
        self.assertEqual(report["analysis_status"], "INCOMPLETE")
        self.assertEqual(
            report["market_signal_gate"]["freshness_status_by_source"][
                "google_trends"
            ],
            "FRESH",
        )

    def test_complete_niche_payload_accepts_controlled_test(self):
        payload = base_payload()
        payload["market_evidence"] = fresh_market_payload()
        payload["niche_validation"] = complete_niche_payload()

        report = build_report(payload)

        self.assertEqual(report["analysis_status"], "COMPLETE")
        self.assertEqual(report["decision"], "ACCEPT_AND_TEST")
        self.assertEqual(
            report["niche_validation"]["launch_gate"],
            "CONTROLLED_TEST_ALLOWED",
        )

    def test_economics_failure_vetoes_launch_after_market_pass(self):
        payload = base_payload()
        payload["market_evidence"] = fresh_market_payload()
        payload["niche_validation"] = complete_niche_payload(economics_viable=False)

        report = build_report(payload)

        self.assertEqual(report["market_signal_gate"]["decision"], "PASS")
        self.assertEqual(report["decision"], "NO_LAUNCH_BEFORE_MODIFICATION")
        self.assertEqual(
            report["niche_validation"]["strategic_decision"],
            "REFINE_OFFER",
        )

    def test_runner_rejects_unsupported_market_source(self):
        payload = base_payload()
        payload["market_evidence"] = [
            {
                **fresh_market_payload()[0],
                "source": "invented_source",
            }
        ]

        with self.assertRaisesRegex(ValueError, "Unsupported market source"):
            build_report(payload)

    def test_report_json_preserves_enum_values_and_iso_timestamps(self):
        payload = base_payload()
        payload["market_evidence"] = fresh_market_payload()
        payload["niche_validation"] = complete_niche_payload()

        report = build_report(payload)

        self.assertIn("market_signal_gate", report)
        rendered = json.dumps(report, ensure_ascii=False)
        decoded = json.loads(rendered)
        snapshot = decoded["market_signal_gate"]["evidence_snapshot"][0]
        self.assertEqual(snapshot["source"], "google_trends")
        self.assertEqual(snapshot["status"], "COLLECTED")
        self.assertIn("+00:00", snapshot["collected_at"])

    def test_scale_decision_applies_economics_veto_after_market_gate_passes(self):
        payload = base_payload()
        payload["config"]["decision_stage"] = "scale"
        payload["market_evidence"] = fresh_scale_payload(
            delivered_orders=4,
            delivered_cpa=300.0,
        )
        payload["niche_validation"] = complete_niche_payload()

        report = build_report(payload)

        self.assertEqual(report["market_signal_gate"]["decision"], "PASS")
        self.assertEqual(report["decision"], "BLOCK_SCALE")
        self.assertTrue(
            any("delivered_orders" in reason for reason in report["decision_reasons"])
        )
        self.assertTrue(
            any("delivered_cpa" in reason for reason in report["decision_reasons"])
        )

    def test_scale_passes_when_market_and_existing_scale_thresholds_pass(self):
        payload = base_payload()
        payload["config"]["decision_stage"] = "scale"
        payload["market_evidence"] = fresh_scale_payload()
        payload["niche_validation"] = complete_niche_payload()

        report = build_report(payload)

        self.assertEqual(report["market_signal_gate"]["decision"], "PASS")
        self.assertEqual(report["decision"], "ACCEPT_AND_TEST")
        self.assertEqual(report["media_protocol_decision"], "PASS")
        self.assertIn("decision_reasons", report)
        self.assertTrue(report["decision_reasons"])

    def test_status_layer_reports_access_without_treating_key_as_evidence(self):
        with patch.dict(os.environ, {"GOOGLE_TRENDS_KEY": "configured"}, clear=False):
            status = AutoUpdateResearchLayer.status()

        self.assertIn("market_signal_providers", status)
        google = status["market_signal_providers"]["google_trends"]
        self.assertTrue(google["credential_configured"])
        self.assertEqual(google["automation_status"], "AUTOMATED_PROVIDER_PENDING")
        self.assertFalse(google["evidence_available"])

    def test_karseell_reference_is_not_launchable(self):
        """Fresh evidence: the gate passes, but the offer still may not launch."""

        payload = _rebased_karseell_payload()

        report = build_report(payload)

        self.assertEqual(report["market_signal_gate"]["decision"], "PASS")
        self.assertEqual(
            report["niche_validation"]["strategic_decision"],
            "REFINE_OFFER",
        )
        self.assertEqual(
            report["niche_validation"]["launch_gate"],
            "NO_LAUNCH_BEFORE_MODIFICATION",
        )
        self.assertEqual(report["decision"], "NO_LAUNCH_BEFORE_MODIFICATION")

    def test_karseell_reference_as_captured_is_held_for_research(self):
        """The archived capture is past its freshness window, so it must hold."""

        payload = _karseell_payload()

        report = build_report(payload)

        self.assertEqual(
            report["market_signal_gate"]["decision"],
            "HOLD_FOR_RESEARCH",
        )
        self.assertEqual(report["decision"], "NO_LAUNCH_BEFORE_MODIFICATION")


if __name__ == "__main__":
    unittest.main()
