# -*- coding: utf-8 -*-
"""Pytest configuration for THINC v4.0.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
"""
from __future__ import annotations

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
