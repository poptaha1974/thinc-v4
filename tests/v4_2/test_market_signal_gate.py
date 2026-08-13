from __future__ import annotations

import importlib
import os
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from unittest.mock import patch


market = importlib.import_module("thinc_v4.v4_2.market_signals")


def fresh_meta(now: datetime):
    return market.MarketSignalEvidence(
        source=market.MarketSignalSource.META_AD_LIBRARY,
        status=market.EvidenceStatus.COLLECTED,
        query="sample product",
        country="Egypt",
        timeframe="active ads observed on collection date",
        collected_at=now,
        collection_method=market.CollectionMethod.BROWSER_ASSISTED,
        source_reference="https://www.facebook.com/ads/library/",
        summary="Active-ad activity was documented without profitability claims.",
        metrics={"active_ads_observed": 4, "signal_direction": "positive"},
    )


def fresh_trends(now: datetime):
    return market.MarketSignalEvidence(
        source=market.MarketSignalSource.GOOGLE_TRENDS,
        status=market.EvidenceStatus.COLLECTED,
        query="sample product",
        country="Egypt",
        timeframe="past 12 months and past 5 years",
        collected_at=now,
        collection_method=market.CollectionMethod.BROWSER_ASSISTED,
        source_reference="https://trends.google.com/trends/",
        summary="Normalized search interest and seasonality were documented.",
        metrics={"relative_interest_index": 61, "signal_direction": "positive"},
    )


def fresh_marketplace(now: datetime):
    return market.MarketSignalEvidence(
        source=market.MarketSignalSource.MARKETPLACE,
        status=market.EvidenceStatus.COLLECTED,
        query="sample product",
        country="Egypt",
        timeframe="current listings on collection date",
        collected_at=now,
        collection_method=market.CollectionMethod.BROWSER_ASSISTED,
        source_reference="https://www.noon.com/egypt-en/",
        summary="Listings, prices, and published customer proof were documented.",
        metrics={"listing_count_observed": 3, "signal_direction": "positive"},
    )


def fresh_first_party(now: datetime, **metric_overrides):
    metrics = {
        "spend": 1000,
        "orders": 20,
        "confirmed_orders": 16,
        "delivered_orders": 12,
        "delivered_cpa": 83.33,
        "delivery_rate_pct": 75.0,
        "returns": 1,
        "delivered_profit": 2400,
        "signal_direction": "positive",
    }
    metrics.update(metric_overrides)
    return market.MarketSignalEvidence(
        source=market.MarketSignalSource.FIRST_PARTY_CAMPAIGN,
        status=market.EvidenceStatus.COLLECTED,
        query="campaign delivered-order cohort",
        country="Egypt",
        timeframe="past 24 hours",
        collected_at=now,
        collection_method=market.CollectionMethod.FILE_UPLOAD,
        source_reference="campaign-outcomes-2026-08-09.json",
        summary="Delivered-order and profit outcomes were exported from first-party data.",
        metrics=metrics,
    )


class MarketSignalGateTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 8, 9, 12, 0, tzinfo=timezone.utc)

    def test_missing_google_trends_holds_research_without_zero_demand(self):
        self.assertIsNotNone(market, "Market-signal module must exist")
        evidence = [fresh_meta(self.now), fresh_marketplace(self.now)]

        result = market.MarketSignalTriangulationEngine.evaluate(
            evidence,
            market.DecisionStage.PRE_TEST_RESEARCH,
            now=self.now,
        )

        self.assertEqual(result.decision, market.GateDecision.HOLD_FOR_RESEARCH)
        self.assertEqual(
            result.coverage_status_by_source["google_trends"],
            "NOT_COLLECTED",
        )
        self.assertNotIn("zero demand", " ".join(result.reasons).lower())

    def test_non_egypt_record_does_not_satisfy_gate(self):
        evidence = [
            replace(fresh_trends(self.now), country="Saudi Arabia"),
            fresh_meta(self.now),
            fresh_marketplace(self.now),
        ]

        result = market.MarketSignalTriangulationEngine.evaluate(
            evidence,
            market.DecisionStage.PRE_TEST_RESEARCH,
            now=self.now,
        )

        self.assertEqual(result.decision, market.GateDecision.HOLD_FOR_RESEARCH)
        self.assertEqual(
            result.coverage_status_by_source["google_trends"],
            "WRONG_COUNTRY",
        )
        self.assertTrue(any("Egypt" in action for action in result.required_actions))

    def test_stale_marketplace_holds_research(self):
        evidence = [
            fresh_trends(self.now),
            fresh_meta(self.now),
            replace(
                fresh_marketplace(self.now),
                collected_at=self.now - timedelta(days=4),
            ),
        ]

        result = market.MarketSignalTriangulationEngine.evaluate(
            evidence,
            market.DecisionStage.PRE_TEST_RESEARCH,
            now=self.now,
        )

        self.assertEqual(result.decision, market.GateDecision.HOLD_FOR_RESEARCH)
        self.assertEqual(result.freshness_status_by_source["marketplace"], "STALE")
        self.assertTrue(any("marketplace" in reason.lower() for reason in result.reasons))

    def test_missing_meta_ad_library_holds_research(self):
        evidence = [fresh_trends(self.now), fresh_marketplace(self.now)]

        result = market.MarketSignalTriangulationEngine.evaluate(
            evidence,
            market.DecisionStage.PRE_TEST_RESEARCH,
            now=self.now,
        )

        self.assertEqual(result.decision, market.GateDecision.HOLD_FOR_RESEARCH)
        self.assertTrue(
            any("Meta Ad Library" in action for action in result.required_actions)
        )

    def test_complete_fresh_research_evidence_passes(self):
        evidence = [
            fresh_trends(self.now),
            fresh_meta(self.now),
            fresh_marketplace(self.now),
        ]

        result = market.MarketSignalTriangulationEngine.evaluate(
            evidence,
            market.DecisionStage.PRE_TEST_RESEARCH,
            now=self.now,
        )

        self.assertEqual(result.decision, market.GateDecision.PASS)
        self.assertEqual(
            {
                result.freshness_status_by_source[source]
                for source in ("google_trends", "meta_ad_library", "marketplace")
            },
            {"FRESH"},
        )

    def test_malformed_collected_record_becomes_invalid_with_field_reasons(self):
        invalid_trends = replace(fresh_trends(self.now), summary="")
        evidence = [invalid_trends, fresh_meta(self.now), fresh_marketplace(self.now)]

        result = market.MarketSignalTriangulationEngine.evaluate(
            evidence,
            market.DecisionStage.PRE_TEST_RESEARCH,
            now=self.now,
        )

        self.assertEqual(result.decision, market.GateDecision.HOLD_FOR_RESEARCH)
        self.assertEqual(result.coverage_status_by_source["google_trends"], "INVALID")
        self.assertTrue(any("summary" in reason for reason in result.reasons))

    def test_synthetic_example_metrics_cannot_satisfy_market_gate(self):
        synthetic_trends = replace(
            fresh_trends(self.now),
            metrics={"example_only": True, "replace_with_observed_metrics": True},
        )
        result = market.MarketSignalTriangulationEngine.evaluate(
            [synthetic_trends, fresh_meta(self.now), fresh_marketplace(self.now)],
            market.DecisionStage.PRE_TEST_RESEARCH,
            now=self.now,
        )

        self.assertEqual(result.decision, market.GateDecision.HOLD_FOR_RESEARCH)
        self.assertEqual(result.coverage_status_by_source["google_trends"], "INVALID")
        self.assertTrue(any("synthetic" in reason.lower() for reason in result.reasons))

    def test_multiple_invalid_timestamps_are_retained_without_datetime_crash(self):
        naive_time_record = replace(
            fresh_trends(self.now),
            collected_at=self.now.replace(tzinfo=None),
        )
        missing_summary_record = replace(fresh_trends(self.now), summary="")
        try:
            result = market.MarketSignalTriangulationEngine.evaluate(
                [
                    naive_time_record,
                    missing_summary_record,
                    fresh_meta(self.now),
                    fresh_marketplace(self.now),
                ],
                market.DecisionStage.PRE_TEST_RESEARCH,
                now=self.now,
            )
        except TypeError as exc:
            self.fail(f"Invalid historical records must be retained without crashing: {exc}")

        self.assertEqual(result.decision, market.GateDecision.HOLD_FOR_RESEARCH)
        self.assertEqual(len(result.evidence_snapshot), 4)

    def test_browser_and_file_ingestion_share_one_evidence_schema(self):
        self.assertTrue(hasattr(market, "BrowserAssistedProvider"))
        self.assertTrue(hasattr(market, "FileEvidenceProvider"))
        payload = {
            "source": "google_trends",
            "status": "COLLECTED",
            "query": "sample product",
            "country": "Egypt",
            "timeframe": "past 12 months",
            "collected_at": self.now.isoformat(),
            "collection_method": "browser_assisted",
            "source_reference": "https://trends.google.com/trends/",
            "summary": "Normalized interest was documented.",
            "metrics": {"relative_interest_index": 61},
        }

        browser_record = market.BrowserAssistedProvider.ingest([payload])[0]
        file_record = market.FileEvidenceProvider.ingest(
            [{**payload, "collection_method": "file_upload"}]
        )[0]

        self.assertIsInstance(browser_record, market.MarketSignalEvidence)
        self.assertIsInstance(file_record, market.MarketSignalEvidence)
        self.assertEqual(browser_record.source, file_record.source)
        self.assertEqual(browser_record.query, file_record.query)

    def test_normalized_csv_ingestion_uses_the_same_evidence_schema(self):
        self.assertTrue(hasattr(market.FileEvidenceProvider, "ingest_csv_text"))
        csv_text = (
            "source,status,query,country,timeframe,collected_at,collection_method,"
            "source_reference,summary,metrics\n"
            'google_trends,COLLECTED,sample product,Egypt,past 12 months,'
            f'{self.now.isoformat()},file_upload,trends.csv,Normalized interest documented,'
            '"{""relative_interest_index"": 61}"\n'
        )

        record = market.FileEvidenceProvider.ingest_csv_text(csv_text)[0]

        self.assertIsInstance(record, market.MarketSignalEvidence)
        self.assertEqual(record.source, market.MarketSignalSource.GOOGLE_TRENDS)
        self.assertEqual(record.metrics, {"relative_interest_index": 61})

    def test_campaign_evidence_is_not_required_before_first_test(self):
        result = market.MarketSignalTriangulationEngine.evaluate(
            [fresh_trends(self.now), fresh_meta(self.now), fresh_marketplace(self.now)],
            market.DecisionStage.PRE_TEST_RESEARCH,
            now=self.now,
        )

        self.assertEqual(result.decision, market.GateDecision.PASS)
        self.assertEqual(
            result.coverage_status_by_source["first_party_campaign"],
            "NOT_APPLICABLE",
        )

    def test_missing_delivered_profit_blocks_scale(self):
        campaign_without_profit = fresh_first_party(self.now)
        campaign_without_profit.metrics.pop("delivered_profit")
        result = market.MarketSignalTriangulationEngine.evaluate(
            [
                fresh_trends(self.now),
                fresh_meta(self.now),
                fresh_marketplace(self.now),
                campaign_without_profit,
            ],
            market.DecisionStage.SCALE,
            now=self.now,
        )

        self.assertEqual(result.decision, market.GateDecision.BLOCK_SCALE)
        self.assertTrue(any("delivered_profit" in reason for reason in result.reasons))

    def test_positive_fresh_first_party_evidence_passes_scale_market_gate(self):
        result = market.MarketSignalTriangulationEngine.evaluate(
            [
                fresh_trends(self.now),
                fresh_meta(self.now),
                fresh_marketplace(self.now),
                fresh_first_party(self.now),
            ],
            market.DecisionStage.SCALE,
            now=self.now,
        )

        self.assertEqual(result.decision, market.GateDecision.PASS)
        self.assertEqual(
            result.freshness_status_by_source["first_party_campaign"],
            "FRESH",
        )

    def test_non_numeric_delivered_profit_blocks_scale_without_crashing(self):
        try:
            result = market.MarketSignalTriangulationEngine.evaluate(
                [
                    fresh_trends(self.now),
                    fresh_meta(self.now),
                    fresh_marketplace(self.now),
                    fresh_first_party(self.now, delivered_profit="not-a-number"),
                ],
                market.DecisionStage.SCALE,
                now=self.now,
            )
        except (TypeError, ValueError) as exc:
            self.fail(f"Malformed campaign metrics must block, not crash: {exc}")

        self.assertEqual(result.decision, market.GateDecision.BLOCK_SCALE)
        self.assertTrue(
            any("delivered_profit must be numeric" in reason for reason in result.reasons)
        )

    def test_provider_configuration_key_without_records_cannot_pass_gate(self):
        self.assertTrue(hasattr(market, "AutomatedProvider"))
        with patch.dict(os.environ, {"GOOGLE_TRENDS_KEY": "configured"}, clear=False):
            status = market.AutomatedProvider.status(
                "GOOGLE_TRENDS_KEY",
                provider_implemented=False,
            )
            result = market.MarketSignalTriangulationEngine.evaluate(
                [],
                market.DecisionStage.PRE_TEST_RESEARCH,
                now=self.now,
            )

        self.assertTrue(status["credential_configured"])
        self.assertEqual(status["automation_status"], "AUTOMATED_PROVIDER_PENDING")
        self.assertEqual(result.decision, market.GateDecision.HOLD_FOR_RESEARCH)

    def test_serialization_preserves_provenance_status_and_actions(self):
        result = market.MarketSignalTriangulationEngine.evaluate(
            [fresh_meta(self.now), fresh_marketplace(self.now)],
            market.DecisionStage.PRE_TEST_RESEARCH,
            now=self.now,
        )

        serialized = result.to_dict()

        self.assertEqual(serialized["decision"], "HOLD_FOR_RESEARCH")
        self.assertEqual(serialized["stage"], "pre_test_research")
        self.assertEqual(
            serialized["evidence_snapshot"][0]["collected_at"],
            self.now.isoformat(),
        )
        self.assertEqual(serialized["evidence_snapshot"][0]["evaluated_status"], "FRESH")
        self.assertTrue(serialized["required_actions"])

    def test_conflicting_signal_directions_are_reported_not_averaged(self):
        negative_meta = replace(
            fresh_meta(self.now),
            metrics={"active_ads_observed": 12, "signal_direction": "negative"},
        )
        result = market.MarketSignalTriangulationEngine.evaluate(
            [fresh_trends(self.now), negative_meta, fresh_marketplace(self.now)],
            market.DecisionStage.PRE_TEST_RESEARCH,
            now=self.now,
        )

        self.assertEqual(result.decision, market.GateDecision.PASS)
        self.assertTrue(result.contradictions)
        self.assertNotIn("composite_score", result.to_dict())


if __name__ == "__main__":
    unittest.main()
