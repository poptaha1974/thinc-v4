#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thin CLI wrapper around `thinc_v4.v4_2.governance`.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

Usage:
    python scripts/verify_governance.py [registry.csv traceability.csv]
"""
from __future__ import annotations

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
if SRC.exists() and str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from thinc_v4.v4_2.governance import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
