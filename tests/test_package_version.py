# -*- coding: utf-8 -*-
"""Version-contract tests for the THINC distribution.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
"""
from __future__ import annotations

import re
import tomllib
from pathlib import Path

import thinc_v4
from thinc_v4 import v4_2

EXPECTED_VERSION = "4.3.0"
PYPROJECT = Path(__file__).resolve().parents[1] / "pyproject.toml"


def test_package_version_matches_the_declared_release() -> None:
    assert thinc_v4.__version__ == EXPECTED_VERSION
    assert thinc_v4.PACKAGE_VERSION == EXPECTED_VERSION


def test_pyproject_version_matches_package() -> None:
    data = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    assert data["project"]["version"] == thinc_v4.__version__


def test_layer_versions_are_independent_of_the_distribution_version() -> None:
    """One distribution ships several layers; never derive one version from another."""

    from thinc_v4 import identity

    assert v4_2.LAYER_VERSION == "4.2"
    assert identity.VERSION == "4.0"
    # 4.3.0 ships the 4.0 framework, the 4.2 engine and the 4.1 calibration line,
    # so the distribution version must not be tied to any single layer.
    assert thinc_v4.__version__ != v4_2.LAYER_VERSION
    assert not thinc_v4.__version__.startswith(identity.VERSION + ".")


def test_all_shipped_layers_are_importable() -> None:
    import importlib

    for module in (
        "thinc_v4.framework",
        "thinc_v4.v4_2.master_framework",
        "thinc_v4.calibration",
        "thinc_v4.outcomes",
        "thinc_v4.retention",
        "thinc_v4.generational",
        "thinc_v4.pixel_bridge",
        "thinc_v4.gift_decision_intelligence",
        "thinc_v4.egyptian_social_culture",
        "thinc_v4.adaptive_market_learning",
        "thinc_v4.external_social_research",
    ):
        assert importlib.import_module(module)


def test_v4_2_layer_watermark_keeps_attribution() -> None:
    from thinc_v4.v4_2 import master_framework

    watermark = master_framework.get_watermark()
    assert "الدكتور إيهاب طه" in watermark
    assert re.search(r"v4\.2", watermark)
    assert master_framework.verify_attribution() is True
