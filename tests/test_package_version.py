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

EXPECTED_VERSION = "4.2.0"
PYPROJECT = Path(__file__).resolve().parents[1] / "pyproject.toml"


def test_package_version_is_4_2_0() -> None:
    assert thinc_v4.__version__ == EXPECTED_VERSION
    assert thinc_v4.PACKAGE_VERSION == EXPECTED_VERSION


def test_pyproject_version_matches_package() -> None:
    data = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    assert data["project"]["version"] == thinc_v4.__version__


def test_v4_2_layer_version_is_declared() -> None:
    assert v4_2.LAYER_VERSION == "4.2"
    assert thinc_v4.__version__.startswith(v4_2.LAYER_VERSION + ".")


def test_v4_2_layer_watermark_keeps_attribution() -> None:
    from thinc_v4.v4_2 import master_framework

    watermark = master_framework.get_watermark()
    assert "الدكتور إيهاب طه" in watermark
    assert re.search(r"v4\.2", watermark)
    assert master_framework.verify_attribution() is True
