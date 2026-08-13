# -*- coding: utf-8 -*-
"""Pytest configuration for THINC v4.0.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
LEGACY_V31 = REPO_ROOT / "thinc_v4_0_final_verified_20260620" / "thinc_v4_final"

for _candidate in (SRC, REPO_ROOT, LEGACY_V31):
    if _candidate.exists() and str(_candidate) not in sys.path:
        sys.path.insert(0, str(_candidate))
