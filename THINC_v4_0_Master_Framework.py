# -*- coding: utf-8 -*-
"""Compatibility entrypoint for THINC v4.0.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
"""
from __future__ import annotations

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from thinc_v4.framework import *  # noqa: F403
from thinc_v4.framework import main as _main

if __name__ == "__main__":
    _main()
