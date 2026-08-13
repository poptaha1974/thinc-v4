# Changelog

## 4.2.2 — 2026-08-13

- Fixed the SBOM pin: the `release` extra pinned `cyclonedx-bom==4.6.1`, whose CLI has no `environment` subcommand, so the v4.2.0 release build silently fell back to the minimal SBOM. Pinned `cyclonedx-bom==7.3.1`, which produces the full dependency SBOM (75 components).
- `RELEASE_MANIFEST.json` now records `sbom.generator` and `sbom.components`, and the fallback path prints an explicit warning instead of degrading silently.
- The release workflow now fails if the SBOM was produced by the fallback generator or looks too thin, so a tooling downgrade can never ship unnoticed.
- Added packaging tests for the generator contract and for the `cyclonedx-bom` major-version floor.

## 4.2.1 — 2026-08-13

- Fixed a time-dependent test inherited from the v4.2 suite: `test_karseell_reference_is_not_launchable` asserted a `PASS` evidence gate against an archived 2026-08-09 capture, so it started failing on 2026-08-13 once the capture aged past its 1-7 day freshness limits (this broke CI on `main` right after the 4.2.0 merges).
- The reference capture is now rebased in-test (block shift, relative spacing preserved) so freshness is measured against a controlled offset instead of the calendar.
- Added `test_karseell_reference_as_captured_is_held_for_research`, pinning the documented stale-evidence behavior: the gate reports `HOLD_FOR_RESEARCH` while the launch decision stays `NO_LAUNCH_BEFORE_MODIFICATION`.
- Documented in the CI smoke job that the Karseell step asserts the launch gate, not evidence freshness.

## 4.2.0 — 2026-08-11 (documented release package)

- Added `scripts/build_release.py`: one command produces the wheel, sdist, `SHA256SUMS`, a CycloneDX 1.5 SBOM, `RELEASE_MANIFEST.json` (provenance) and `RELEASE_NOTES.md`.
- The build enforces gates before packaging: Ruff, MyPy strict, pytest, the v4.2 self-test, `pyproject`↔package version parity, and `verify_attribution()` — a modified attribution aborts the release.
- Made archives reproducible: `SOURCE_DATE_EPOCH` pinned to the HEAD commit, sdist rewritten with fixed member mtimes/ownership/permissions and a pinned gzip header. Rebuilds of the same commit produce identical wheel and sdist digests.
- Added `.github/workflows/release.yml` (tag `v*` or manual): rebuild, `sha256sum -c`, reproducibility diff, clean-virtualenv wheel install + self-test, artifact upload, and GitHub Release attachment.
- Added `make release` / `make verify-release` and `docs/v4_2/RELEASE.md` with the full verification procedure.
- Added `tests/test_release_packaging.py` covering the digest helper, version single-source-of-truth, deterministic sdist normalization, and the workflow's verification steps.
- Added a `release` extra (`build`, `cyclonedx-bom`) to `pyproject.toml`.

## 4.2.0 — 2026-08-11 (modularization)

- Split the 2,365-line v4.2 master framework into focused modules under `src/thinc_v4/v4_2/`: `identity`, `theories`, `egyptianization`, `business`, `competitive`, `category`, `founder`, `ai_layer`, `academy`, `composite`, `creative_models`, `media_models`, `creative_engines`, `media_protocol`, `reporting`, `research`, `examples`, `selftest`.
- Kept `master_framework.py` as a stable facade (re-exports + CLI only), so existing imports and `python -m thinc_v4.v4_2.master_framework` keep working.
- Consolidated the optional THINC v3.1 bridge into `_v3_compat.py` with a typed `V3` module handle, removing duplicated `try/except ImportError` blocks from engine code.
- Added `tests/v4_2/test_module_architecture.py`: module-size ceiling, expected module set, facade purity, `__all__` completeness, acyclic import graph, and no engine → facade imports.
- Added `docs/v4_2/ARCHITECTURE.md` documenting the module map and the enforced dependency rules.
- Kept the refactor script `tools/split_master_framework.py` for auditability.
- Verified behavior parity: the Karseell reference run still returns `NO_LAUNCH_BEFORE_MODIFICATION` / `REFINE_OFFER`, self-tests 45/45, Ruff clean, MyPy strict clean, 109 tests passing.

