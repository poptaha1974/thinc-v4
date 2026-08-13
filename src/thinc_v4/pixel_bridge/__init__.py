# -*- coding: utf-8 -*-
"""THINC v4.0 — Pixel Feedback Bridge.

This plugin closes the feedback loop between Meta Pixel/CAPI purchase events
and the Generational Intelligence layer (Layer 8): it ingests real purchase
data, computes generational rollups, detects behavioural drift, and updates
GENERATIONAL_NORMS / formative events on the underlying engine.

Golden Rule (enforced by the bridge):
    A purchase event is only counted after both delivery confirmation and
    payment settlement — never on `add_to_cart` or on cancelled / returned
    orders.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 الدكتور إيهاب طه — EgyPioneers / Egy-Pioneers Academy.
"""
from __future__ import annotations

from ..identity import INVENTOR, INVENTOR_AR, WATERMARK
from .bridge import (
    GenerationalRollup,
    PixelFeedbackBridge,
    PixelPurchaseEvent,
)

__all__ = [
    "GenerationalRollup",
    "PixelFeedbackBridge",
    "PixelPurchaseEvent",
    "INVENTOR",
    "INVENTOR_AR",
    "WATERMARK",
]
