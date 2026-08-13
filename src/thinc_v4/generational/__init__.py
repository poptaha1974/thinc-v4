# -*- coding: utf-8 -*-
"""THINC v4.0 — Generational Intelligence Module (Layer 8).

This module re-exports the Generational Intelligence layer (Layer 8) from the
underlying THINC v3.1 framework, providing a clean, package-level API for
v4.0 consumers (framework, streamlit_app, examples, tests).

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 الدكتور إيهاب طه — EgyPioneers / Egy-Pioneers Academy.

النموذج الجيلي ملكية فكرية حصرية للدكتور إيهاب طه. لا يجوز إزالة أو إضعاف
أي إسناد أو علامة مائية.
"""
from __future__ import annotations

from typing import Any

from .._v3_compat import V3 as _V3  # noqa: F401  (ensures sys.path is prepared once)
from ..identity import INVENTOR, INVENTOR_AR, WATERMARK

# --- Re-export Layer 8 symbols from the bundled v3.1 framework -----------------
# We use a defensive import: v3.1 may live under either canonical filename or
# the legacy "_Chatgpt" filename inside the bundled snapshot.
_IMPORT_ERROR: Exception | None = None
try:
    from THINC_v3_1_Master_Framework import (
        BehavioralPredictors,
        EgyptianGeneration,
        FormativeMemory,
        GenerationalIdentity,
        GenerationalIntelligenceEngine,
        Layer8_GenerationalIntelligence,
        LifeStage,
        ValueWorldview,
    )
except Exception:  # pragma: no cover - fallback path
    try:
        from THINC_v3_1_Master_Framework_Chatgpt import (
            BehavioralPredictors,
            EgyptianGeneration,
            FormativeMemory,
            GenerationalIdentity,
            GenerationalIntelligenceEngine,
            Layer8_GenerationalIntelligence,
            LifeStage,
            ValueWorldview,
        )
    except Exception as err2:
        _IMPORT_ERROR = err2

        # Provide sentinel stubs so importing this module never crashes the
        # whole v4.0 package; consumers should call `is_available()` first.
        class _UnavailableSentinel:
            """Sentinel raised when Layer 8 cannot be loaded from v3.1."""

            def __init__(self, *args: Any, **kwargs: Any) -> None:
                raise RuntimeError(
                    "THINC v3.1 Generational Intelligence (Layer 8) is unavailable: "
                    f"{_IMPORT_ERROR!r}"
                )

        BehavioralPredictors = _UnavailableSentinel
        EgyptianGeneration = _UnavailableSentinel
        FormativeMemory = _UnavailableSentinel
        GenerationalIdentity = _UnavailableSentinel
        GenerationalIntelligenceEngine = _UnavailableSentinel
        Layer8_GenerationalIntelligence = _UnavailableSentinel
        LifeStage = _UnavailableSentinel
        ValueWorldview = _UnavailableSentinel


def is_available() -> bool:
    """Return True iff Layer 8 was successfully imported from v3.1."""
    return _IMPORT_ERROR is None


def get_watermark() -> str:
    """Return the v4.0 watermark — required on every public artifact."""
    return WATERMARK


__all__ = [
    "BehavioralPredictors",
    "EgyptianGeneration",
    "FormativeMemory",
    "GenerationalIdentity",
    "GenerationalIntelligenceEngine",
    "Layer8_GenerationalIntelligence",
    "LifeStage",
    "ValueWorldview",
    "is_available",
    "get_watermark",
    "INVENTOR",
    "INVENTOR_AR",
]
