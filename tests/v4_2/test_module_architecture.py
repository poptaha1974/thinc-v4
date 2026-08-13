# -*- coding: utf-8 -*-
"""Architecture guards for the modularized THINC v4.2 layer.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

These tests keep the 4.2.0 modularization from silently regressing back into a
monolith and protect the public facade contract.
"""
from __future__ import annotations

import ast
import importlib
from pathlib import Path

import pytest

PACKAGE = Path(__file__).resolve().parents[2] / "src/thinc_v4/v4_2"
MAX_MODULE_LINES = 560
FACADE = "thinc_v4.v4_2.master_framework"

EXPECTED_MODULES = {
    "__init__",
    "_v3_compat",
    "academy",
    "ai_layer",
    "business",
    "category",
    "competitive",
    "composite",
    "creative_engines",
    "creative_models",
    "egyptianization",
    "examples",
    "founder",
    "governance",
    "identity",
    "market_signals",
    "master_framework",
    "media_models",
    "media_protocol",
    "media_runner",
    "niche_validation",
    "reporting",
    "research",
    "selftest",
    "theories",
}


def module_paths() -> list[Path]:
    return sorted(PACKAGE.glob("*.py"))


def test_expected_module_set() -> None:
    assert {path.stem for path in module_paths()} == EXPECTED_MODULES


@pytest.mark.parametrize("path", module_paths(), ids=lambda p: p.stem)
def test_no_module_is_a_monolith(path: Path) -> None:
    line_count = len(path.read_text(encoding="utf-8").splitlines())
    assert line_count <= MAX_MODULE_LINES, f"{path.name} has {line_count} lines"


@pytest.mark.parametrize("path", module_paths(), ids=lambda p: p.stem)
def test_every_module_keeps_attribution(path: Path) -> None:
    docstring = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8")))
    assert docstring, f"{path.name} is missing a module docstring"


def test_facade_only_re_exports() -> None:
    """`master_framework` must stay a facade: no classes, only the CLI helper."""

    tree = ast.parse((PACKAGE / "master_framework.py").read_text(encoding="utf-8"))
    classes = [node.name for node in tree.body if isinstance(node, ast.ClassDef)]
    functions = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
    assert classes == []
    assert functions == ["main"]


def test_facade_exports_are_importable() -> None:
    facade = importlib.import_module(FACADE)
    missing = [name for name in facade.__all__ if not hasattr(facade, name)]
    assert missing == []
    assert len(facade.__all__) >= 70


def test_import_graph_has_no_cycles() -> None:
    edges: dict[str, set[str]] = {}
    for path in module_paths():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        targets: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module:
                targets.add(node.module)
        edges[path.stem] = targets

    state: dict[str, int] = {}

    def visit(node: str, trail: list[str]) -> None:
        if state.get(node) == 2:
            return
        assert state.get(node) != 1, f"import cycle: {' -> '.join(trail + [node])}"
        state[node] = 1
        for child in sorted(edges.get(node, set())):
            visit(child, trail + [node])
        state[node] = 2

    for module in sorted(edges):
        visit(module, [])


def test_engine_layers_stay_independent_of_the_facade() -> None:
    """No engine module may import the facade (that would recreate the cycle)."""

    offenders = []
    for path in module_paths():
        if path.stem in {"master_framework", "media_runner", "__init__"}:
            continue
        text = path.read_text(encoding="utf-8")
        if "from .master_framework import" in text or "import master_framework" in text:
            offenders.append(path.name)
    assert offenders == []
