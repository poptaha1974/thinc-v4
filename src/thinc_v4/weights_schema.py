# -*- coding: utf-8 -*-
"""Canonical schema for THINC component weights.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

THINC grew two weight vocabularies. The packaged distribution uses descriptive
keys (`v3_behavioral_commerce_core`, `founder_os`, …) while the self-updating
edition bundled with the `thinc-marketing-intelligence` skill uses short keys
(`v3_core`, `founder`, …) for the *same six components with the same values*.

That mismatch used to degrade **silently**: `load_component_weights()` compared
the key set against the defaults and fell back to the built-in weights on any
difference, so pointing `THINC_WEIGHTS_PATH` at a short-key file produced scores
computed with weights the operator never chose, without a single message.

This module makes the descriptive keys canonical, translates the short keys
explicitly, and rejects genuinely broken payloads with a reason instead of a
quiet fallback.

CLI (installed as a console script; `-m` also works but Python warns because the
package imports this module during its own import):

    thinc-v4-weights <weights.json> [--write]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple

#: The canonical component keys, in scoring order.
CANONICAL_WEIGHT_KEYS: Tuple[str, ...] = (
    "v3_behavioral_commerce_core",
    "founder_os",
    "business_architecture",
    "category_design",
    "competitive_differentiation",
    "academy_operating_system",
)

#: Legacy short keys (self-updating edition) → canonical keys.
WEIGHT_KEY_ALIASES: Dict[str, str] = {
    "v3_core": "v3_behavioral_commerce_core",
    "founder": "founder_os",
    "business": "business_architecture",
    "category": "category_design",
    "competitive": "competitive_differentiation",
    "academy": "academy_operating_system",
}

#: Tolerance for the "weights must sum to 1" invariant.
SUM_TOLERANCE = 1e-6

#: Marker appended to a weights version when legacy keys were translated.
NORMALIZED_MARKER = "legacy-keys-normalized"


class WeightsPayloadError(ValueError):
    """Raised when a weights payload cannot be normalized to the canonical form."""


def canonical_key(key: str) -> str:
    """Return the canonical name for `key`.

    Raises:
        WeightsPayloadError: if the key is neither canonical nor a known alias.
    """

    if key in CANONICAL_WEIGHT_KEYS:
        return key
    if key in WEIGHT_KEY_ALIASES:
        return WEIGHT_KEY_ALIASES[key]
    raise WeightsPayloadError(
        f"unknown weight key {key!r}; expected one of "
        f"{', '.join(CANONICAL_WEIGHT_KEYS)} (or a legacy alias: "
        f"{', '.join(sorted(WEIGHT_KEY_ALIASES))})"
    )


def normalize_weight_keys(
    raw: Mapping[str, Any],
) -> Tuple[Dict[str, float], Tuple[str, ...]]:
    """Translate `raw` to canonical keys and floats.

    Returns `(weights, translated_aliases)`; `translated_aliases` names the legacy
    keys that were renamed, so callers can report the translation instead of
    hiding it.

    Raises:
        WeightsPayloadError: unknown key, non-numeric value, conflicting duplicate,
            missing component, or a key set that does not sum to 1.
    """

    weights: Dict[str, float] = {}
    translated: list[str] = []
    for key, value in raw.items():
        target = canonical_key(key)
        try:
            numeric = float(value)
        except (TypeError, ValueError) as err:
            raise WeightsPayloadError(
                f"weight {key!r} must be a number, got {value!r}"
            ) from err
        if target in weights and abs(weights[target] - numeric) > SUM_TOLERANCE:
            raise WeightsPayloadError(
                f"conflicting values for component {target!r}: "
                f"{weights[target]} and {numeric} (a legacy alias and its canonical "
                "key are both present with different values)"
            )
        if target != key:
            translated.append(key)
        weights[target] = numeric

    validate_weights(weights)
    return weights, tuple(sorted(translated))


def validate_weights(weights: Mapping[str, float]) -> None:
    """Check that every canonical component is present exactly once and sums to 1."""

    missing = [key for key in CANONICAL_WEIGHT_KEYS if key not in weights]
    if missing:
        raise WeightsPayloadError(f"missing weight components: {', '.join(missing)}")
    total = sum(weights[key] for key in CANONICAL_WEIGHT_KEYS)
    if abs(total - 1.0) > SUM_TOLERANCE:
        raise WeightsPayloadError(f"weights must sum to 1.0, got {total:.6f}")


def normalize_payload(
    payload: Mapping[str, Any],
) -> Tuple[Dict[str, Any], Tuple[str, ...]]:
    """Normalize a full weights file payload (`{"version": ..., "weights": {...}}`)."""

    if "weights" not in payload:
        raise WeightsPayloadError("weights payload has no 'weights' section")
    raw = payload["weights"]
    if not isinstance(raw, Mapping):
        raise WeightsPayloadError("'weights' must be a mapping of component to number")
    weights, translated = normalize_weight_keys(raw)
    normalized: Dict[str, Any] = dict(payload)
    normalized["weights"] = {key: weights[key] for key in CANONICAL_WEIGHT_KEYS}
    return normalized, translated


def annotate_version(version: str, translated: Tuple[str, ...]) -> str:
    """Make a key translation visible in the reported weights version."""

    if not translated:
        return version
    return f"{version} ({NORMALIZED_MARKER})"


def migrate_file(path: Path, write: bool = False) -> Tuple[Dict[str, Any], Tuple[str, ...]]:
    """Normalize the weights file at `path`, optionally rewriting it in place."""

    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    normalized, translated = normalize_payload(payload)
    if write and translated:
        with path.open("w", encoding="utf-8") as handle:
            json.dump(normalized, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
    return normalized, translated


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Normalize a THINC weights file to the canonical component keys."
    )
    parser.add_argument("path", type=Path, help="path to weights.json")
    parser.add_argument(
        "--write", action="store_true", help="rewrite the file in canonical form"
    )
    args = parser.parse_args()

    try:
        normalized, translated = migrate_file(args.path, write=args.write)
    except (OSError, json.JSONDecodeError, WeightsPayloadError) as err:
        print(f"❌ {err}", file=sys.stderr)
        raise SystemExit(1) from err

    if translated:
        print(f"legacy keys translated: {', '.join(translated)}")
    else:
        print("already canonical")
    if args.write and translated:
        print(f"rewritten: {args.path}")
    else:
        print(json.dumps(normalized["weights"], ensure_ascii=False, indent=2))


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
