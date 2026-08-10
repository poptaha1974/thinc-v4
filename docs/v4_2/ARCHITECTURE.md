# THINC v4.2 — Module Architecture

**Inventor / Author / Owner:** Dr. Ehab Taha (الدكتور إيهاب طه).
**Distribution version:** 4.2.0.

Before 4.2.0 the v4.2 layer was one 2,365-line file
(`THINC_v4_2_Media_Test_Protocol_Master_Framework.py`). It is now split into
focused modules under `src/thinc_v4/v4_2/`, with `master_framework.py` kept as a
**stable facade** so every existing import keeps working.

## Module map

| Module | Lines | Responsibility |
|---|---|---|
| `identity.py` | ~69 | framework identity, watermark, identity hash, attribution guard |
| `theories.py` | ~194 | scientific theory registry + CSV export |
| `egyptianization.py` | ~128 | generational language and dialect engine |
| `business.py` | ~43 | business architecture layer |
| `competitive.py` | ~55 | competitor profiles and competitive intelligence |
| `category.py` | ~40 | category design layer |
| `founder.py` | ~59 | Founder OS readiness scoring |
| `ai_layer.py` | ~65 | AI operating layer and tool specs |
| `academy.py` | ~55 | Academy operating system |
| `composite.py` | ~145 | THINC v4 composite scoring engine |
| `creative_models.py` | ~175 | creative value objects (enums + dataclasses) |
| `media_models.py` | ~149 | media economics and protocol value objects |
| `creative_engines.py` | ~304 | deconstruction, angles, montage, experiments, winner election |
| `media_protocol.py` | ~444 | media test protocol engine: guardrails, stages, stop-loss, scale |
| `reporting.py` | ~86 | orchestration and report assembly |
| `research.py` | ~65 | auto-update research layer (safe stubs) |
| `examples.py` | ~147 | reference examples |
| `selftest.py` | ~325 | `run_all_tests()` + `print_summary()` |
| `market_signals.py` | ~545 | auditable market-signal evidence gate |
| `niche_validation.py` | ~332 | bidirectional niche family-tree validation |
| `governance.py` | ~74 | requirement registry / traceability coverage |
| `media_runner.py` | ~155 | JSON-in / report-out CLI |
| `_v3_compat.py` | ~58 | single optional bridge to THINC v3.1 |
| `master_framework.py` | ~281 | facade: re-exports + CLI only (no engine code) |

## Dependency rules (enforced by tests)

`tests/v4_2/test_module_architecture.py` fails the build when:

1. a module exceeds 560 lines (no new monoliths),
2. the module set drifts from the expected list,
3. `master_framework.py` gains classes or functions other than `main` (it must
   stay a facade),
4. a facade export is missing or `__all__` shrinks below 70 names,
5. the internal import graph gains a cycle,
6. an engine module imports the facade.

## v3.1 bridge

All optional v3.1 access goes through `_v3_compat.py`, which resolves
`THINC_v3_1_Master_Framework` (or the `_Chatgpt` fallback) once and exposes
`V3` (module or `None`) plus `V3_IMPORT_ERROR`. Engine modules use
`if V3 is not None:` instead of duplicating `try/except ImportError` blocks.

## Behavior parity

The Karseell reference run produces the same decisions before and after the
split — `NO_LAUNCH_BEFORE_MODIFICATION` / `REFINE_OFFER` — with the only output
delta being time-dependent evidence `age_days`. CI asserts this on every push.

---
THINC™ v4.2 — Invented by Dr. Ehab Taha (الدكتور إيهاب طه). © 2026 all rights reserved.
