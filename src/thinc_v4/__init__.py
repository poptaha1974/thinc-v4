# -*- coding: utf-8 -*-
"""THINC package — distribution version 4.3.0.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

Layers:
- `thinc_v4.framework` — the v4.0 layer over v3.1.
- `thinc_v4.v4_2` — the v4.2 layer (creative intelligence, media testing,
  market-signal gate, bidirectional niche governance).
- `thinc_v4.outcomes` / `thinc_v4.calibration` / `thinc_v4.retention` — the v4.1
  outcome-tracking, Bayesian calibration (±20% per cycle) and retention line.

Extension subpackages:
- `thinc_v4.generational` — Layer 8 Generational Intelligence (Egyptian
  generations, formative events, value-shift index, decision modifiers).
- `thinc_v4.pixel_bridge` — closes the feedback loop from Meta Pixel / CAPI
  purchase events back into Layer 8 norms and formative events. Purchase is
  counted only after delivery and payment settlement (the COD truth rule).

The distribution version lives in `thinc_v4._version`; layer identities are
declared per layer (e.g. `thinc_v4.v4_2.LAYER_VERSION`).
"""
from __future__ import annotations

from . import generational, pixel_bridge
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

__all__ = [
    "ATTRIBUTION_NOTICE",
    "COPYRIGHT_NOTICE",
    "IDENTITY_TAGLINE",
    "INVENTOR",
    "INVENTOR_AR",
    "IP_STATEMENT",
    "MODEL_NAME",
    "OWNER",
    "VERSION",
    "WATERMARK",
    "generational",
    "pixel_bridge",
]
