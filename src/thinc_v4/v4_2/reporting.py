# -*- coding: utf-8 -*-
"""Creative intelligence orchestration and report assembly.

THINC™ v4.2 — Invented by Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 Dr. Ehab Taha — Egy-Pioneers Academy.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List
from .creative_engines import (
    ControlledCreativeExperimentEngine,
    CreativeAngleIntelligenceEngine,
    MontageStrategyEngine,
    ProductDeconstructionEngine,
)
from .creative_models import (
    AdvertisingAngle,
    CreativeBlueprint,
    CreativeVariant,
    EgyptianConsumerPersona,
    ProductIntelligenceInput,
)
from .market_signals import MarketSignalEvidence
from .media_models import (
    MediaEconomicsInput,
    MediaTestConfig,
    MediaTestProtocolReport,
)
from .media_protocol import MediaTestProtocolEngine


@dataclass
class CreativeIntelligenceReport:
    product_name: str
    feature_value_map: List[Dict[str, Any]]
    problem_hierarchy: List[Dict[str, Any]]
    ranked_angles: List[AdvertisingAngle]
    top_blueprint: CreativeBlueprint
    experiment_matrix: Dict[str, List[CreativeVariant]]
    media_test_protocol: MediaTestProtocolReport | None = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if self.media_test_protocol is not None:
            data["media_test_protocol"] = self.media_test_protocol.to_dict()
        return data


class THINCCreativeIntelligenceLayer:
    """End-to-end orchestration: Product → Persona → Angles → Montage → Test Matrix."""

    @classmethod
    def build(
        cls,
        product: ProductIntelligenceInput,
        persona: EgyptianConsumerPersona,
        base_offer: str,
        base_cta: str,
        media_economics: MediaEconomicsInput | None = None,
        media_config: MediaTestConfig | None = None,
        market_evidence: List[MarketSignalEvidence] | None = None,
    ) -> CreativeIntelligenceReport:
        if (media_economics is None) != (media_config is None):
            raise ValueError("media_economics and media_config must be supplied together.")
        angles = CreativeAngleIntelligenceEngine.generate_angles(product, persona)
        blueprint = MontageStrategyEngine.build_blueprint(angles[0], product, cta=base_cta)
        matrix = ControlledCreativeExperimentEngine.build_test_matrix(angles, base_offer, base_cta)
        media_protocol = (
            MediaTestProtocolEngine.build(
                media_economics,
                media_config,
                market_evidence=market_evidence,
            )
            if media_economics is not None and media_config is not None
            else None
        )
        return CreativeIntelligenceReport(
            product_name=product.product_name,
            feature_value_map=ProductDeconstructionEngine.feature_value_map(product),
            problem_hierarchy=ProductDeconstructionEngine.problem_hierarchy(product),
            ranked_angles=angles,
            top_blueprint=blueprint,
            experiment_matrix=matrix,
            media_test_protocol=media_protocol,
        )
