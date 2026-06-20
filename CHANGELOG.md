# Changelog

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
