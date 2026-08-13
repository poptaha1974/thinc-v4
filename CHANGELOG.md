# Changelog

## Unreleased

- Made the Markdown link check scan only git-tracked files. It previously walked the tree, so a stray `.pytest_cache/README.md` was collected locally but not in CI (238 tests locally vs 237 in CI for the same commit) and generated or third-party Markdown could fail a suite over links we do not control.
- Added a guard on the guard: the file list must contain the known entry points and at least 25 tracked documents, so a broken listing cannot silently scan nothing.

## 4.3.0 — 2026-08-13

First distribution that ships every merged layer together: the v4.0 framework, the
modular v4.2 engine, the v4.1 calibration line, Layer 8 with the Pixel Feedback
Bridge, and the Intelligence OS service layer. The version moves to 4.3.0 because
the shipped content changed — 4.2.0 must keep describing the artifacts published
under it.

### Version and documentation

- Bumped the distribution to `4.3.0` (`src/thinc_v4/_version.py` + `pyproject.toml`) so the merged layers ship under their own version instead of re-publishing `4.2.0` with different content.
- Documented that layer versions are independent of the distribution version, and replaced the test that derived one from the other with an explicit independence check plus an importability check for all eleven shipped modules.
- Moved `docs/v4_2/RELEASE.md` to `docs/RELEASE.md` (it is a distribution-level document, not a v4.2-layer one) and made it version-agnostic with a `<version>` placeholder and a tag command that reads the version from `pyproject.toml`.
- Clarified in `docs/v4_2/ARCHITECTURE.md` that it documents the v4.2 *layer*, whose version is separate from the distribution's.

### Release publishing robustness

- Fixed a release-publishing hazard found while re-tagging `v4.2.0`: deleting a tag turns its GitHub release into an orphaned draft (slug `untagged-…`), so the previous "does a release exist?" check edited the detached draft and left the tag with duplicate drafts and no published release.
- The workflow now reuses a release only when it is still attached to the tag and not a draft; otherwise it deletes the stale draft and recreates the release with `--verify-tag --latest`.
- Added a post-publish assertion: exactly one release must exist for the tag, and it must not be a draft.
- Documented in `docs/v4_2/RELEASE.md` that new content should get a new version, and what happens if a tag is moved anyway.

### Documentation layout

- Moved the eleven service-layer documents out of the `docs/` root into `docs/api/`, so the API architecture no longer sits beside the packaged-engine docs under a colliding `ARCHITECTURE.md` name.
- Added `docs/api/README.md` as an index mapping each document to the endpoint or engine it describes.
- Moved the calibration execution plan to `docs/v4_1/EXECUTION_PLAN.md`.
- Updated every internal reference (roadmap, scope note, root README, service README) to the new paths.
- Added `tests/test_docs_layout.py`: fails if a service-layer doc drifts back to the `docs/` root, if the index loses an entry, or if any relative Markdown link in the repository points at a missing file.

### Intelligence OS service layer

- Fixed a runtime `AttributeError` in `external_social_research`: five call sites compared an observation's *domain* against `SEARCH_TRENDS`, which is a `ResearchSourceType` member and not a research domain, so any request carrying a search signal returned HTTP 500. Search signals are now classified through the source type via `_is_search_signal()` / `_has_search_signal()`, and the research-gap check reports missing search coverage on the same basis.
- Fixed the silently-dropped cohort profile in `egyptian_social_culture.evaluate_gift_social_fit()`: the computed `SocialNormProfile` was unused (flagged by Ruff `F841`), so the gift evaluation reflected only the occasion. Cohort-specific embarrassment triggers, trust signals, words to avoid, and preferred channels are now surfaced in blind spots and recommendations — deliberately without touching the numeric score, which stays a model decision.
- Added `services/api/errors.py`: invalid enum input now returns HTTP 422 with the helpful message instead of a 500.
- Extended MyPy strict to `services` (with `services/__init__.py`, `services/api/__init__.py` and the `pydantic.mypy` plugin) and annotated the route helpers, health endpoints, and enum coercion generics. 76 files now type-check clean.
- Cleared the remaining Ruff findings (`UP037` quoted annotation, `F841`, `F541`).
- Added test coverage for the previously untested service layer: `tests/services/` (main API, gift intelligence, adaptive learning, external research — happy paths, boundary rejections, and the COD truth rule) and `tests/test_intelligence_os_engines.py` for the engines, including regressions for the search-signal bug and the cohort-usage gap. Suite: 202 tests.
- Documented the domain/source-type distinction, the 422 error contract, and clarified that `docs/ARCHITECTURE.md` covers the service layer while `docs/v4_2/ARCHITECTURE.md` covers the packaged engine.

### Dashboard competitor table

- Fixed the competitor table in the **active** dashboard `src/thinc_v4/streamlit_app.py`: it built rows with `[asdict for asdict in [c.__dict__ for c in comp.competitors]]`, which shadowed the imported `dataclasses.asdict`, never called it, and rendered whatever `__dict__` happened to contain (order and internals included). PR #3 only patched the archived snapshot, so the live surface stayed broken.
- Added `framework.competitor_rows()`: a pure, testable row builder using `dataclasses.asdict` with an explicit column order, so the table stays stable when `CompetitorProfile` gains fields.
- Mirrored the fix in the archived snapshot so both surfaces agree.
- Added tests for column order, values, DataFrame rendering, and a regression guard that fails if the `__dict__` pattern ever returns to either dashboard.

