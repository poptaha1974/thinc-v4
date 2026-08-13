# -*- coding: utf-8 -*-
"""Re-export of the package-level v3.1 compatibility bridge.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

The loader lives at `thinc_v4._v3_compat` so every layer (v4.0, v4.2, Layer 8
generational, pixel bridge) resolves v3.1 exactly once and in the same way.
"""
from __future__ import annotations

from .._v3_compat import (
    APP_DIR as APP_DIR,
)
from .._v3_compat import (
    LEGACY_DIR as LEGACY_DIR,
)
from .._v3_compat import (
    PACKAGE_DIR as PACKAGE_DIR,
)
from .._v3_compat import (
    REPO_ROOT as REPO_ROOT,
)
from .._v3_compat import (
    V3 as V3,
)
from .._v3_compat import (
    V3_IMPORT_ERROR as V3_IMPORT_ERROR,
)
from .._v3_compat import (
    _V3_IMPORT_ERROR as _V3_IMPORT_ERROR,
)
from .._v3_compat import (
    V3_MODULE_CANDIDATES as V3_MODULE_CANDIDATES,
)
from .._v3_compat import (
    load_v3_module as load_v3_module,
)
from .._v3_compat import (
    require_v3 as require_v3,
)
from .._v3_compat import (
    v3_available as v3_available,
)
