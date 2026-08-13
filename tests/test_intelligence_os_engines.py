# -*- coding: utf-8 -*-
"""Unit tests for the Intelligence OS engines behind the API.

Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).

The API tests cover the HTTP contract; these cover the decision logic directly,
including the search-signal classification that used to raise `AttributeError`.
"""
from __future__ import annotations

from datetime import date, datetime, timezone

import pytest

from thinc_v4.external_social_research import (
    CommercialImplication,
    DailyEgyptIntelligenceInput,
    EgyptResearchDomain,
    EvidenceStrength,
    ExternalSocialResearchEngine,
    MarketImpact,
    ResearchObservation,
    ResearchSource,
    ResearchSourceType,
    SignalDirection,
)


def _source(source_type: ResearchSourceType, reliability: float = 7.0) -> ResearchSource:
    return ResearchSource(
        title="مرجع",
        source_name="Desk",
        source_type=source_type,
        retrieved_at=datetime(2026, 8, 13, tzinfo=timezone.utc),
        reliability_score=reliability,
    )


def _observation(
    domain: EgyptResearchDomain,
    source_type: ResearchSourceType | None = None,
    direction: SignalDirection = SignalDirection.UP,
    impact: MarketImpact = MarketImpact.MEDIUM,
) -> ResearchObservation:
    return ResearchObservation(
        domain=domain,
        summary="ملاحظة",
        evidence="دليل",
        direction=direction,
        evidence_strength=EvidenceStrength.MEDIUM,
        market_impact=impact,
        commercial_implications=[CommercialImplication.CATEGORY_DEMAND_UP],
        source=_source(source_type) if source_type else None,
    )


class TestSearchSignalClassification:
    """`SEARCH_TRENDS` is a source type; treating it as a domain crashed at runtime."""

    def test_search_trends_is_not_a_research_domain(self) -> None:
        assert not hasattr(EgyptResearchDomain, "SEARCH_TRENDS")
        assert ResearchSourceType.SEARCH_TRENDS.value == "search_trends"

    def test_observation_from_a_search_source_is_a_search_signal(self) -> None:
        observation = _observation(
            EgyptResearchDomain.PRODUCT_CATEGORY_TREND, ResearchSourceType.SEARCH_TRENDS
        )
        assert ExternalSocialResearchEngine._is_search_signal(observation) is True

    def test_observation_from_another_source_is_not(self) -> None:
        observation = _observation(
            EgyptResearchDomain.PRODUCT_CATEGORY_TREND, ResearchSourceType.NEWS
        )
        assert ExternalSocialResearchEngine._is_search_signal(observation) is False

    def test_observation_without_a_source_is_not(self) -> None:
        assert (
            ExternalSocialResearchEngine._is_search_signal(
                _observation(EgyptResearchDomain.PRODUCT_CATEGORY_TREND)
            )
            is False
        )


class TestSearchSignalEffects:
    def test_rising_search_creates_an_opportunity(self) -> None:
        observations = [
            _observation(
                EgyptResearchDomain.PRODUCT_CATEGORY_TREND, ResearchSourceType.SEARCH_TRENDS
            )
        ]
        opportunities = ExternalSocialResearchEngine.commercial_opportunities(observations)
        assert any("search intent" in item.lower() for item in opportunities)

    def test_search_signal_raises_momentum_weight(self) -> None:
        baseline = ExternalSocialResearchEngine.update_weights([], {})
        with_search = ExternalSocialResearchEngine.update_weights(
            [
                _observation(
                    EgyptResearchDomain.PRODUCT_CATEGORY_TREND, ResearchSourceType.SEARCH_TRENDS
                )
            ],
            {},
        )
        assert with_search["search_trend_momentum"] > baseline["search_trend_momentum"]

    def test_search_signal_adds_campaign_guidance(self) -> None:
        guidance = ExternalSocialResearchEngine.campaign_guidance(
            [
                _observation(
                    EgyptResearchDomain.PRODUCT_CATEGORY_TREND, ResearchSourceType.SEARCH_TRENDS
                )
            ]
        )
        assert any("search trend" in item.lower() for item in guidance)

    def test_search_coverage_gap_is_reported_only_when_absent(self) -> None:
        without = ExternalSocialResearchEngine.research_gaps(
            [_observation(EgyptResearchDomain.INFLATION_PRICES, ResearchSourceType.OFFICIAL_STATISTICS)]
        )
        assert any("search trend momentum" in gap for gap in without)

        with_search = ExternalSocialResearchEngine.research_gaps(
            [
                _observation(
                    EgyptResearchDomain.PRODUCT_CATEGORY_TREND, ResearchSourceType.SEARCH_TRENDS
                )
            ]
        )
        assert not any("search trend momentum" in gap for gap in with_search)