### v4.1 calibration layer

- Rebased the v4.1 calibration line onto the 4.2.0 package: outcome tracking (`outcomes.py`), predictive-accuracy reporting and Bayesian weight calibration with a ±20% per-cycle cap (`calibration.py`), and the retention engine (`retention.py`).
- `framework.load_component_weights()` now reads calibrated weights from `weights.json`, falling back safely to the built-in defaults.
- Made the calibrated weights file relocatable: `THINC_WEIGHTS_PATH` overrides the packaged `weights.json`, `save_weights()` creates missing parent directories, and a read-only target raises a clear error instead of an opaque `OSError` (an installed package lives in a read-only `site-packages`).
- Narrowed the ignore rule from `data/` to `/data/` so reference fixtures under `tests/data/` can never be silently untracked.
- The calibration line does not carry its own distribution version; it ships inside this release.

## 4.2.3 — 2026-08-13

- Fixed release provenance: the workflow's external "rebuild and diff" step rebuilt with `--skip-gates` into `dist/`, overwriting the gated `RELEASE_MANIFEST.json` and `RELEASE_NOTES.md`, so the published record claimed `quality_gates: SKIPPED` even though every gate had passed.
- Reproducibility is now proven inside `build_release.py` (second build in a scratch directory, archive digests compared) and recorded under `reproducibility` in the manifest, leaving the gated artifacts untouched.
- Added `--skip-reproducibility-check` for fast local iterations, and a `Reproducibility` section to the release notes.
- The release workflow now asserts the published manifest reports `quality_gates: PASSED`, zero self-test failures, and `reproducibility.verified: true`.
- Release publishing is now idempotent: an existing release gets its notes re-synced with the replaced artifacts instead of keeping stale digests.
- Added tests that the workflow never packages a gate-skipped build and that reproducibility is recorded.

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
## Layer 8 + Pixel Feedback Bridge — 2026-08-13 (shipped in distribution 4.3.0)

- **Generational Intelligence (Layer 8) is now a first-class v4.0 subpackage**:
  added `src/thinc_v4/generational/` which re-exports `Layer8_GenerationalIntelligence`,
  `GenerationalIntelligenceEngine`, `EgyptianGeneration`, `GenerationalIdentity`,
  `FormativeMemory`, `ValueWorldview`, `BehavioralPredictors`, and `LifeStage`
  from the bundled v3.1 framework, with a defensive fallback when the canonical
  module name is unavailable and an `is_available()` guard.
- **Pixel Feedback Bridge (Meta Pixel ↔ Layer 8)** is now a first-class v4.0
  subpackage: added `src/thinc_v4/pixel_bridge/` containing `PixelPurchaseEvent`,
  `GenerationalRollup`, and the `PixelFeedbackBridge` engine. The bridge
  enforces the Golden Rule (Purchase counted only after delivery + payment
  settlement), computes generational rollups, detects behavioural drift, and
  closes the loop into `GENERATIONAL_NORMS` and `EGYPTIAN_FORMATIVE_EVENTS`.
- Added `examples/karseell/` capturing a real-product validation run
  (Karseell Maca Collagen from the AlHhomz Shopify store) with the test
  script, full Markdown report, and JSON snapshot.
- Added `tests/test_generational_and_pixel_bridge.py` covering subpackage
  availability, Layer 8 re-exports, Egyptian generation enum membership,
  pixel-bridge instantiation, and the documented public API surface.
- Updated the top-level `thinc_v4` namespace to re-export the two extension
  subpackages and tightened the package docstring accordingly.
- Preserved THINC v4.0 identity, ownership, watermarking, attribution, and
  Arabic/Egyptian dialect behavior unchanged.
- Rebased onto the packaged distribution: this layer no longer changes the distribution version (it previously declared `4.1.0`), because the version is owned solely by `src/thinc_v4/_version.py` and enforced by a parity test.
- Merged the package docstring and namespace re-exports so `PACKAGE_VERSION`/`__version__` stay exported alongside `generational` and `pixel_bridge`.
- Fixed an import-time crash: `thinc_v4.pixel_bridge.bridge` imported `THINC_v3_1_Master_Framework` unguarded, so `import thinc_v4` failed in any environment without the bundled v3.1 snapshot (an installed wheel). The suite hid it because `conftest.py` had already put the legacy directory on `sys.path`.
- Promoted the v3.1 loader to `thinc_v4/_v3_compat.py` as the single package-wide resolver (`V3`, `V3_IMPORT_ERROR`, `v3_available()`, `require_v3()`); `thinc_v4/v4_2/_v3_compat.py` is now a thin re-export, and the generational and pixel-bridge layers use the same loader.
- The pixel bridge now exposes `is_available()` and raises a clear `RuntimeError` naming the consumer on first use when v3.1 is absent, instead of crashing on import.
- Added `tests/test_v3_compat_isolation.py`: a static guard against unguarded v3.1 imports anywhere in the package, plus behavioural tests for the degraded path. Verified in a clean virtualenv that the built wheel imports without v3.1.


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
