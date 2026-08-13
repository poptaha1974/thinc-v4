from __future__ import annotations

import csv
import unittest
from collections import Counter
from pathlib import Path

from thinc_v4.v4_2.governance import build_coverage_report


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "docs/governance/THINC_v4_2_Approved_Decisions_Registry_2026-08-09.csv"
TRACEABILITY = ROOT / "docs/governance/THINC_v4_2_Requirements_Traceability_Matrix_2026-08-09.csv"


def read_rows(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class GovernanceTests(unittest.TestCase):
    def test_registry_ids_are_unique(self):
        ids = [row["id"] for row in read_rows(REGISTRY)]
        self.assertEqual(len(ids), len(set(ids)))

    def test_all_registry_ids_have_traceability_rows(self):
        registry_ids = {row["id"] for row in read_rows(REGISTRY)}
        trace_ids = {row["requirement_id"] for row in read_rows(TRACEABILITY)}
        self.assertEqual(registry_ids, trace_ids)

    def test_registry_uses_only_allowed_states(self):
        allowed = {
            "IMPLEMENTED",
            "PENDING_IMPLEMENTATION",
            "PENDING_CONFIRMATION",
            "EXPLICITLY_EXCLUDED",
            "SUPERSEDED",
        }
        states = Counter(row["state"] for row in read_rows(REGISTRY))
        self.assertTrue(states)
        self.assertFalse(set(states) - allowed)

    def test_coverage_counts_derive_from_registry(self):
        report = build_coverage_report(REGISTRY, TRACEABILITY)
        rows = read_rows(REGISTRY)

        self.assertEqual(report["total_requirements"], len(rows))
        self.assertEqual(
            sum(report["registry_state_counts"].values()),
            len(rows),
        )
        self.assertEqual(report["missing_traceability_ids"], [])


if __name__ == "__main__":
    unittest.main()
