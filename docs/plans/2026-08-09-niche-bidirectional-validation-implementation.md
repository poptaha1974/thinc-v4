# THINC v4.2 Niche Bidirectional Validation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Niche Family Tree, reverse validation, convergence, launch veto, post-test niche feedback, and completeness governance executable and auditable in THINC v4.2.

**Architecture:** Add a focused `thinc_v4_2_niche_validation.py` domain module and compose it in the existing JSON media runner. Keep market evidence and media economics as independent component gates, then calculate the overall THINC decision through a completeness-aware orchestrator.

**Tech Stack:** Python 3.11+, `dataclasses`, `enum`, `unittest`, JSON, Markdown, CSV.

## Global Constraints

- Preserve Dr. Ehab Taha's THINC attribution and Egy-Pioneers Academy ownership.
- Never use a component `PASS` as the overall decision.
- Never invent missing market, customer, supplier, authenticity, or economics evidence.
- Keep `Baby Organizer Bag` as a temporary example only and out of defaults.
- Use test-first red/green cycles for production behavior.

---

### Task 1: Approved Decisions Registry and Traceability Matrix

**Files:**
- Create: `docs/governance/THINC_v4_2_Approved_Decisions_Registry_2026-08-09.csv`
- Create: `docs/governance/THINC_v4_2_Requirements_Traceability_Matrix_2026-08-09.csv`
- Create: `docs/governance/THINC_v4_2_Conversation_Inventory_2026-08-09.md`

**Interfaces:**
- Consumes: the approved conversation design and current THINC/PRA/market-signal artifacts.
- Produces: stable `NFT-*`, `GOV-*`, and `MS-*` requirement IDs used by tests, reports, the skill, Notion, and GitHub.

- [ ] Extract accepted, pending-confirmation, and explicitly excluded decisions.
- [ ] Record code/test/report mappings without marking planned behavior as implemented.
- [ ] Count each status from the CSV itself and include the counts in the inventory.

### Task 2: Niche validation domain tests — RED

**Files:**
- Create: `tests/test_niche_validation.py`

**Interfaces:**
- Consumes: the intended API below.
- Produces: executable behavioral requirements for `NicheValidationEngine.evaluate` and `NicheFeedbackEngine.evaluate`.

- [ ] Write failing tests importing:

```python
from thinc_v4_2_niche_validation import (
    NicheFeedbackEngine,
    NicheValidationEngine,
)
```

- [ ] Cover `REJECT`, `REPOSITION`, `REFINE_OFFER`, `ACCEPT_AND_TEST`, missing-field `INCOMPLETE`, economics veto, and one-micro-niche failure preservation.
- [ ] Run `python -m unittest tests.test_niche_validation -v` and verify failure is caused by the missing module.

### Task 3: Niche validation domain implementation — GREEN

**Files:**
- Create: `thinc_v4_2_niche_validation.py`

**Interfaces:**
- Consumes: plain dictionaries for portability through JSON.
- Produces: `NicheValidationReport.to_dict()` and `NicheFeedbackReport.to_dict()`.

- [ ] Define enums for strategic decisions, launch gates, completeness, and feedback actions.
- [ ] Define required discovery fields: `market`, `niche`, `micro_niche`, `persona`, `problem_jtbd`, `product`.
- [ ] Implement deterministic precedence from the approved design.
- [ ] Implement feedback logic where a single failed micro-niche cannot reject the parent niche.
- [ ] Run the domain tests and verify all pass.

### Task 4: Runner integration tests — RED

**Files:**
- Modify: `tests/test_market_signal_integration.py`

**Interfaces:**
- Consumes: `build_report(payload)` with optional `niche_validation` and `niche_feedback` objects.
- Produces: top-level `decision`, `analysis_status`, `niche_validation`, and `completeness_gate`.

