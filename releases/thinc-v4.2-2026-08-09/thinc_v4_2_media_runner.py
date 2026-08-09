# -*- coding: utf-8 -*-
"""Run THINC v4.2 Media Test Protocol from a JSON input file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Mapping

from THINC_v4_2_Media_Test_Protocol_Master_Framework import (
    DecisionStage,
    EvidenceMode,
    MediaEconomicsInput,
    MediaTestConfig,
    MediaTestProtocolEngine,
    SalesChannel,
    TestBudgetMode,
)
from thinc_v4_2_market_signals import FileEvidenceProvider
from thinc_v4_2_niche_validation import (
    NicheFeedbackEngine,
    NicheValidationEngine,
)


def _enum_value(enum_cls, raw: str):
    value = str(raw).strip().lower()
    for item in enum_cls:
        if value in {str(item.value).lower(), item.name.lower()}:
            return item
    allowed = ", ".join(str(item.value) for item in enum_cls)
    raise ValueError(f"Invalid {enum_cls.__name__}: {raw!r}. Allowed: {allowed}")


def load_payload(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("The input JSON must contain one object.")
    return payload


def build_report(payload: Dict[str, Any]) -> Dict[str, Any]:
    economics_data = dict(payload.get("economics", {}))
    config_data = dict(payload.get("config", {}))
    if not economics_data or not config_data:
        raise ValueError("Input must contain both 'economics' and 'config' objects.")

    config_data["sales_channel"] = _enum_value(
        SalesChannel, config_data.get("sales_channel", "website")
    )
    config_data["budget_mode"] = _enum_value(
        TestBudgetMode, config_data.get("budget_mode", "Controlled ABO")
    )
    config_data["evidence_mode"] = _enum_value(
        EvidenceMode, config_data.get("evidence_mode", "standard")
    )
    config_data["decision_stage"] = _enum_value(
        DecisionStage,
        config_data.get("decision_stage", "pre_test_research"),
    )

    market_evidence_data = payload.get("market_evidence", [])
    if market_evidence_data is None:
        market_evidence_data = []
    if not isinstance(market_evidence_data, list):
        raise ValueError("'market_evidence' must be an array of evidence objects.")
    market_evidence = FileEvidenceProvider.ingest(market_evidence_data)

    economics = MediaEconomicsInput(**economics_data)
    config = MediaTestConfig(**config_data)
    report = MediaTestProtocolEngine.build(
        economics,
        config,
        market_evidence=market_evidence,
    ).to_dict()

    media_protocol_decision = str(report["decision"])
    report["media_protocol_decision"] = media_protocol_decision
    niche_payload = payload.get("niche_validation")
    if not isinstance(niche_payload, Mapping):
        report["decision"] = "INCOMPLETE"
        report["analysis_status"] = "INCOMPLETE"
        report["niche_validation"] = None
        report["niche_feedback"] = None
        report["completeness_gate"] = {
            "status": "INCOMPLETE",
            "missing_components": ["niche_validation"],
        }
        report["decision_reasons"] = list(report.get("decision_reasons", [])) + [
            "Overall THINC analysis is incomplete because niche_validation is missing."
        ]
        return report

    market_signal_pass = (
        report.get("market_signal_gate", {}).get("decision") == "PASS"
    )
    niche_report = NicheValidationEngine.evaluate(
        niche_payload,
        market_signal_pass=market_signal_pass,
    ).to_dict()
    completeness = dict(niche_report["completeness_gate"])
    report["niche_validation"] = niche_report
    report["completeness_gate"] = completeness
    report["analysis_status"] = completeness["status"]

    feedback_payload = payload.get("niche_feedback")
    report["niche_feedback"] = (
        NicheFeedbackEngine.evaluate(feedback_payload).to_dict()
        if isinstance(feedback_payload, Mapping)
        else None
    )

    if completeness["status"] != "COMPLETE":
        report["decision"] = "INCOMPLETE"
    elif niche_report["launch_gate"] == "NO_LAUNCH_BEFORE_MODIFICATION":
        report["decision"] = "NO_LAUNCH_BEFORE_MODIFICATION"
    elif media_protocol_decision != "PASS":
        report["decision"] = media_protocol_decision
    else:
        report["decision"] = niche_report["strategic_decision"]

    report["decision_reasons"] = list(report.get("decision_reasons", [])) + list(
        niche_report["required_actions"]
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Path to the JSON input file")
    parser.add_argument("--output", type=Path, default=None, help="Optional output JSON path")
    args = parser.parse_args()

    try:
        report = build_report(load_payload(args.input))
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        parser.error(str(exc))
        return 2

    rendered = json.dumps(report, ensure_ascii=False, indent=2, default=str)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"Saved: {args.output}")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
