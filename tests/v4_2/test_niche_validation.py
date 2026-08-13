from __future__ import annotations

import unittest

from thinc_v4.v4_2.niche_validation import (
    NicheFeedbackEngine,
    NicheValidationEngine,
)


def aligned_input(**overrides):
    payload = {
        "discovery_path": {
            "market": "Beauty & Personal Care",
            "niche": "Hair Care",
            "micro_niche": "Egyptian women seeking home care for dry and frizzy hair",
            "persona": "Trust-sensitive Egyptian woman buying hair care online",
            "problem_jtbd": "Improve softness and appearance while avoiding counterfeit products",
            "product": "Karseell Collagen Hair Mask 500ml",
        },
        "reverse_validation_path": {
            "product": "Karseell Collagen Hair Mask 500ml",
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


class NicheValidationTests(unittest.TestCase):
    def test_rejects_when_product_does_not_solve_problem(self):
        report = NicheValidationEngine.evaluate(
            aligned_input(product_solves_problem=False),
            market_signal_pass=True,
        ).to_dict()

        self.assertEqual(report["strategic_decision"], "REJECT")
        self.assertEqual(report["launch_gate"], "NO_LAUNCH_BEFORE_MODIFICATION")

    def test_repositions_when_actual_persona_differs(self):
        report = NicheValidationEngine.evaluate(
            aligned_input(persona_matches_problem=False),
            market_signal_pass=True,
        ).to_dict()

        self.assertEqual(report["strategic_decision"], "REPOSITION")

    def test_refines_offer_when_offer_is_weak(self):
        report = NicheValidationEngine.evaluate(
            aligned_input(offer_strength="weak"),
            market_signal_pass=True,
        ).to_dict()

        self.assertEqual(report["strategic_decision"], "REFINE_OFFER")
        self.assertEqual(report["launch_gate"], "NO_LAUNCH_BEFORE_MODIFICATION")

    def test_accept_and_test_when_both_paths_and_gates_align(self):
        report = NicheValidationEngine.evaluate(
            aligned_input(),
            market_signal_pass=True,
        ).to_dict()

        self.assertEqual(report["completeness_gate"]["status"], "COMPLETE")
        self.assertTrue(report["convergence"]["aligned"])
        self.assertEqual(report["strategic_decision"], "ACCEPT_AND_TEST")
        self.assertEqual(report["launch_gate"], "CONTROLLED_TEST_ALLOWED")

    def test_missing_path_field_is_incomplete(self):
        payload = aligned_input()
        del payload["discovery_path"]["micro_niche"]

        report = NicheValidationEngine.evaluate(
            payload,
            market_signal_pass=True,
        ).to_dict()

        self.assertEqual(report["strategic_decision"], "INCOMPLETE")
        self.assertIn(
            "discovery_path.micro_niche",
            report["completeness_gate"]["missing_components"],
        )

    def test_economics_failure_vetoes_launch(self):
        report = NicheValidationEngine.evaluate(
            aligned_input(economics_viable=False),
            market_signal_pass=True,
        ).to_dict()

        self.assertEqual(report["strategic_decision"], "REFINE_OFFER")
        self.assertEqual(report["launch_gate"], "NO_LAUNCH_BEFORE_MODIFICATION")
        self.assertFalse(report["convergence"]["economics_viable"])

    def test_critical_risk_vetoes_launch(self):
        report = NicheValidationEngine.evaluate(
            aligned_input(critical_risks=["Authenticity is not verified"]),
            market_signal_pass=True,
        ).to_dict()

        self.assertEqual(report["launch_gate"], "NO_LAUNCH_BEFORE_MODIFICATION")
        self.assertIn("Authenticity is not verified", report["critical_risks"])

    def test_no_baby_organizer_default(self):
        rendered = " ".join(NicheValidationEngine.PATH_LEVELS).lower()
        self.assertNotIn("baby organizer", rendered)


class NicheFeedbackTests(unittest.TestCase):
    def test_single_micro_niche_failure_preserves_parent_niche(self):
        report = NicheFeedbackEngine.evaluate(
            {
                "niche": "Hair Care",
                "micro_niche": "Dry and frizzy hair home care",
                "product": "Karseell Mask",
                "product_outcome": "failed",
                "micro_niche_outcome": "failed",
                "tested_micro_niches": 1,
                "tested_solutions": 1,
                "evidence_strength": "strong",
            }
        ).to_dict()

        self.assertEqual(report["parent_niche_decision"], "KEEP")
        self.assertNotEqual(report["action"], "REJECT")

    def test_strong_niche_weak_product_returns_to_opportunity_map(self):
        report = NicheFeedbackEngine.evaluate(
            {
                "niche": "Hair Care",
                "micro_niche": "Dry and frizzy hair home care",
                "product": "Weak SKU",
                "product_outcome": "failed",
                "micro_niche_outcome": "passed",
                "tested_micro_niches": 2,
                "tested_solutions": 1,
                "evidence_strength": "strong",
            }
        ).to_dict()

        self.assertEqual(report["parent_niche_decision"], "KEEP")
        self.assertEqual(report["action"], "PIVOT")
        self.assertIn("Opportunity Map", report["recommended_next_step"])


if __name__ == "__main__":
    unittest.main()

