# -*- coding: utf-8 -*-
"""THINC package — distribution version 4.2.0.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

Layers:
- `thinc_v4.framework` — the v4.0 layer over v3.1.
- `thinc_v4.v4_2` — the v4.2 layer (creative intelligence, media testing,
  market-signal gate, bidirectional niche governance).
"""
from __future__ import annotations

from ._version import PACKAGE_VERSION as PACKAGE_VERSION
from ._version import __version__ as __version__

from .identity import (
    ATTRIBUTION_NOTICE,
    COPYRIGHT_NOTICE,
    IDENTITY_TAGLINE,
    INVENTOR,
    INVENTOR_AR,
    IP_STATEMENT,
    MODEL_NAME,
    OWNER,
    VERSION,
    WATERMARK,
)
from .framework import *  # noqa: F403