- [ ] Change the fresh-market-only expectation from top-level `PASS` to `INCOMPLETE` while keeping `market_signal_gate.decision == "PASS"`.
- [ ] Add a complete aligned payload that returns `ACCEPT_AND_TEST`.
- [ ] Add a complete economics-failed payload that returns `NO_LAUNCH_BEFORE_MODIFICATION`.
- [ ] Run the focused integration tests and verify they fail against the existing runner.

### Task 5: Runner orchestration — GREEN

**Files:**
- Modify: `thinc_v4_2_media_runner.py`

**Interfaces:**
- Consumes: `economics`, `config`, `market_evidence`, `niche_validation`, and optional `niche_feedback`.
- Produces: component market/media report plus overall completeness-aware decision.

- [ ] Evaluate the niche input after calculating existing media economics.
- [ ] Preserve existing media component decision as `media_protocol_decision`.
- [ ] Serialize `niche_validation`, `niche_feedback`, and `completeness_gate`.
- [ ] Apply overall decision precedence without hiding component results.
- [ ] Run domain and integration tests until green.

### Task 6: Karseell reference case and documentation

**Files:**
- Modify: `Karseell_THINC_v4_2_input_2026-08-09.json`
- Regenerate: `Karseell_THINC_v4_2_engine_output_2026-08-09.json`
- Modify: `THINC_v4_2_QUICKSTART.md`
- Modify: `THINC_v4_2_CHANGELOG.md`
- Modify: `Karseell_THINC_v4_2_Analysis_2026-08-09.md`

**Interfaces:**
- Consumes: documented Karseell evidence from 2026-08-09.
- Produces: an auditable case with market `PASS`, strategic `REFINE_OFFER`, and launch `NO_LAUNCH_BEFORE_MODIFICATION`.

- [ ] Add explicit Karseell discovery and reverse paths.
- [ ] Mark supplier cost and authenticity as unresolved critical evidence.
- [ ] Regenerate output through the runner rather than hand-writing it.
- [ ] Update prose to distinguish component and overall decisions.

### Task 7: Personal THINC v4.2 skill

**Files:**
- Create in personal skills checkout: `thinc-v4-2/SKILL.md`
- Create: `thinc-v4-2/agents/openai.yaml`
- Create: `thinc-v4-2/references/approved-decisions.md`
- Create: `thinc-v4-2/references/analysis-contract.md`
- Create: `thinc-v4-2/references/feedback-and-governance.md`

**Interfaces:**
- Consumes: the implementation and governance artifacts.
- Produces: an installed skill that requires bidirectional validation and completeness evidence before full-analysis claims.

- [ ] Initialize with the official skill creator.
- [ ] Keep `SKILL.md` procedural and move detailed rules to references.
- [ ] Validate using `quick_validate.py` against the personal skills checkout.
- [ ] Save and verify the exact remote skill path.

### Task 8: GitHub and Notion publication

**Files:**
- GitHub: add the dated v4.2 governance, domain module, tests, examples, and docs on `agent/thinc-v4-2-niche-governance-2026-08-09`.
- Notion: create a dated THINC v4.2 page under the main THINC documentation; create a Decisions Log entry; add the skill to the Skills Library.

**Interfaces:**
- Consumes: locally verified artifacts and test counts.
- Produces: a draft PR and linked Notion records.

- [ ] Create a GitHub branch from `main` and commit only the scoped v4.2 files.
- [ ] Open a draft PR with verification evidence and known limitations.
- [ ] Create the Notion documentation page and decision record using the exact database schema.
- [ ] Update the Skills Library with a link to the created page.

### Task 9: Final verification

**Files:**
- All changed files.

**Interfaces:**
- Consumes: final working tree, skill checkout, GitHub PR, and Notion records.
- Produces: evidence-backed completion report.

- [ ] Run all existing v4.2 behavioral and integration tests plus new niche tests.
- [ ] Validate JSON outputs and CSV counts.
- [ ] Search for forbidden generic top-level `PASS` in incomplete examples.
- [ ] Fetch the GitHub PR and Notion pages to verify persistence.
- [ ] Report exact counts, links, pending confirmations, and non-implemented automation limits.

