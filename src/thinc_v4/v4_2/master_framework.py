# -*- coding: utf-8 -*-
"""THINC™ v4.2 — Adaptive Commerce Intelligence & Venture Building System.

نظام طه المتكيف للذكاء التجاري وبناء المشاريع

THINC™ v4.2 — Invented by Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 الدكتور إيهاب طه — EgyPioneers / Egy-Pioneers Academy.

This module is the **stable facade** of the v4.2 layer. Since 4.2.0 the engine
is split into focused modules; this file only re-exports them and hosts the CLI,
so existing imports (`from thinc_v4.v4_2.master_framework import ...`) keep
working unchanged.

Module map:

| Module | Responsibility |
|---|---|
| `identity` | framework identity, watermark, identity hash |
| `theories` | scientific theory registry |
| `egyptianization` | generational language & dialect engine |
| `business` / `competitive` / `category` / `founder` | strategy layers |
| `ai_layer` / `academy` | AI operating layer, academy OS |
| `composite` | THINC v4 composite scoring engine |
| `creative_models` / `media_models` | value objects |
| `creative_engines` | deconstruction, angles, montage, experiments, winners |
| `media_protocol` | media test protocol engine (economics, stages, stop-loss, scale) |
| `reporting` | orchestration and report assembly |
| `research` | auto-update research layer (safe stubs) |
| `examples` | reference examples |
| `selftest` | the v4.2 self-test suite and console summary |
| `market_signals` / `niche_validation` / `governance` | evidence gate, niche governance |
| `_v3_compat` | optional bridge to THINC v3.1 |

Run the self-tests:
    python -m thinc_v4.v4_2.master_framework --test

Run an example:
    python -m thinc_v4.v4_2.master_framework --example
"""
from __future__ import annotations

import json
import sys

from ._v3_compat import (
    APP_DIR,
    LEGACY_DIR,
    PACKAGE_DIR,
    REPO_ROOT,
    V3,
    V3_IMPORT_ERROR,
    _V3_IMPORT_ERROR,
    v3_available,
)
from .academy import AcademyOperatingSystem
from .ai_layer import AIOperatingLayer, AIToolSpec, AITaskType
from .business import BusinessArchitecture
from .category import CategoryDesign
from .competitive import CompetitiveIntelligence, CompetitorProfile
from .composite import THINCV4Engine, THINCV4ProjectInput, THINCV4Report
from .creative_engines import (
    ControlledCreativeExperimentEngine,
    CreativeAngleIntelligenceEngine,
    CreativeWinnerElectionEngine,
    MontageStrategyEngine,
    ProductDeconstructionEngine,
)
from .creative_models import (
    AdvertisingAngle,
    AngleArchetype,
    BenefitType,
    CreativeBlueprint,
    CreativeFormat,
    CreativePerformance,
    CreativeVariant,
    EgyptianConsumerPersona,
    ExperimentVariable,
    ProductFeature,
    ProductIntelligenceInput,
    ProductProblem,
    StoryboardBeat,
    WinnerDecision,
)
from .egyptianization import (
    AudienceSkillLevel,
    EgyptianAudienceGeneration,
    EgyptianizationEngine,
    EgyptianLanguageProfile,
)
from .examples import (
    example_academy_project,
    example_creative_product,
    example_media_protocol,
)
from .founder import FounderOS
from .identity import (
    ACADEMY_NAME,
    AUTHOR_NAME_AR,
    AUTHOR_NAME_EN,
    COPYRIGHT_YEAR,
    FRAMEWORK_FULL_NAME,
    FRAMEWORK_NAME,
    FRAMEWORK_VERSION,
    PROGRAM_POSITIONING,
    TRADEMARK_HOLDER,
    compute_identity_hash,
    enforce_watermark,
    get_watermark,
    verify_attribution,
)
from .market_signals import (
    AutomatedProvider,
    CollectionMethod,
    DecisionStage,
    EvidenceStatus as MarketEvidenceStatus,
    GateDecision,
    MarketSignalEvidence,
    MarketSignalGateResult,
    MarketSignalSource,
    MarketSignalTriangulationEngine,
)
from .media_models import (
    CampaignObjectivePlan,
    EvidenceMode,
    MediaEconomicsInput,
    MediaEconomicsResult,
    MediaTestConfig,
    MediaTestProtocolReport,
    MediaTestStagePlan,
    SalesChannel,
    ScalePolicy,
    StopLossPolicy,
    TestBudgetMode,
)
from .media_protocol import MediaTestProtocolEngine
from .reporting import CreativeIntelligenceReport, THINCCreativeIntelligenceLayer
from .research import AutoUpdateResearchLayer, ResearchSourceSpec
from .selftest import print_summary, run_all_tests
from .theories import (
    EvidenceLevel,
    ScientificTheory,
    ScientificTheoryRegistry,
    TheoryDomain,
    UpdateCadence,
)

