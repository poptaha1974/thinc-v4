#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-off refactor helper: split the v4.2 master framework into modules.

Kept in the repository for auditability of the 4.2.0 modularization.
It is not part of the runtime package.
"""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src/thinc_v4/v4_2"
SOURCE = SRC / "master_framework.py"

# name -> target module (relative to src/thinc_v4/v4_2)
MODULE_MAP: dict[str, str] = {
    # identity
    "FRAMEWORK_NAME": "identity",
    "FRAMEWORK_VERSION": "identity",
    "FRAMEWORK_FULL_NAME": "identity",
    "AUTHOR_NAME_AR": "identity",
    "AUTHOR_NAME_EN": "identity",
    "TRADEMARK_HOLDER": "identity",
    "COPYRIGHT_YEAR": "identity",
    "PROGRAM_POSITIONING": "identity",
    "ACADEMY_NAME": "identity",
    "compute_identity_hash": "identity",
    "verify_attribution": "identity",
    "get_watermark": "identity",
    "enforce_watermark": "identity",
    # theories
    "TheoryDomain": "theories",
    "EvidenceLevel": "theories",
    "UpdateCadence": "theories",
    "ScientificTheory": "theories",
    "ScientificTheoryRegistry": "theories",
    # egyptianization
    "EgyptianAudienceGeneration": "egyptianization",
    "AudienceSkillLevel": "egyptianization",
    "EgyptianLanguageProfile": "egyptianization",
    "EgyptianizationEngine": "egyptianization",
    # business layers
    "BusinessArchitecture": "business",
    "CompetitorProfile": "competitive",
    "CompetitiveIntelligence": "competitive",
    "CategoryDesign": "category",
    "FounderOS": "founder",
    "AITaskType": "ai_layer",
    "AIToolSpec": "ai_layer",
    "AIOperatingLayer": "ai_layer",
    "AcademyOperatingSystem": "academy",
    # composite engine
    "THINCV4ProjectInput": "composite",
    "THINCV4Report": "composite",
    "THINCV4Engine": "composite",
    # creative models
    "BenefitType": "creative_models",
    "AngleArchetype": "creative_models",
    "CreativeFormat": "creative_models",
    "ExperimentVariable": "creative_models",
    "ProductFeature": "creative_models",
    "ProductProblem": "creative_models",
    "EgyptianConsumerPersona": "creative_models",
    "ProductIntelligenceInput": "creative_models",
    "AdvertisingAngle": "creative_models",
    "StoryboardBeat": "creative_models",
    "CreativeBlueprint": "creative_models",
    "CreativeVariant": "creative_models",
    "CreativePerformance": "creative_models",
    "WinnerDecision": "creative_models",
    # media models
    "SalesChannel": "media_models",
    "TestBudgetMode": "media_models",
    "EvidenceMode": "media_models",
    "MediaEconomicsInput": "media_models",
    "MediaTestConfig": "media_models",
    "CampaignObjectivePlan": "media_models",
    "MediaEconomicsResult": "media_models",
    "MediaTestStagePlan": "media_models",
    "StopLossPolicy": "media_models",
    "ScalePolicy": "media_models",
    "MediaTestProtocolReport": "media_models",
    # engines
    "ProductDeconstructionEngine": "creative_engines",
    "CreativeAngleIntelligenceEngine": "creative_engines",
    "MontageStrategyEngine": "creative_engines",
    "ControlledCreativeExperimentEngine": "creative_engines",
    "CreativeWinnerElectionEngine": "creative_engines",
    "MediaTestProtocolEngine": "media_protocol",
    # reporting + research
    "CreativeIntelligenceReport": "reporting",
    "THINCCreativeIntelligenceLayer": "reporting",
    "ResearchSourceSpec": "research",
    "AutoUpdateResearchLayer": "research",
    # examples / self-tests
    "example_academy_project": "examples",
    "example_creative_product": "examples",
    "example_media_protocol": "examples",
    "run_all_tests": "examples",
    "print_summary": "examples",
}

# emission order (also the dependency order)
MODULE_ORDER = [
    "identity",
    "theories",
    "egyptianization",
    "business",
    "competitive",
    "category",
    "founder",
    "ai_layer",
    "academy",
    "composite",
    "creative_models",
    "media_models",
    "creative_engines",
    "media_protocol",
    "reporting",
    "research",
    "examples",
]

MODULE_DOCSTRINGS = {
    "identity": "Identity, versioning, and watermark protection for the THINC v4.2 layer.",
    "theories": "Scientific theory registry for the THINC v4.2 layer.",
    "egyptianization": "Egyptianization and generational language engine.",
    "business": "Business architecture layer.",
    "competitive": "Competitive intelligence layer.",
    "category": "Category design layer.",
    "founder": "Founder OS layer.",
    "ai_layer": "AI operating layer.",
    "academy": "Academy operating system layer.",
    "composite": "THINC v4 composite scoring engine.",
    "creative_models": "Creative intelligence value objects (enums and dataclasses).",
    "media_models": "Media economics and media test protocol value objects.",
    "creative_engines": "Creative intelligence engines: deconstruction, angles, montage, experiments, winners.",
    "media_protocol": "Media test protocol engine: economics guardrails, stages, stop-loss, and scale policy.",
    "reporting": "Creative intelligence orchestration and report assembly.",
    "research": "Auto-update research layer (safe stubs, no silent model changes).",
    "examples": "Reference examples and the v4.2 self-test suite.",
}

STDLIB_PREAMBLE = """import csv
import hashlib
import json
import math
import os
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
"""

MARKET_SIGNAL_NAMES = [
    "AutomatedProvider",
    "CollectionMethod",
    "DecisionStage",
    "MarketEvidenceStatus",
    "GateDecision",
    "MarketSignalEvidence",
    "MarketSignalGateResult",
    "MarketSignalSource",
    "MarketSignalTriangulationEngine",
]
V3_NAMES = ["V3", "V3_IMPORT_ERROR", "_V3_IMPORT_ERROR", "v3_available"]
PATH_NAMES = ["APP_DIR", "PACKAGE_DIR", "REPO_ROOT", "LEGACY_DIR"]


def segments(source: str) -> list[tuple[str, str]]:
    """Return `(name, source_segment)` for every mapped top-level definition."""

    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    out: list[tuple[str, str]] = []
    for node in tree.body:
        names: list[str] = []
        if isinstance(node, ast.ClassDef | ast.FunctionDef):
            names = [node.name]
        elif isinstance(node, ast.Assign):
            names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names = [node.target.id]
        mapped = [n for n in names if n in MODULE_MAP]
        if not mapped:
            continue
        start = min([node.lineno] + [d.lineno for d in getattr(node, "decorator_list", [])]) - 1
        # pull in the contiguous comment block directly above the definition
        while start - 1 >= 0 and lines[start - 1].lstrip().startswith("#") and "===" not in lines[start - 1]:
            start -= 1
        end = node.end_lineno or node.lineno
        out.append((mapped[0], "".join(lines[start:end])))
    return out


def main() -> int:
    source = SOURCE.read_text(encoding="utf-8")
    blocks = segments(source)
    found = {name for name, _ in blocks}
    missing = sorted(set(MODULE_MAP) - found)
    if missing:
        print(f"ERROR: unmapped/not-found top-level names: {missing}", file=sys.stderr)
        return 1

    bodies: dict[str, list[str]] = {module: [] for module in MODULE_ORDER}
    for name, text in blocks:
        bodies[MODULE_MAP[name]].append(text.rstrip("\n"))

    defined_in: dict[str, str] = dict(MODULE_MAP)
    module_index = {module: i for i, module in enumerate(MODULE_ORDER)}

    for module in MODULE_ORDER:
        body = "\n\n\n".join(bodies[module]) + "\n"
        tokens = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", body))
        imports: dict[str, list[str]] = {}
        for token in sorted(tokens):
            origin = defined_in.get(token)
            if origin is None or origin == module:
                continue
            if module_index[origin] > module_index[module]:
                print(f"ERROR: forward dependency {module} -> {origin} ({token})", file=sys.stderr)
                return 1
            imports.setdefault(f".{origin}", []).append(token)
        for token in sorted(tokens & set(MARKET_SIGNAL_NAMES)):
            imports.setdefault(".market_signals", []).append(token)
        for token in sorted(tokens & set(V3_NAMES)):
            imports.setdefault("._v3_compat", []).append(token)
        for token in sorted(tokens & set(PATH_NAMES)):
            imports.setdefault("._v3_compat", []).append(token)

        header = [
            "# -*- coding: utf-8 -*-",
            f'"""{MODULE_DOCSTRINGS[module]}',
            "",
            "THINC™ v4.2 — Invented by Dr. Ehab Taha (الدكتور إيهاب طه).",
            "© 2026 Dr. Ehab Taha — Egy-Pioneers Academy.",
            '"""',
            "from __future__ import annotations",
            "",
            STDLIB_PREAMBLE.rstrip("\n"),
        ]
        for target in sorted(imports):
            names = sorted(set(imports[target]))
            if target == ".market_signals":
                names = [
                    "EvidenceStatus as MarketEvidenceStatus" if n == "MarketEvidenceStatus" else n
                    for n in names
                ]
            if len(names) == 1:
                header.append(f"from {target} import {names[0]}")
            else:
                header.append(f"from {target} import (")
                header.extend(f"    {n}," for n in names)
                header.append(")")
        text = "\n".join(header) + "\n\n\n" + body
        (SRC / f"{module}.py").write_text(text, encoding="utf-8")
        print(f"wrote {module}.py ({len(body.splitlines())} body lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
