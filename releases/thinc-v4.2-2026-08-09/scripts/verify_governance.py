#!/usr/bin/env python3
"""Derive THINC v4.2 governance coverage from the source CSV files."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Dict, List


def _read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_coverage_report(registry_path: Path, traceability_path: Path) -> Dict[str, object]:
    registry_rows = _read_rows(registry_path)
    trace_rows = _read_rows(traceability_path)
    registry_ids = {row["id"] for row in registry_rows}
    trace_ids = {row["requirement_id"] for row in trace_rows}
    missing_tests = sorted(
        row["requirement_id"]
        for row in trace_rows
        if not row.get("behavioral_test", "").strip()
    )
    hidden_outputs = sorted(
        row["requirement_id"]
        for row in trace_rows
        if not row.get("report_output", "").strip()
    )
    return {
        "total_requirements": len(registry_rows),
        "registry_state_counts": dict(
            sorted(Counter(row["state"] for row in registry_rows).items())
        ),
        "traceability_status_counts": dict(
            sorted(Counter(row["current_status"] for row in trace_rows).items())
        ),
        "missing_traceability_ids": sorted(registry_ids - trace_ids),
        "unknown_traceability_ids": sorted(trace_ids - registry_ids),
        "requirements_without_tests": missing_tests,
        "requirements_hidden_from_reports": hidden_outputs,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry", type=Path)
    parser.add_argument("traceability", type=Path)
    args = parser.parse_args()
    print(
        json.dumps(
            build_coverage_report(args.registry, args.traceability),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

