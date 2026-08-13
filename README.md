# THINC v4.2 — Invented by Dr. Ehab Taha

**Inventor / Author / Owner:** Dr. Ehab Taha (الدكتور إيهاب طه).  
**Distribution version:** 4.2.0 (v4.0 layer + v4.2 layer in one package).  
**Status:** Proprietary behavioral commerce operating system for Egy-Pioneers Academy.

> THINC v4.0 is the original intellectual property, invention, and proprietary business methodology of Dr. Ehab Taha (الدكتور إيهاب طه). All branding, attribution, watermarks, Arabic/Egyptian dialect support, and ownership statements must be preserved and must not be removed or weakened.

## Architecture

THINC uses a modern Python `src/` package layout. The v4.2 layer now lives
inside the installable package instead of a loose `releases/` folder:

- `src/thinc_v4/identity.py` — single source of truth for inventor, version, watermark, copyright, and IP statements.
- `src/thinc_v4/framework.py` — THINC v4.0 scoring engine, scientific registry, Egyptianization, business architecture, competitive intelligence, Founder OS, AI Operating Layer, and Academy OS.
- `src/thinc_v4/streamlit_app.py` — Streamlit operational dashboard preserving Arabic/Egyptian dialect outputs.
- `src/thinc_v4/_version.py` — distribution version (`4.2.0`); `pyproject.toml` parity is enforced by tests.
- `src/thinc_v4/v4_2/` — the THINC v4.2 layer:
  - `market_signals.py` — auditable market-signal evidence gate.
  - `niche_validation.py` — bidirectional niche family-tree validation and launch gates.
  - `master_framework.py` — stable facade (re-exports + CLI); the engine itself is split into
    `identity`, `theories`, `egyptianization`, `business`, `competitive`, `category`, `founder`,
    `ai_layer`, `academy`, `composite`, `creative_models`, `media_models`, `creative_engines`,
    `media_protocol`, `reporting`, `research`, `examples`, `selftest` — see
    [`docs/v4_2/ARCHITECTURE.md`](docs/v4_2/ARCHITECTURE.md).
  - `_v3_compat.py` — the single optional bridge to THINC v3.1.
  - `media_runner.py` — JSON-in / report-out CLI (`thinc-v4-2`).
  - `governance.py` — requirement registry / traceability coverage (`thinc-v4-2-governance`).
- `tests/v4_2/` — the v4.2 suites, run by the same `make test` gate.
- `tests/data/v4_2/` — reference inputs (Karseell) used by regression tests.
- `docs/v4_2/`, `docs/governance/`, `docs/cases/thinc-v4.2/` — v4.2 docs, approved-decision registry, traceability matrix, and case outputs.
- `thinc_v4_theory_registry.csv` — exported scientific theory registry; tests enforce parity with the in-code registry.

## Usage

```bash
python -m pip install -e '.[dev]'

# v4.0 layer
python THINC_v4_0_Master_Framework.py --example
python THINC_v4_0_Master_Framework.py --test
streamlit run thinc_v4_streamlit_app.py

# v4.2 layer
python -m thinc_v4.v4_2.master_framework --test
python -m thinc_v4.v4_2.master_framework --media-example
thinc-v4-2 tests/data/v4_2/Karseell_THINC_v4_2_input_2026-08-09.json
thinc-v4-2-governance
```

## Quality Gates

```bash
make lint
make type
make test
```

`make type` runs MyPy in strict mode over `src`, `tests`, and `scripts`
(`files` is configured in `pyproject.toml`).

CI has two jobs:

1. `quality` — Ruff lint, MyPy strict, and the full pytest suite (v4.0 + v4.2).
2. `v4_2_smoke` — the v4.2 engine self-test, governance coverage, and the
   Karseell reference run, which must stay `NO_LAUNCH_BEFORE_MODIFICATION`.

## Release Packaging

```bash
make release          # wheel + sdist + SHA256SUMS + SBOM + manifest + notes
make verify-release   # sha256sum -c SHA256SUMS
```

The build runs all quality gates first and aborts if THINC attribution was
modified. Archives are reproducible for a given commit. See
[`docs/v4_2/RELEASE.md`](docs/v4_2/RELEASE.md) for verification steps and the
tag-driven release workflow.

## Security & Configuration

No secrets are hardcoded. External integrations must be configured through environment variables; see `.env.example`.

## Slack Connectivity Test

`scripts/slack_test.py` sends a single test message to verify that `SLACK_BOT_TOKEN` is valid and that the bot can post in the target channel.

**Prerequisites:** the Slack bot must have the `chat:write` scope and be invited to the target channel.

```bash
export SLACK_BOT_TOKEN=xoxb-...    # never commit; set in your shell or CI secret store
export SLACK_CHANNEL_ID=C0123...   # the channel ID (not display name)
python scripts/slack_test.py
```

The token is read exclusively from the environment and is **never** printed, logged, or echoed anywhere.


## Ownership Notice

THINC™ v4.2 — Invented by Dr. Ehab Taha (الدكتور إيهاب طه). Copyright © 2026 Dr. Ehab Taha. All rights reserved.
