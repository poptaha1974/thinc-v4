# -*- coding: utf-8 -*-
"""Self-test suite and console summary for the THINC v4.2 layer.

THINC™ v4.2 — Invented by Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 Dr. Ehab Taha — Egy-Pioneers Academy.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List
from ._v3_compat import V3
from .academy import AcademyOperatingSystem
from .ai_layer import (
    AIOperatingLayer,
    AITaskType,
)
from .business import BusinessArchitecture
from .category import CategoryDesign
from .creative_engines import CreativeWinnerElectionEngine
from .creative_models import (
    CreativePerformance,
)
from .egyptianization import (
    AudienceSkillLevel,
    EgyptianAudienceGeneration,
    EgyptianizationEngine,
)
from .founder import FounderOS
from .identity import (
    FRAMEWORK_NAME,
    FRAMEWORK_VERSION,
    PROGRAM_POSITIONING,
    compute_identity_hash,
    get_watermark,
    verify_attribution,
)
from .market_signals import (
    AutomatedProvider,
    CollectionMethod,
    DecisionStage,
    GateDecision,
    EvidenceStatus as MarketEvidenceStatus,
    MarketSignalEvidence,
    MarketSignalSource,
    MarketSignalTriangulationEngine,
)
from .research import AutoUpdateResearchLayer
from .theories import (
    ScientificTheoryRegistry,
    TheoryDomain,
)


from .examples import (
    example_academy_project,
    example_creative_product,
    example_media_protocol,
)



def run_all_tests() -> Dict[str, Any]:
    passed: List[str] = []
    failed: List[str] = []

    def check(name: str, condition: bool) -> None:
        (passed if condition else failed).append(name)

    check("identity attribution", verify_attribution())
    check("identity hash length", len(compute_identity_hash()) == 64)
    check("theory count >= 50", ScientificTheoryRegistry.count() >= 50)
    check("has behavioral economics domain", ScientificTheoryRegistry.by_domain().get(TheoryDomain.BEHAVIORAL_ECONOMICS.value, 0) >= 5)

    profile = EgyptianizationEngine.build_profile(EgyptianAudienceGeneration.GEN_Z, AudienceSkillLevel.BEGINNER)
    check("egyptian profile hook", bool(profile.sample_hook))
    check("egyptian profile preferred words", len(profile.preferred_words) >= 5)

    b = BusinessArchitecture()
    check("business architecture readiness", b.readiness_score() >= 8)

    cat = CategoryDesign()
    check("category strength", cat.category_strength() >= 8)

    founder = FounderOS(8, 7, 8, 7, 7, 6)
    check("founder readiness", founder.founder_readiness()["score"] > 6)

    tools = AIOperatingLayer.recommend_stack(AITaskType.CODING)
    check("ai coding stack includes codex", any(t.name == "Codex" for t in tools))

    academy = AcademyOperatingSystem()
    check("academy value stack", academy.value_stack_score() >= 8)

    report = example_academy_project()
    check("example final score", report.final_score > 7)
    check("report theory count", report.theory_count >= 50)

    creative = example_creative_product()
    check("creative feature map", len(creative.feature_value_map) >= 2)
    check("creative problem hierarchy", creative.problem_hierarchy[0]["problem_strength"] >= 8)
    check("creative angles generated", len(creative.ranked_angles) >= 5)
    check("creative angles ranked", creative.ranked_angles[0].total_score >= creative.ranked_angles[-1].total_score)
    check("montage storyboard beats", len(creative.top_blueprint.beats) == 6)
    check("controlled experiment matrix", all(creative.experiment_matrix[k] for k in ["angle_test", "hook_test", "editing_test"]))
    perf = CreativePerformance("A1", 1000, 20000, 8000, 500, 40, 34, 28, 42000, 650, 8.0, 25.0)
    winner = CreativeWinnerElectionEngine.evaluate(perf)
    check("winner uses delivered orders", winner.metrics["delivered_cpa"] > 0)
    check("winner decision generated", winner.decision.startswith(("SCALE", "ITERATE", "FIX", "HOLD", "KILL")))

    media = creative.media_test_protocol
    check("media protocol integrated", media is not None)
    if media is not None:
        check("website objective is sales", media.objective_plan.objective == "Sales")
        check("website optimization is purchase", media.objective_plan.optimization_event == "Purchase")
        check("economics target cpa hierarchy", media.economics.target_purchase_cpa < media.economics.target_confirmed_cpa < media.economics.target_delivered_cpa)
        check("media stages complete", [s.stage for s in media.stages] == ["Angle Test", "Hook Test", "Editing Test", "Offer & CTA Test", "Winner Validation"])
        check("angle duration bounded", 4 <= media.stages[0].recommended_days <= 7)
        check("stop loss protects target cpa", media.stop_loss.hard_stop_spend > media.stop_loss.soft_stop_spend > 0)
        check("scale uses delivered cpa", media.scale_policy.maximum_delivered_cpa == media.economics.target_delivered_cpa)
        check("scale requires delivered orders", media.scale_policy.minimum_delivered_orders >= 5)

    whatsapp = example_media_protocol()
    check("whatsapp fallback objective", whatsapp.objective_plan.objective == "Leads")
    check("whatsapp destination", whatsapp.objective_plan.destination == "WhatsApp")
    check("whatsapp delivered warning", any("delivered" in w.lower() for w in whatsapp.warnings))

    market_now = datetime.now(timezone.utc)

    def market_record(
        source: MarketSignalSource,
        metrics: Dict[str, Any],
        *,
        country: str = "Egypt",
        collected_at: datetime | None = None,
        summary: str = "Documented evidence for an embedded behavioral test.",
    ) -> MarketSignalEvidence:
        return MarketSignalEvidence(
            source=source,
            status=MarketEvidenceStatus.COLLECTED,
            query="embedded test product",
            country=country,
            timeframe="embedded test observation window",
            collected_at=collected_at or market_now,
            collection_method=CollectionMethod.FILE_UPLOAD,
            source_reference=f"embedded-{source.value}.json",
            summary=summary,
            metrics=metrics,
        )

    trends = market_record(
        MarketSignalSource.GOOGLE_TRENDS,
        {"relative_interest_index": 60, "signal_direction": "positive"},
    )
    meta = market_record(
        MarketSignalSource.META_AD_LIBRARY,
        {"active_ads_observed": 4, "signal_direction": "positive"},
    )
    marketplace = market_record(
        MarketSignalSource.MARKETPLACE,
        {"listing_count_observed": 3, "signal_direction": "positive"},
    )
    first_party = market_record(
        MarketSignalSource.FIRST_PARTY_CAMPAIGN,
        {
            "spend": 2400,
            "delivered_orders": 12,
            "delivered_cpa": 200,
            "delivery_rate_pct": 75,
            "delivered_profit": 2400,
            "signal_direction": "positive",
        },
    )

    missing_trends = MarketSignalTriangulationEngine.evaluate(
        [meta, marketplace], DecisionStage.PRE_TEST_RESEARCH, now=market_now
    )
    check(
        "market gate missing trends holds",
        missing_trends.decision is GateDecision.HOLD_FOR_RESEARCH
        and missing_trends.coverage_status_by_source["google_trends"]
        == "NOT_COLLECTED",
    )
    missing_meta = MarketSignalTriangulationEngine.evaluate(
        [trends, marketplace], DecisionStage.PRE_TEST_RESEARCH, now=market_now
    )
    check(
        "market gate missing meta holds",
        missing_meta.decision is GateDecision.HOLD_FOR_RESEARCH,
    )
    stale_marketplace = market_record(
        MarketSignalSource.MARKETPLACE,
        {"listing_count_observed": 3},
        collected_at=market_now - timedelta(days=4),
    )
    stale_gate = MarketSignalTriangulationEngine.evaluate(
        [trends, meta, stale_marketplace],
        DecisionStage.PRE_TEST_RESEARCH,
        now=market_now,
    )
    check(
        "market gate stale evidence holds",
        stale_gate.decision is GateDecision.HOLD_FOR_RESEARCH
        and stale_gate.freshness_status_by_source["marketplace"] == "STALE",
    )
    wrong_country_gate = MarketSignalTriangulationEngine.evaluate(
        [
            market_record(
                MarketSignalSource.GOOGLE_TRENDS,
                {"relative_interest_index": 60},
                country="Saudi Arabia",
            ),
            meta,
            marketplace,
        ],
        DecisionStage.PRE_TEST_RESEARCH,
        now=market_now,
    )
    check(
        "market gate requires Egypt evidence",
        wrong_country_gate.decision is GateDecision.HOLD_FOR_RESEARCH
        and wrong_country_gate.coverage_status_by_source["google_trends"]
        == "WRONG_COUNTRY",
    )
    research_pass = MarketSignalTriangulationEngine.evaluate(
        [trends, meta, marketplace],
        DecisionStage.PRE_TEST_RESEARCH,
        now=market_now,
    )
    check(
        "market gate fresh research passes",
        research_pass.decision is GateDecision.PASS,
    )
    check(
        "campaign evidence not required pretest",
        research_pass.coverage_status_by_source["first_party_campaign"]
        == "NOT_APPLICABLE",
    )
    no_profit = market_record(
        MarketSignalSource.FIRST_PARTY_CAMPAIGN,
        {"delivered_orders": 12},
    )
    scale_no_profit = MarketSignalTriangulationEngine.evaluate(
        [trends, meta, marketplace, no_profit],
        DecisionStage.SCALE,
        now=market_now,
    )
    check(
        "scale gate requires delivered profit",
        scale_no_profit.decision is GateDecision.BLOCK_SCALE,
    )
    scale_pass = MarketSignalTriangulationEngine.evaluate(
        [trends, meta, marketplace, first_party],
        DecisionStage.SCALE,
        now=market_now,
    )
    check("scale evidence gate passes", scale_pass.decision is GateDecision.PASS)
    prior_key = os.environ.get("GOOGLE_TRENDS_KEY")
    os.environ["GOOGLE_TRENDS_KEY"] = "configured-for-test"
    try:
        key_only_gate = MarketSignalTriangulationEngine.evaluate(
            [], DecisionStage.PRE_TEST_RESEARCH, now=market_now
        )
        provider_status = AutomatedProvider.status(
            "GOOGLE_TRENDS_KEY", provider_implemented=False
        )
    finally:
        if prior_key is None:
            os.environ.pop("GOOGLE_TRENDS_KEY", None)
        else:
            os.environ["GOOGLE_TRENDS_KEY"] = prior_key
    check(
        "provider key is not evidence",
        key_only_gate.decision is GateDecision.HOLD_FOR_RESEARCH
        and provider_status["automation_status"] == "AUTOMATED_PROVIDER_PENDING",
    )
    serialized_gate = missing_trends.to_dict()
    check(
        "market gate provenance serializes",
        serialized_gate["decision"] == "HOLD_FOR_RESEARCH"
        and serialized_gate["evidence_snapshot"][0]["source_reference"]
        == "embedded-meta_ad_library.json"
        and bool(serialized_gate["required_actions"]),
    )
    legacy_media = example_media_protocol()
    check(
        "legacy media call returns research hold",
        legacy_media.decision == "HOLD_FOR_RESEARCH"
        and legacy_media.market_signal_gate.decision
        is GateDecision.HOLD_FOR_RESEARCH,
    )

    # Optional v3 tests if v3 import is available
    v3_status = "not_available"
    if V3 is not None:
        try:
            v3 = V3.run_all_tests()
            v3_status = "passed" if v3.get("failed", 1) == 0 else "failed"
            check("v3 tests pass", v3_status == "passed")
        except Exception:
            v3_status = "error"
            check("v3 tests pass", False)

    return {
        "total": len(passed) + len(failed),
        "passed": len(passed),
        "failed": len(failed),
        "failed_names": failed,
        "success_rate": round(len(passed) / max(1, len(passed) + len(failed)) * 100, 1),
        "v3_status": v3_status,
    }


def print_summary() -> None:
    print("=" * 80)
    print(f"{FRAMEWORK_NAME}™ {FRAMEWORK_VERSION}")
    print(PROGRAM_POSITIONING)
    print("=" * 80)
    print(f"Scientific theories loaded: {ScientificTheoryRegistry.count()}")
    print("Theory domains:")
    for domain, count in ScientificTheoryRegistry.by_domain().items():
        print(f"- {domain}: {count}")
    print("\nAuto-update status:")
    print(json.dumps(AutoUpdateResearchLayer.status(), ensure_ascii=False, indent=2))
    print(get_watermark())
