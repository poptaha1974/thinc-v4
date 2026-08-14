# -*- coding: utf-8 -*-
"""Canonical weight-key schema and the legacy-key translation path.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pytest

from thinc_v4 import calibration, framework
from thinc_v4.weights_schema import (
    CANONICAL_WEIGHT_KEYS,
    NORMALIZED_MARKER,
    WEIGHT_KEY_ALIASES,
    WeightsPayloadError,
    annotate_version,
    canonical_key,
    migrate_file,
    normalize_payload,
    normalize_weight_keys,
    validate_weights,
)

#: The weights file shape written by the self-updating edition (skill backend).
LEGACY_WEIGHTS: Dict[str, float] = {
    "v3_core": 0.35,
    "founder": 0.15,
    "business": 0.15,
    "category": 0.12,
    "competitive": 0.10,
    "academy": 0.13,
}

CANONICAL_WEIGHTS: Dict[str, float] = dict(framework.DEFAULT_COMPONENT_WEIGHTS)


def write_payload(path: Path, weights: Dict[str, Any], version: str = "v4.2.0-eg") -> Path:
    path.write_text(
        json.dumps({"version": version, "weights": weights}, ensure_ascii=False),
        encoding="utf-8",
    )
    return path


class TestSchemaContract:
    def test_aliases_cover_every_canonical_component_exactly_once(self) -> None:
        assert set(WEIGHT_KEY_ALIASES.values()) == set(CANONICAL_WEIGHT_KEYS)
        assert len(WEIGHT_KEY_ALIASES) == len(CANONICAL_WEIGHT_KEYS)

    def test_canonical_keys_match_the_framework_defaults(self) -> None:
        assert set(CANONICAL_WEIGHT_KEYS) == set(framework.DEFAULT_COMPONENT_WEIGHTS)

    def test_no_alias_collides_with_a_canonical_key(self) -> None:
        assert not set(WEIGHT_KEY_ALIASES) & set(CANONICAL_WEIGHT_KEYS)

    def test_canonical_key_passes_through_and_translates(self) -> None:
        assert canonical_key("founder_os") == "founder_os"
        assert canonical_key("founder") == "founder_os"

    def test_unknown_key_names_the_expected_keys(self) -> None:
        with pytest.raises(WeightsPayloadError, match="unknown weight key"):
            canonical_key("founder_score")


class TestNormalization:
    def test_legacy_keys_translate_to_canonical_values(self) -> None:
        weights, translated = normalize_weight_keys(LEGACY_WEIGHTS)
        assert weights == CANONICAL_WEIGHTS
        assert translated == tuple(sorted(LEGACY_WEIGHTS))

    def test_canonical_payload_reports_no_translation(self) -> None:
        weights, translated = normalize_weight_keys(CANONICAL_WEIGHTS)
        assert weights == CANONICAL_WEIGHTS
        assert translated == ()

    def test_mixed_keys_agreeing_are_accepted(self) -> None:
        mixed = dict(LEGACY_WEIGHTS)
        mixed.pop("founder")
        mixed["founder_os"] = 0.15
        weights, translated = normalize_weight_keys(mixed)
        assert weights == CANONICAL_WEIGHTS
        assert "founder" not in translated

    def test_conflicting_alias_and_canonical_values_are_rejected(self) -> None:
        conflicting = dict(LEGACY_WEIGHTS)
        conflicting["founder_os"] = 0.25
        with pytest.raises(WeightsPayloadError, match="conflicting values"):
            normalize_weight_keys(conflicting)

    def test_missing_component_is_named(self) -> None:
        partial = dict(LEGACY_WEIGHTS)
        partial.pop("academy")
        with pytest.raises(WeightsPayloadError, match="academy_operating_system"):
            normalize_weight_keys(partial)

    def test_sum_violation_reports_the_total(self) -> None:
        broken = dict(LEGACY_WEIGHTS)
        broken["founder"] = 0.40
        with pytest.raises(WeightsPayloadError, match="must sum to 1.0"):
            normalize_weight_keys(broken)

    def test_non_numeric_value_is_rejected(self) -> None:
        broken: Dict[str, Any] = dict(LEGACY_WEIGHTS)
        broken["founder"] = "high"
        with pytest.raises(WeightsPayloadError, match="must be a number"):
            normalize_weight_keys(broken)

    def test_validate_weights_accepts_the_defaults(self) -> None:
        validate_weights(CANONICAL_WEIGHTS)

    def test_payload_normalization_keeps_canonical_order(self) -> None:
        payload, translated = normalize_payload({"version": "x", "weights": LEGACY_WEIGHTS})
        assert tuple(payload["weights"]) == CANONICAL_WEIGHT_KEYS
        assert payload["version"] == "x"
        assert translated

    def test_payload_without_weights_section_is_rejected(self) -> None:
        with pytest.raises(WeightsPayloadError, match="no 'weights' section"):
            normalize_payload({"version": "x"})

    def test_weights_section_must_be_a_mapping(self) -> None:
        with pytest.raises(WeightsPayloadError, match="must be a mapping"):
            normalize_payload({"weights": [0.35, 0.15]})


class TestVersionAnnotation:
    def test_translation_is_announced(self) -> None:
        assert NORMALIZED_MARKER in annotate_version("v4.2.0-eg", ("founder",))

    def test_clean_version_is_untouched(self) -> None:
        assert annotate_version("v4.1.0-c2", ()) == "v4.1.0-c2"


class TestFrameworkLoading:
    """The regression this phase exists for: legacy files used to fall back silently."""

    def test_legacy_weights_file_is_loaded_not_silently_replaced(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        path = write_payload(tmp_path / "weights.json", LEGACY_WEIGHTS)
        monkeypatch.setenv("THINC_WEIGHTS_PATH", str(path))

        weights, version = framework.load_component_weights()

        assert weights == CANONICAL_WEIGHTS
        assert version != "builtin-fallback", (
            "a legacy-key weights file must be translated, not silently swapped "
            "for the built-in defaults"
        )
        assert NORMALIZED_MARKER in version

    def test_canonical_file_loads_with_its_own_version(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        path = write_payload(tmp_path / "weights.json", CANONICAL_WEIGHTS, version="v4.1.0-c3")
        monkeypatch.setenv("THINC_WEIGHTS_PATH", str(path))

        weights, version = framework.load_component_weights()

        assert weights == CANONICAL_WEIGHTS
        assert version == "v4.1.0-c3"

    def test_unknown_keys_still_fall_back_safely(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        path = write_payload(tmp_path / "weights.json", {"mystery": 1.0})
        monkeypatch.setenv("THINC_WEIGHTS_PATH", str(path))

        weights, version = framework.load_component_weights()

        assert weights == CANONICAL_WEIGHTS
        assert version == "builtin-fallback"

    def test_packaged_weights_file_is_canonical(self) -> None:
        payload = json.loads((framework.APP_DIR / "weights.json").read_text(encoding="utf-8"))
        normalized, translated = normalize_payload(payload)
        assert translated == ()
        assert set(normalized["weights"]) == set(CANONICAL_WEIGHT_KEYS)


class TestCalibrationLoading:
    def test_calibration_reads_legacy_files_in_canonical_form(self, tmp_path: Path) -> None:
        path = write_payload(tmp_path / "weights.json", LEGACY_WEIGHTS)
        payload = calibration.load_weights(path)
        assert payload["weights"] == CANONICAL_WEIGHTS

    def test_calibration_rejects_a_broken_sum_with_a_reason(self, tmp_path: Path) -> None:
        broken = dict(CANONICAL_WEIGHTS)
        broken["founder_os"] = 0.9
        path = write_payload(tmp_path / "weights.json", broken)
        with pytest.raises(WeightsPayloadError, match="must sum to 1.0"):
            calibration.load_weights(path)

    def test_round_trip_through_save_writes_canonical_keys(self, tmp_path: Path) -> None:
        path = write_payload(tmp_path / "weights.json", LEGACY_WEIGHTS)
        payload = calibration.load_weights(path)
        calibration.save_weights(payload, path)
        reloaded = json.loads(path.read_text(encoding="utf-8"))
        assert set(reloaded["weights"]) == set(CANONICAL_WEIGHT_KEYS)


class TestMigrationTool:
    def test_migrate_file_rewrites_only_when_asked(self, tmp_path: Path) -> None:
        path = write_payload(tmp_path / "weights.json", LEGACY_WEIGHTS)

        normalized, translated = migrate_file(path)
        assert translated
        assert "v3_core" in path.read_text(encoding="utf-8")

        migrate_file(path, write=True)
        rewritten = json.loads(path.read_text(encoding="utf-8"))
        assert set(rewritten["weights"]) == set(CANONICAL_WEIGHT_KEYS)
        assert rewritten["weights"] == normalized["weights"]

    def test_migrating_an_already_canonical_file_is_a_no_op(self, tmp_path: Path) -> None:
        path = write_payload(tmp_path / "weights.json", CANONICAL_WEIGHTS)
        before = path.read_text(encoding="utf-8")
        _, translated = migrate_file(path, write=True)
        assert translated == ()
        assert path.read_text(encoding="utf-8") == before
