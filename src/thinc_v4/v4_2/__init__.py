# -*- coding: utf-8 -*-
"""THINC v4.2 layer — Creative Intelligence, Media Testing & Niche Governance.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 Dr. Ehab Taha — Egy-Pioneers Academy.

Public entry points:
- `market_signals` — auditable market-signal evidence gate.
- `niche_validation` — bidirectional niche family-tree validation.
- `master_framework` — the v4.2 engine layer over v4.0 / v3.1.
- `media_runner` — JSON-in / report-out CLI (`thinc-v4-2`).
- `governance` — requirement/traceability coverage checks.
"""
from __future__ import annotations

from .governance import build_coverage_report
from .market_signals import (
    AutomatedProvider,
    CollectionMethod,
    DecisionStage,
    EvidenceStatus,
    FileEvidenceProvider,
    GateDecision,
    MarketSignalEvidence,
    MarketSignalGateResult,
    MarketSignalSource,
    MarketSignalTriangulationEngine,
)
from .niche_validation import (
    LaunchGate,
    NicheFeedbackEngine,
    NicheValidationEngine,
    StrategicDecision,
)

LAYER_VERSION = "4.2"

__all__ = [
    "LAYER_VERSION",
    "AutomatedProvider",
    "CollectionMethod",
    "DecisionStage",
    "EvidenceStatus",
    "FileEvidenceProvider",
    "GateDecision",
    "LaunchGate",
    "MarketSignalEvidence",
    "MarketSignalGateResult",
    "MarketSignalSource",
    "MarketSignalTriangulationEngine",
    "NicheFeedbackEngine",
    "NicheValidationEngine",
    "StrategicDecision",
    "build_coverage_report",
]
