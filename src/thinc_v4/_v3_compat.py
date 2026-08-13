# -*- coding: utf-8 -*-
"""Optional compatibility bridge to the THINC v3.1 master framework.

This is the single place in the package that resolves v3.1. Every layer
(v4.0 framework, v4.2 engine, Layer 8 generational, pixel bridge) imports the
`V3` handle from here instead of repeating `try/except ImportError` blocks — and
importing any of them must never crash when v3.1 is absent.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

The v3.1 engines (Persona, CNCR, Profit, Reality Validation, Decision Engine)
are optional at runtime: the v4.2 layer degrades to local calculations when they
are not importable. This module is the single place that resolves them, so no
other module needs `try/except ImportError` blocks.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path
from types import ModuleType

PACKAGE_DIR = Path(__file__).resolve().parent
APP_DIR = PACKAGE_DIR
REPO_ROOT = PACKAGE_DIR.parents[1]
LEGACY_DIR = REPO_ROOT / "thinc_v4_0_final_verified_20260620" / "thinc_v4_final"

#: Candidate module names, in priority order (canonical name first).
V3_MODULE_CANDIDATES = (
    "THINC_v3_1_Master_Framework",
    "THINC_v3_1_Master_Framework_Chatgpt",
)


def _ensure_import_paths() -> None:
    for import_dir in (APP_DIR, REPO_ROOT, LEGACY_DIR):
        if import_dir.exists() and str(import_dir) not in sys.path:
            sys.path.insert(0, str(import_dir))


def load_v3_module() -> tuple[ModuleType | None, Exception | None]:
    """Return `(module, error)` for the first importable v3.1 framework."""

    _ensure_import_paths()
    last_error: Exception | None = None
    for candidate in V3_MODULE_CANDIDATES:
        try:
            return importlib.import_module(candidate), None
        except Exception as err:  # pragma: no cover - depends on local files
            last_error = err
    return None, last_error


V3, V3_IMPORT_ERROR = load_v3_module()

#: Backwards-compatible alias kept for existing call sites.
_V3_IMPORT_ERROR = V3_IMPORT_ERROR


def v3_available() -> bool:
    """True when the optional v3.1 layer is importable."""

    return V3 is not None


def require_v3(consumer: str) -> ModuleType:
    """Return the v3.1 module or fail with a message naming the consumer."""

    if V3 is None:
        raise RuntimeError(
            f"{consumer} requires the THINC v3.1 framework, which is not importable "
            f"({V3_IMPORT_ERROR!r}). Expected it next to the package or under "
            f"{LEGACY_DIR}."
        )
    return V3
