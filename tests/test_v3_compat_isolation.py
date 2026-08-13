# -*- coding: utf-8 -*-
"""Importing any THINC layer must never require the optional v3.1 framework.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

Regression guard: `thinc_v4.pixel_bridge.bridge` used to import
`THINC_v3_1_Master_Framework` unguarded at module level, so `import thinc_v4`
crashed in any environment without the bundled v3.1 snapshot (an installed
wheel, for example) — while the test suite passed because `conftest.py` had
already put the legacy directory on `sys.path`.
"""
from __future__ import annotations

import ast
import importlib
from pathlib import Path

import pytest

PACKAGE = Path(__file__).resolve().parents[1] / "src/thinc_v4"
#: Only the compatibility bridge itself may reach for the v3.1 module names,
#: and it does so through `importlib` with graceful degradation.
V3_MODULE_PREFIX = "THINC_v3_1_Master_Framework"


def _module_level_v3_imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found: list[str] = []
    for node in tree.body:  # module level only
        targets = [node] if isinstance(node, ast.Try) else []
        if isinstance(node, ast.ImportFrom) and (node.module or "").startswith(V3_MODULE_PREFIX):
            found.append(node.module or "")
        for guarded in targets:
            # imports inside a module-level try/except are tolerated only when the
            # handler provides a fallback, which the generational layer does.
            for inner in ast.walk(guarded):
                if isinstance(inner, ast.ImportFrom) and (inner.module or "").startswith(V3_MODULE_PREFIX):
                    if not guarded.handlers:
                        found.append(inner.module or "")
    return found


def test_no_unguarded_v3_imports_in_the_package() -> None:
    offenders = {
        path.relative_to(PACKAGE).as_posix(): _module_level_v3_imports(path)
        for path in sorted(PACKAGE.rglob("*.py"))
        if _module_level_v3_imports(path)
    }
    assert offenders == {}


def test_pixel_bridge_degrades_when_v3_is_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    compat = importlib.import_module("thinc_v4._v3_compat")
    bridge_name = "thinc_v4.pixel_bridge.bridge"

    monkeypatch.setattr(compat, "V3", None)
    monkeypatch.setattr(compat, "V3_IMPORT_ERROR", ModuleNotFoundError("simulated absence"))
    try:
        bridge = importlib.reload(importlib.import_module(bridge_name))
        assert bridge.is_available() is False
        assert "الدكتور إيهاب طه" in bridge.get_watermark()
        with pytest.raises(RuntimeError, match="THINC v3.1"):
            bridge.require_v3("PixelFeedbackBridge")
    finally:
        monkeypatch.undo()
        importlib.reload(importlib.import_module(bridge_name))


def test_pixel_bridge_is_available_with_the_bundled_snapshot() -> None:
    bridge = importlib.import_module("thinc_v4.pixel_bridge.bridge")
    assert bridge.is_available() is True


def test_v4_2_compat_module_re_exports_the_package_loader() -> None:
    package_level = importlib.import_module("thinc_v4._v3_compat")
    v4_2_level = importlib.import_module("thinc_v4.v4_2._v3_compat")
    assert v4_2_level.V3 is package_level.V3
    assert v4_2_level.load_v3_module is package_level.load_v3_module
