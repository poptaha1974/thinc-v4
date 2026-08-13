# -*- coding: utf-8 -*-
"""THINC v4 composite scoring engine.

THINC™ v4.2 — Invented by Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 Dr. Ehab Taha — Egy-Pioneers Academy.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List
from ._v3_compat import V3
from .academy import AcademyOperatingSystem
from .business import BusinessArchitecture
from .category import CategoryDesign
from .competitive import CompetitiveIntelligence
from .egyptianization import (
    AudienceSkillLevel,
    EgyptianAudienceGeneration,
    EgyptianLanguageProfile,
    EgyptianizationEngine,
)
from .founder import FounderOS
from .theories import ScientificTheoryRegistry


@dataclass
class THINCV4ProjectInput:
    project_name: str
    target_generation: EgyptianAudienceGeneration = EgyptianAudienceGeneration.MIXED
    skill_level: AudienceSkillLevel = AudienceSkillLevel.BEGINNER
    persona_completeness: float = 75.0
    taha_index: float = 7.0
    profitability_score: float = -1.0
    reality_score: float = -1.0
    generational_alignment: float = 1.0
    founder_os: FounderOS = field(default_factory=FounderOS)
    business_architecture: BusinessArchitecture = field(default_factory=BusinessArchitecture)
    category_design: CategoryDesign = field(default_factory=CategoryDesign)
    competitive_intelligence: CompetitiveIntelligence = field(default_factory=CompetitiveIntelligence)
    academy_os: AcademyOperatingSystem = field(default_factory=AcademyOperatingSystem)


@dataclass
class THINCV4Report:
    project_name: str
    final_score: float
    grade: str
    components: Dict[str, float]
    language_profile: EgyptianLanguageProfile
    message: str
    recommendations: List[str]
    theory_count: int
    theory_domains: Dict[str, int]
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["language_profile"]["generation"] = self.language_profile.generation.value
        d["language_profile"]["skill_level"] = self.language_profile.skill_level.value
        return d


class THINCV4Engine:
    """Main orchestration engine for THINC v4.0."""

    @staticmethod
    def _grade(score: float) -> str:
        if score >= 8.5:
            return "A — جاهز كمنظومة قوية قابلة للتوسع"
        if score >= 7.0:
            return "B — قوي ويحتاج تحسينات محددة"
        if score >= 5.5:
            return "C — واعد لكن يحتاج ضبط هندسي"
        if score >= 4.0:
            return "D — لا يطلق قبل إعادة بناء نقاط الضعف"
        return "F — أوقف وأعد التصميم"

    @classmethod
    def assess(cls, project: THINCV4ProjectInput) -> THINCV4Report:
        # v3 composite is optional; if v3 unavailable, fallback to local calculation
        if V3 is not None:
            v3_comp = V3.CompositeScoreV3(
                persona_completeness=project.persona_completeness,
                taha_index=project.taha_index,
                profitability_score=project.profitability_score,
                reality_score=project.reality_score,
                generational_alignment=project.generational_alignment,
            ).calculate()
            v3_score = float(v3_comp["score"])
        else:
            v3_score = round((project.persona_completeness / 10) * 0.4 + project.taha_index * 0.6, 2)

        founder = project.founder_os.founder_readiness()["score"]
        business = project.business_architecture.readiness_score()
        category = project.category_design.category_strength()
        competitive = project.competitive_intelligence.differentiation_score()
        academy = project.academy_os.value_stack_score()

        weights = {
            "v3_behavioral_commerce_core": 0.35,
            "founder_os": 0.15,
            "business_architecture": 0.15,
            "category_design": 0.12,
            "competitive_differentiation": 0.10,
            "academy_operating_system": 0.13,
        }
        components = {
            "v3_behavioral_commerce_core": v3_score,
            "founder_os": founder,
            "business_architecture": business,
            "category_design": category,
            "competitive_differentiation": competitive,
            "academy_operating_system": academy,
        }
        final = round(sum(components[k] * weights[k] for k in weights), 2)

        profile = EgyptianizationEngine.build_profile(project.target_generation, project.skill_level)
        message = EgyptianizationEngine.generate_offer_message(profile)
        recommendations: List[str] = []

        if business < 8:
            recommendations.append("استكمل SOPs التشغيلية قبل التوسع: اعتماد المنتج، الشحن، المرتجعات، وتسوية أرباح الطالب.")
        if founder < 7:
            recommendations.extend(project.founder_os.coaching_recommendations())
        if competitive < 7:
            recommendations.append("اعمل Competitive Matrix لثلاثة منافسين على الأقل قبل إطلاق الرسالة النهائية.")
        if category < 8:
            recommendations.append("قوّي Category POV: نحن لسنا كورسًا؛ نحن برنامج بناء مشروع مدعوم بالكامل.")
        if project.reality_score < 0:
            recommendations.append("أضف Reality Validation فعلي من حملة اختبار قبل أي Scale.")
        if project.academy_os.value_stack_score() >= 8:
            recommendations.append("استخدم Value Stack في العرض: تدريب + تشغيل + مكان فعلي + نادي + AI Tools + Workshops.")

        return THINCV4Report(
            project_name=project.project_name,
            final_score=final,
            grade=cls._grade(final),
            components=components,
            language_profile=profile,
            message=message,
            recommendations=recommendations,
            theory_count=ScientificTheoryRegistry.count(),
            theory_domains=ScientificTheoryRegistry.by_domain(),
        )
