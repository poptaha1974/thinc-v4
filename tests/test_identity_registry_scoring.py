# -*- coding: utf-8 -*-
"""Tests for THINC v4.0 identity, registry parity, and scoring.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

import pytest

from thinc_v4 import identity
from thinc_v4.framework import (
    AIOperatingLayer,
    CompetitorProfile,
    FounderOS,
    ScientificTheoryRegistry,
    THINCV4Engine,
    THINCV4ProjectInput,
    get_watermark,
)


def test_identity_constants_are_protected() -> None:
    assert identity.INVENTOR == "Dr. Ehab Taha"
    assert identity.INVENTOR_AR == "الدكتور إيهاب طه"
    assert identity.MODEL_NAME == "THINC"
    assert identity.VERSION == "4.0"
    assert "Invented by Dr. Ehab Taha" in identity.IDENTITY_TAGLINE
    assert "الدكتور إيهاب طه" in identity.IP_STATEMENT
    assert "الدكتور إيهاب طه" in get_watermark()


def test_registry_csv_parity() -> None:
    registry_ids = [theory.id for theory in ScientificTheoryRegistry.default_theories()]
    with Path("thinc_v4_theory_registry.csv").open(encoding="utf-8-sig", newline="") as fh:
        csv_ids = [row["id"] for row in csv.DictReader(fh)]
    assert csv_ids == registry_ids


@pytest.mark.parametrize("bad", [math.nan, math.inf, -math.inf])
def test_founder_scores_reject_non_finite_numbers(bad: float) -> None:
    with pytest.raises(ValueError):
        FounderOS(execution_score=bad)


def test_score_edges_are_clamped_and_valid() -> None:
    report = THINCV4Engine.assess(
        THINCV4ProjectInput(project_name="edge", persona_completeness=1000, taha_index=1000)
    )
    assert 0 <= report.final_score <= 10


def test_competitor_scores_validate_range() -> None:
    with pytest.raises(ValueError):
        CompetitorProfile(name="bad", offer_strength=11)


def test_ai_cost_saving_never_reports_negative_saving() -> None:
    message = AIOperatingLayer.cost_saving_message(monthly_club_fee_egp=500, estimated_individual_cost_egp=100)
    assert "-" not in message.split("بفرق توفير تقريبي", maxsplit=1)[1].split("جنيه", maxsplit=1)[0]


def test_streamlit_module_importable() -> None:
    pytest.importorskip("pandas")
    pytest.importorskip("streamlit")
    import thinc_v4.streamlit_app  # noqa: F401


def test_competitor_rows_are_explicit_and_ordered() -> None:
    """The dashboard table must not depend on `__dict__` ordering or leak internals."""

    from thinc_v4.framework import competitor_rows

    rows = competitor_rows(
        [
            CompetitorProfile("كورس دروبشيبينج", "تعليم فقط", "2000-7000", 5, 5, 4, 2, "لا يوجد تشغيل فعلي"),
            CompetitorProfile("أكاديمية تسويق", "شهادة ومحاضرات", "3000-12000", 6, 6, 6, 3, "ضعف التطبيق"),
        ]
    )

    assert [row["name"] for row in rows] == ["كورس دروبشيبينج", "أكاديمية تسويق"]
    assert list(rows[0]) == [
        "name",
        "positioning",
        "price_range",
        "offer_strength",
        "creative_strength",
        "trust_strength",
        "operational_strength",
        "weakness",
    ]
    assert rows[0]["offer_strength"] == 5
    assert rows[1]["weakness"] == "ضعف التطبيق"


def test_competitor_rows_render_as_a_dataframe() -> None:
    pd = pytest.importorskip("pandas")

    from thinc_v4.framework import competitor_rows

    frame = pd.DataFrame(competitor_rows([CompetitorProfile("منافس", "موقع", "1000", 5, 5, 5, 5, "ضعف")]))
    assert list(frame.columns)[0] == "name"
    assert frame.shape == (1, 8)


def test_no_dunder_dict_tables_remain_in_the_dashboard() -> None:
    """Regression guard for the broken `[asdict for asdict in [c.__dict__ ...]]` table."""

    dashboards = [
        Path(__file__).resolve().parents[1] / "src/thinc_v4/streamlit_app.py",
        Path(__file__).resolve().parents[1]
        / "thinc_v4_0_final_verified_20260620/thinc_v4_final/thinc_v4_streamlit_app.py",
    ]
    for dashboard in dashboards:
        text = dashboard.read_text(encoding="utf-8")
        assert "asdict for asdict in" not in text, dashboard.name
        assert "c.__dict__ for c in comp.competitors" not in text, dashboard.name