class TestDailyBriefing:
    def test_full_briefing_is_produced_and_bounded(self) -> None:
        payload = DailyEgyptIntelligenceInput(
            intelligence_date=date(2026, 8, 13),
            observations=[
                _observation(
                    EgyptResearchDomain.INFLATION_PRICES,
                    ResearchSourceType.OFFICIAL_STATISTICS,
                    impact=MarketImpact.HIGH,
                ),
                _observation(
                    EgyptResearchDomain.PRODUCT_CATEGORY_TREND, ResearchSourceType.SEARCH_TRENDS
                ),
            ],
        )
        output = ExternalSocialResearchEngine.evaluate_daily_intelligence(payload)

        assert 0 <= output.confidence_score <= 10
        assert output.top_signals
        assert output.source_audit
        assert output.intelligence_date == date(2026, 8, 13)

    def test_low_reliability_source_requires_human_review(self) -> None:
        weak = ResearchObservation(
            domain=EgyptResearchDomain.COMPETITOR_MARKET,
            summary="إشارة ضعيفة المصدر",
            evidence="منشور غير موثق",
            direction=SignalDirection.MIXED,
            source=_source(ResearchSourceType.SOCIAL_MEDIA_TREND, reliability=2.0),
        )
        review = ExternalSocialResearchEngine.human_review_required([weak])
        assert any("reliability" in note.lower() for note in review)


class TestSocialCultureCohortUse:
    """The cohort profile must reach the output, not be computed and discarded."""

    def test_gift_fit_mentions_cohort_language_and_channels(self) -> None:
        from thinc_v4.egyptian_social_culture import (
            EgyptianGenerationalCohort,
            EgyptianSocialCulturalEngine,
            GiftOccasion,
            GiftSocialFitInput,
            LifeStage,
            PriceBand,
        )

        result = EgyptianSocialCulturalEngine.evaluate_gift_social_fit(
            GiftSocialFitInput(
                cohort=EgyptianGenerationalCohort.SOCIAL_NATIVE,
                life_stage=LifeStage.STUDENT,
                occasion=GiftOccasion.BIRTHDAY,
                price_band=PriceBand.PRACTICAL,
                has_packaging=False,
                has_exchange_policy=False,
                has_social_proof=False,
                is_practical=True,
                looks_more_expensive_than_price=False,
                has_clear_use_case=False,
            )
        )

        joined = " ".join(result.blind_spots + result.recommendations)
        assert "تجنّب في الرسالة" in joined
        assert "قنوات مفضّلة للعرض" in joined
        assert 0 <= result.score <= 10

    def test_score_is_unchanged_by_the_cohort_surfacing(self) -> None:
        """Cohort guidance is advisory: it must not silently move the score."""

        from thinc_v4.egyptian_social_culture import (
            EgyptianGenerationalCohort,
            EgyptianSocialCulturalEngine,
            GiftOccasion,
            GiftSocialFitInput,
            LifeStage,
            PriceBand,
        )

        base = GiftSocialFitInput(
            cohort=EgyptianGenerationalCohort.SOCIAL_NATIVE,
            life_stage=LifeStage.STUDENT,
            occasion=GiftOccasion.BIRTHDAY,
            price_band=PriceBand.PRACTICAL,
            has_packaging=True,
            has_exchange_policy=True,
            has_social_proof=True,
            is_practical=True,
            looks_more_expensive_than_price=True,
            has_clear_use_case=True,
        )
        other_cohort = GiftSocialFitInput(
            cohort=EgyptianGenerationalCohort.INFTAH_SATELLITE,
            life_stage=LifeStage.PARENT,
            occasion=GiftOccasion.BIRTHDAY,
            price_band=PriceBand.PRACTICAL,
            has_packaging=True,
            has_exchange_policy=True,
            has_social_proof=True,
            is_practical=True,
            looks_more_expensive_than_price=True,
            has_clear_use_case=True,
        )

        first = EgyptianSocialCulturalEngine.evaluate_gift_social_fit(base)
        second = EgyptianSocialCulturalEngine.evaluate_gift_social_fit(other_cohort)
        assert first.score == pytest.approx(second.score)
