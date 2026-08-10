# THINC v4.2 Productionization Design

**Date:** 2026-08-11  
**Status:** Approved design  
**Owner / Inventor:** Dr. Ehab Taha (الدكتور إيهاب طه)

## Objective

Promote the merged THINC v4.2 release bundle into the canonical `src/thinc_v4` package, publish package version `4.2.0`, preserve complete backward compatibility with v4.0 public imports, CLI behavior, Streamlit entrypoints, identity, attribution, watermarking, and Arabic/Egyptian dialect behavior, and produce reproducible release artifacts with SHA-256 checksums and a CycloneDX SBOM.

## Architectural Decision

Use an incremental compatibility-preserving migration.

The existing `src/thinc_v4/framework.py` remains the compatibility facade for current v4.0 consumers. New v4.2 logic moves into focused domain modules and is re-exported through the facade where public access is required. The historical directory `releases/thinc-v4.2-2026-08-09` remains immutable evidence and is not imported at runtime.

Rejected approaches:

- Replacing the v4.0 engine outright: excessive compatibility risk.
- Maintaining a second v4.2 package: preserves the current split source of truth.

## Canonical Package Structure

- `src/thinc_v4/identity.py`: immutable identity, attribution, and canonical version `4.2.0`.
- `src/thinc_v4/framework.py`: v4.0 compatibility facade and re-exports.
- `src/thinc_v4/niche_validation.py`: bidirectional niche discovery, reverse validation, convergence, strategic decisions, launch vetoes, and feedback actions.
- `src/thinc_v4/market_signals.py`: normalized evidence contracts, freshness and geography checks, triangulation stages, provider boundaries, and evidence provenance.
- `src/thinc_v4/media_protocol.py`: channel objective selection, economics, test sequencing, stop-loss policy, scale policy, and serialized reports.
- `src/thinc_v4/governance.py`: approved decision registry and traceability verification.
- `src/thinc_v4/streamlit_app.py`: UI composition only; domain decisions remain in typed domain modules.

Modules communicate through typed dataclasses and enums. Domain modules must not import Streamlit. Circular imports are prohibited. The compatibility facade may import domain modules; domain modules must not import the facade.

## Compatibility Contract

The following remain operational without consumer changes:

- Existing imports from `thinc_v4` and `thinc_v4.framework`.
- `python THINC_v4_0_Master_Framework.py --example`.
- `python THINC_v4_0_Master_Framework.py --test`.
- `streamlit run thinc_v4_streamlit_app.py`.
- Existing v4.0 scoring semantics unless an explicit v4.2 API is requested.
- Inventor, owner, Arabic identity, copyright, watermark, proprietary notice, and Egyptian dialect behavior.

The package reports `4.2.0`; human-facing model labels report `THINC v4.2`.

## Migration Rules

The merged v4.2 release files are reference inputs, not runtime dependencies. Code is moved by responsibility, not copied into another monolith. Case-specific Karseell data, customer data, generated outputs, and historical conversation material are excluded from the installable package.

Public v4.2 names use stable imports from `thinc_v4` or the focused module. Compatibility aliases are explicit and tested.

## Type Safety

MyPy remains in strict mode. All canonical v4.2 modules under `src/thinc_v4` are included by `mypy src`. New public functions and methods require complete parameter and return annotations. Untyped suppressions are prohibited unless they are narrow, justified inline, and unavoidable for a third-party boundary.

External provider payloads enter through typed normalization functions. Raw `dict[str, object]` values do not flow into decision logic without validation.

## Test Strategy

Tests migrate into the root `tests` suite so the default `pytest` command and CI execute them.

Required suites:

- Backward-compatibility imports, CLI, Streamlit importability, identity, attribution, and watermark tests.
- Niche discovery and reverse-validation unit tests.
- Parent-niche guard and launch-veto tests.
- Market evidence status, freshness, geography, contradiction, and missing-evidence tests.
- Media economics, objective selection, stop-loss, and scale-veto tests.
- Governance traceability tests.
- JSON serialization and schema-version tests.
- One end-to-end input-to-decision-report test.
- Package metadata/version parity tests.

Every production behavior change follows red-green-refactor. Existing release tests are first moved or adapted to fail against the absent canonical APIs, then production code is added.

## CI and Release Pipeline

The quality workflow executes:

1. Ruff on canonical source, tests, scripts, and release tooling.
2. MyPy strict on `src`.
3. Pytest with branch coverage.
4. Governance verification.
5. Wheel and sdist build.
6. Installation and smoke test from the built wheel.
7. CycloneDX SBOM generation.
8. SHA-256 manifest generation.
9. Verification that artifact names, package metadata, `identity.VERSION`, and runtime `__version__` all agree on `4.2.0`.

Release artifacts contain no credentials, customer data, case outputs, caches, bytecode, or local environment files.

## Artifact Integrity

The build produces:

- `thinc_v4-4.2.0-py3-none-any.whl`
- `thinc_v4-4.2.0.tar.gz`
- `thinc_v4-4.2.0.cdx.json`
- `SHA256SUMS`

`SHA256SUMS` covers the wheel, sdist, and SBOM. CI verifies the manifest before upload. The release record includes the source commit SHA.

## Security

Dependencies remain explicitly controlled. CI adds dependency vulnerability auditing, secret scanning where supported, and prevents `.pyc`, `__pycache__`, environment files, and unapproved case data from entering artifacts. Runtime integrations read credentials only from environment variables and never serialize or log secret values.

## Documentation

README, changelog, quickstart, package metadata, and release notes are updated together. Documentation distinguishes the canonical v4.2 package from the historical dated release bundle and records backward-compatibility guarantees.

## Delivery Sequence

1. Establish version and compatibility tests.
2. Move niche validation.
3. Move market signals.
4. Extract media protocol from the v4.2 monolith.
5. Add governance verification.
6. Re-export canonical APIs and verify legacy behavior.
7. Expand CI to cover all canonical code and tests.
8. Build and verify wheel, sdist, SBOM, and SHA-256 manifest.
9. Update documentation and release notes.

Each step must leave the repository testable and independently reviewable.

## Success Criteria

- Canonical package and runtime version are `4.2.0`.
- Existing v4.0 imports, CLI, and Streamlit entrypoints pass compatibility tests.
- No runtime import depends on `releases/`.
- Ruff, MyPy strict, pytest, governance verification, build, wheel smoke test, SBOM generation, and checksum verification pass in CI.
- The installable artifact excludes case/customer data and bytecode.
- Identity and attribution to Dr. Ehab Taha (الدكتور إيهاب طه) are unchanged and protected by tests.
