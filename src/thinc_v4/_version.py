# -*- coding: utf-8 -*-
"""Single source of truth for the distributed THINC package version.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

`__version__` is the version of the *distribution* (`pyproject.toml`).
Layer identities stay separate:
- `thinc_v4.identity.VERSION` → the v4.0 layer.
- `thinc_v4.v4_2.identity.LAYER_VERSION` → the v4.2 layer.
"""
from __future__ import annotations

__version__ = "4.2.0"
PACKAGE_VERSION = __version__