## 4.2.0 — 2026-08-11

- Moved the THINC v4.2 layer out of `releases/thinc-v4.2-2026-08-09/` and into the installable package as `src/thinc_v4/v4_2/` (`master_framework`, `market_signals`, `niche_validation`, `media_runner`, `governance`).
- Bumped the distribution version to `4.2.0` and added `src/thinc_v4/_version.py` as the single source of truth, with tests enforcing parity against `pyproject.toml`.
- Kept layer identities separate: `thinc_v4.identity.VERSION` stays `4.0` for the v4.0 layer, while `thinc_v4.v4_2.LAYER_VERSION` is `4.2`.
- Added console entry points `thinc-v4-2` (media/niche report runner) and `thinc-v4-2-governance` (requirement coverage).
- Relocated v4.2 tests to `tests/v4_2/`, reference inputs to `tests/data/v4_2/`, and v4.2 documentation/governance/case files to `docs/`.
- Fixed the CI `quality` failure: the 19 Ruff findings in the v4.2 sources are resolved (PEP 604 annotations, unused variable, quoted annotation).
- Brought the v4.2 sources to zero MyPy strict errors with real type fixes (CSV JSON-field tuple annotation, `collected_at` None guard, typed Egyptianization tables, annotated `__post_init__`/`check` helpers, distinct report variables, generic `_enum_value`).
- Extended MyPy in CI to `src`, `tests`, and `scripts` via `files` in `pyproject.toml`, with annotation-strictness relaxed only for legacy unittest suites and operational scripts.
- Added a `v4_2_smoke` CI job running the v4.2 engine self-test, governance coverage, and the Karseell reference run asserted to stay `NO_LAUNCH_BEFORE_MODIFICATION`.
- Added `.gitignore` so build, cache, and virtualenv artifacts stay out of the repository.

## 4.0.2 — 2026-06-20

- Fixed CI MyPy strict-mode failures by removing unused import ignores and redundant list casts.
- Added typed Streamlit enum casts for selectbox values before passing them to THINC engine APIs.
- Coerced Streamlit metric values to concrete strings where cached test results are typed as generic objects.
- Preserved THINC v4.0 identity, ownership, watermarking, and Arabic/Egyptian dialect behavior unchanged.

## 4.0.1 — 2026-06-20

- Fixed CI lint configuration by removing invalid Ruff selector `UP045`, which is unsupported by the pinned Ruff version.
- Confirmed Ruff and MyPy remain pinned to explicit reproducible versions in `pyproject.toml` and `requirements_thinc_v4.txt`.
- Re-ran lint, type-check, and tests locally without changing or weakening THINC identity, attribution, ownership, watermarking, or Arabic/Egyptian dialect support.

## 4.0.0 — 2026-06-20

- Added `src/` package layout with `thinc_v4` package and compatibility entrypoints for existing CLI and Streamlit commands.
- Added `src/thinc_v4/identity.py` as the single source of truth for THINC v4.0 identity: inventor, owner, version, watermark, attribution, copyright, and IP statement.
- Preserved and strengthened attribution to Dr. Ehab Taha (الدكتور إيهاب طه) across source headers, README, LICENSE, NOTICE, and tests.
- Added proprietary LICENSE and NOTICE files with explicit ownership and IP protection language.
- Added `pyproject.toml`, pinned requirements, Ruff, MyPy, pytest coverage configuration, pre-commit hooks, Makefile, and GitHub Actions CI.
- Added `.env.example` to document environment-variable-driven integration stubs and avoid hardcoded secrets.
- Added finite-number validation and score clamping helpers to protect scoring from NaN/inf and out-of-range values.
- Fixed v3 fallback scoring normalization so persona completeness is treated as 0–100 and converted to a 0–10 component before weighting.
- Fixed AI Operating Layer cost-saving messaging so invalid costs are rejected and negative savings are never reported.
- Fixed root import drift by adding canonical `THINC_v4_0_Master_Framework.py` and package imports while preserving legacy files.
- Added tests for identity protection, registry CSV parity, scoring edge cases, AI cost-savings behavior, and Streamlit importability.
- Updated README with architecture overview, usage, quality gates, security guidance, and prominent “Invented by Dr. Ehab Taha” attribution.
