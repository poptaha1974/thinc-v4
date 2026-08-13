# -*- coding: utf-8 -*-
"""Tests for the v3.1 → v4.0 integration surfaces.

Covers:
* ``thinc_v4.generational`` re-exports Layer 8 symbols and ``is_available()``
  returns ``True`` against the bundled v3.1 framework.
* ``thinc_v4.pixel_bridge`` exposes the bridge classes and they can be
  instantiated without raising.
* The package-level ``thinc_v4`` namespace still exposes identity, watermark,
  and the two extension subpackages.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
"""
from __future__ import annotations

import importlib

import pytest


def test_generational_module_is_available() -> None:
    """Layer 8 must be importable from the bundled v3.1 framework."""
    mod = importlib.import_module("thinc_v4.generational")
    assert mod.is_available() is True, (
        "Generational module reports unavailable; v3.1 bundled framework not "
        "reachable from src/thinc_v4/generational/__init__.py."
    )
    # Watermark must be non-empty and reference Dr. Ehab Taha.
    wm = mod.get_watermark()
    assert isinstance(wm, str) and wm
    assert "Ehab Taha" in wm


def test_generational_reexports() -> None:
    """All expected Layer 8 symbols are re-exported from the subpackage."""
    from thinc_v4 import generational

    expected = {
        "BehavioralPredictors",
        "EgyptianGeneration",
        "FormativeMemory",
        "GenerationalIdentity",
        "GenerationalIntelligenceEngine",
        "Layer8_GenerationalIntelligence",
        "LifeStage",
        "ValueWorldview",
    }
    missing = expected - set(dir(generational))
    assert not missing, f"Missing re-exports: {missing!r}"


def test_egyptian_generation_enum_members() -> None:
    """Sanity check: the seven canonical Egyptian generations are present."""
    from thinc_v4.generational import EgyptianGeneration

    members = {m.name for m in EgyptianGeneration}
    # All seven core generations + the UNKNOWN sentinel.
    assert "GEN_TIKTOK" in members
    assert "GEN_YANAYER" in members
    assert "GEN_INFITAH" in members
    assert "GEN_NASSER" in members
    assert "GEN_KIFAH" in members
    assert "GEN_ALPHA" in members
    assert "GEN_BETA" in members
    assert "UNKNOWN" in members


def test_pixel_bridge_module_classes_importable() -> None:
    """Pixel bridge classes are importable from the subpackage."""
    from thinc_v4.pixel_bridge import (
        GenerationalRollup,
        PixelFeedbackBridge,
        PixelPurchaseEvent,
    )

    assert PixelFeedbackBridge.__name__ == "PixelFeedbackBridge"
    assert PixelPurchaseEvent.__name__ == "PixelPurchaseEvent"
    assert GenerationalRollup.__name__ == "GenerationalRollup"


def test_pixel_bridge_can_be_instantiated() -> None:
    """``PixelFeedbackBridge`` instantiates without raising."""
    from thinc_v4.pixel_bridge import PixelFeedbackBridge

    bridge = PixelFeedbackBridge()
    # Bridge must expose the documented public API surface.
    for method in (
        "ingest_events",
        "rollup_by_generation",
        "detect_anomalies",
        "update_generational_norms",
        "propose_new_formative_events",
        "generate_feedback_report",
        "save_state",
    ):
        assert hasattr(bridge, method), f"Bridge missing public method: {method}"


def test_top_level_package_exposes_extension_subpackages() -> None:
    """``thinc_v4`` re-exports ``generational`` and ``pixel_bridge``."""
    import thinc_v4

    assert hasattr(thinc_v4, "generational")
    assert hasattr(thinc_v4, "pixel_bridge")
    assert "Ehab Taha" in thinc_v4.WATERMARK
    assert thinc_v4.VERSION.startswith("4.")
