# THINC™ v4.2 Changelog

## Added — Niche Family Tree Bidirectional Validation (2026-08-09)

- Added the discovery path: `Market → Niche → Micro-Niche → Persona → Problem/JTBD → Product`.
- Added reverse validation: `Product → Problem/JTBD → Persona → Micro-Niche → Niche → Market`.
- Added explicit convergence on customer, evidenced problem, suitable solution, and viable economics.
- Added strategic decisions: `REJECT`, `REPOSITION`, `REFINE_OFFER`, and `ACCEPT_AND_TEST`.
- Added an independent launch veto: `NO_LAUNCH_BEFORE_MODIFICATION`.
- Added post-test hypothesis feedback while preventing one failed Micro-Niche or product from rejecting its parent Niche.
- Added a completeness gate so a component `PASS` cannot be serialized as a Full THINC Analysis pass.
- Added a dated Approved Decisions Registry and Requirements Traceability Matrix.
- Preserved `Baby Organizer Bag` as a temporary teaching example only; it is not a model default.

## Added — Market Signal Triangulation Gate

- Added normalized evidence contracts for Google Trends, Meta Ad Library, marketplaces, and first-party campaigns.
- Added browser-assisted and file-ingestion provider boundaries using one auditable schema.
- Added stage gates for `PRE_TEST_RESEARCH`, `CONTROLLED_TEST`, and `SCALE`.
- Missing evidence now becomes `NOT_COLLECTED` and `HOLD_FOR_RESEARCH`, never a zero-demand score.
- Stale, invalid, non-Egypt, and contradictory signals are preserved and explained.
- Scale requires fresh delivered-order and positive delivered-profit evidence.
- Existing Delivered Orders, Delivered CPA, and Delivery Rate thresholds remain an independent Scale veto.
- Automated-provider status remains `PENDING_INTEGRATION`; credentials alone are not evidence.
- The JSON runner now accepts `market_evidence` and serializes provenance, status, reasons, actions, and evidence snapshots.

## Added — Media Test Protocol Engine

- `SalesChannel`
- `TestBudgetMode`
- `EvidenceMode`
- `MediaEconomicsInput`
- `MediaTestConfig`
- `CampaignObjectivePlan`
- `MediaEconomicsResult`
- `MediaTestStagePlan`
- `StopLossPolicy`
- `ScalePolicy`
- `MediaTestProtocolReport`
- `MediaTestProtocolEngine`

## Objective Selection

- Website: Sales → Website → Purchase.
- WhatsApp/DM/Messenger: Sales when available; otherwise Leads → Messaging Apps.
- Lead Form: Leads → Instant Forms.

## Financial Protection

- Contribution margin before ads.
- Break-even Delivered CPA.
- Target Delivered CPA after safety margin.
- Target Confirmed CPA.
- Target Purchase CPA adjusted for confirmation and delivery rates.

## Test Sequence

1. Angle Test
2. Hook Test
3. Editing Test
4. Offer & CTA Test
5. Winner Validation

## Decision Controls

- One-variable-at-a-time protocol.
- Dynamic duration bounded per test stage.
- Soft and hard stop-loss rules.
- Delivered-order evidence modes: Lean / Standard / Conservative.
- Scale blocked until delivered profit is positive.

## Integration

`CreativeIntelligenceReport` now optionally contains `media_test_protocol`.

## Verification

- 44 embedded tests passed.
- 41 standalone behavioral and governance tests passed on 2026-08-09.
- 0 tests failed.
- v3.1 tests were unavailable because the dependency file was not present in the current runtime.
