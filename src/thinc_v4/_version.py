# -*- coding: utf-8 -*-
"""Single source of truth for the distributed THINC package version.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

`__version__` is the version of the *distribution* (`pyproject.toml`) and moves
whenever shipped content changes. Layer identities are independent of it:
- `thinc_v4.identity.VERSION` → the v4.0 layer ("4.0").
- `thinc_v4.v4_2.LAYER_VERSION` → the v4.2 engine layer ("4.2").
- `thinc_v4.generational` / `thinc_v4.pixel_bridge` → the v4.1 Layer 8 line.
- `thinc_v4.calibration` → the v4.1 calibration line.

A single distribution therefore ships several layer versions; never derive one
from the other.
"""
from __future__ import annotations

__version__ = "4.4.0"
PACKAGE_VERSION = __version__