__all__ = [
    # identity
    "ACADEMY_NAME",
    "AUTHOR_NAME_AR",
    "AUTHOR_NAME_EN",
    "COPYRIGHT_YEAR",
    "FRAMEWORK_FULL_NAME",
    "FRAMEWORK_NAME",
    "FRAMEWORK_VERSION",
    "PROGRAM_POSITIONING",
    "TRADEMARK_HOLDER",
    "compute_identity_hash",
    "enforce_watermark",
    "get_watermark",
    "verify_attribution",
    # v3 bridge
    "APP_DIR",
    "LEGACY_DIR",
    "PACKAGE_DIR",
    "REPO_ROOT",
    "V3",
    "V3_IMPORT_ERROR",
    "_V3_IMPORT_ERROR",
    "v3_available",
    # theories
    "EvidenceLevel",
    "ScientificTheory",
    "ScientificTheoryRegistry",
    "TheoryDomain",
    "UpdateCadence",
    # egyptianization
    "AudienceSkillLevel",
    "EgyptianAudienceGeneration",
    "EgyptianLanguageProfile",
    "EgyptianizationEngine",
    # strategy layers
    "AcademyOperatingSystem",
    "AIOperatingLayer",
    "AITaskType",
    "AIToolSpec",
    "BusinessArchitecture",
    "CategoryDesign",
    "CompetitiveIntelligence",
    "CompetitorProfile",
    "FounderOS",
    # composite engine
    "THINCV4Engine",
    "THINCV4ProjectInput",
    "THINCV4Report",
    # creative
    "AdvertisingAngle",
    "AngleArchetype",
    "BenefitType",
    "ControlledCreativeExperimentEngine",
    "CreativeAngleIntelligenceEngine",
    "CreativeBlueprint",
    "CreativeFormat",
    "CreativeIntelligenceReport",
    "CreativePerformance",
    "CreativeVariant",
    "CreativeWinnerElectionEngine",
    "EgyptianConsumerPersona",
    "ExperimentVariable",
    "MontageStrategyEngine",
    "ProductDeconstructionEngine",
    "ProductFeature",
    "ProductIntelligenceInput",
    "ProductProblem",
    "StoryboardBeat",
    "THINCCreativeIntelligenceLayer",
    "WinnerDecision",
    # media
    "CampaignObjectivePlan",
    "EvidenceMode",
    "MediaEconomicsInput",
    "MediaEconomicsResult",
    "MediaTestConfig",
    "MediaTestProtocolEngine",
    "MediaTestProtocolReport",
    "MediaTestStagePlan",
    "SalesChannel",
    "ScalePolicy",
    "StopLossPolicy",
    "TestBudgetMode",
    # market signals
    "AutomatedProvider",
    "CollectionMethod",
    "DecisionStage",
    "GateDecision",
    "MarketEvidenceStatus",
    "MarketSignalEvidence",
    "MarketSignalGateResult",
    "MarketSignalSource",
    "MarketSignalTriangulationEngine",
    # research + examples
    "AutoUpdateResearchLayer",
    "ResearchSourceSpec",
    "example_academy_project",
    "example_creative_product",
    "example_media_protocol",
    "print_summary",
    "run_all_tests",
]


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for the v4.2 layer."""

    args = list(sys.argv[1:] if argv is None else argv)
    if "--test" in args:
        results = run_all_tests()
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 1 if results["failed"] else 0
    if "--example" in args:
        print(json.dumps(example_academy_project().to_dict(), ensure_ascii=False, indent=2))
        print(get_watermark())
        return 0
    if "--creative-example" in args:
        print(json.dumps(example_creative_product().to_dict(), ensure_ascii=False, indent=2, default=str))
        print(get_watermark())
        return 0
    if "--media-example" in args:
        print(json.dumps(example_media_protocol().to_dict(), ensure_ascii=False, indent=2, default=str))
        print(get_watermark())
        return 0
    if "--export-theories" in args:
        out = ScientificTheoryRegistry.export_csv(REPO_ROOT / "thinc_v4_theory_registry.csv")
        print(f"Exported: {out}")
        return 0
    print_summary()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
