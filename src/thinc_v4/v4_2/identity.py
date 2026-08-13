# -*- coding: utf-8 -*-
"""Identity, versioning, and watermark protection for the THINC v4.2 layer.

THINC™ v4.2 — Invented by Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 Dr. Ehab Taha — Egy-Pioneers Academy.
"""
from __future__ import annotations

import hashlib


FRAMEWORK_NAME = "THINC"


FRAMEWORK_VERSION = "v4.2 — Creative Intelligence, Media Testing & Scale Protocol Edition"


FRAMEWORK_FULL_NAME = "Taha's Holistic Integration of Needs & Consumer behavior"


AUTHOR_NAME_AR = "الدكتور إيهاب طه"


AUTHOR_NAME_EN = "Dr. Ehab Taha"


TRADEMARK_HOLDER = "EgyPioneers — طلائع شباب مصر"


ACADEMY_NAME = "Egy-Pioneers Academy / Insta Learn Academy"


PROGRAM_POSITIONING = "ابنِ مشروع تجارة إلكترونية مدعوم بالكامل من أول فكرة إلى أول عملية بيع."


COPYRIGHT_YEAR = 2026


def compute_identity_hash() -> str:
    identity_string = (
        f"{FRAMEWORK_NAME}|{FRAMEWORK_VERSION}|{FRAMEWORK_FULL_NAME}|"
        f"{AUTHOR_NAME_EN}|{TRADEMARK_HOLDER}|{PROGRAM_POSITIONING}|{COPYRIGHT_YEAR}"
    )
    return hashlib.sha256(identity_string.encode("utf-8")).hexdigest()


def verify_attribution() -> bool:
    return (
        AUTHOR_NAME_AR == "الدكتور إيهاب طه"
        and AUTHOR_NAME_EN == "Dr. Ehab Taha"
        and FRAMEWORK_NAME == "THINC"
        and FRAMEWORK_FULL_NAME.startswith("Taha's")
    )


def get_watermark() -> str:
    return (
        f"\n💎 {FRAMEWORK_NAME}™ {FRAMEWORK_VERSION.split('—')[0].strip()} — "
        f"© {COPYRIGHT_YEAR} {AUTHOR_NAME_AR} — {TRADEMARK_HOLDER}\n"
        f"   {ACADEMY_NAME}\n"
        f"   Positioning: {PROGRAM_POSITIONING}\n"
        f"   Identity Hash: {compute_identity_hash()[:16]}..."
    )


def enforce_watermark(text: str) -> str:
    if not verify_attribution():
        raise RuntimeError("Identity Protection Violated — THINC attribution was modified.")
    return text.rstrip() + "\n" + get_watermark()
