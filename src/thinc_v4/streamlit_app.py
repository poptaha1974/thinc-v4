# -*- coding: utf-8 -*-
"""
THINC™ v4.0 Streamlit App
واجهة تشغيلية لنظام THINC v4.0
Inventor / Author / Owner: Dr. Ehab Taha (الدكتور إيهاب طه).
© 2026 الدكتور إيهاب طه — EgyPioneers

Run:
    streamlit run thinc_v4_streamlit_app.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING, cast

import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

try:
    from thinc_v4.framework import (
        ACADEMY_NAME,
        PROGRAM_POSITIONING,
        AIOperatingLayer,
        AITaskType,
        AcademyOperatingSystem,
        AudienceSkillLevel,
        AutoUpdateResearchLayer,
        BusinessArchitecture,
        CategoryDesign,
        CompetitiveIntelligence,
        CompetitorProfile,
        EgyptianAudienceGeneration,
        EgyptianizationEngine,
        FounderOS,
        ScientificTheoryRegistry,
        THINCV4Engine,
        THINCV4ProjectInput,
        competitor_rows,
        example_academy_project,
        get_watermark,
        run_all_tests,
    )
except Exception as import_error:  # pragma: no cover
    st.error("تعذر تحميل THINC_v4_0_Master_Framework.py")
    st.exception(import_error)
    st.stop()

st.set_page_config(
    page_title="THINC v4.0 | Commerce Builder",
    page_icon="🧠",
    layout="wide",
)

st.markdown(
    """
<style>
/* Force RTL globally for the app to ensure Arabic displays right-to-left */
html, body, .stApp, .main, .block-container {
    direction: rtl !important;
    text-align: right !important;
    unicode-bidi: embed;
    font-family: 'Segoe UI', Tahoma, sans-serif;
}

.stApp {
    background-color: #020617;
    color: #f8fafc;
}
[data-testid="stSidebar"] {
    direction: rtl;
    text-align: right;
    background-color: #0f172a;
}
[data-testid="stSidebar"] * { color: #f8fafc; }
h1, h2, h3 { color: #22c55e; }
.block-container { padding-top: 2rem; }
[data-testid="stMetric"] {
    background-color: #0f172a;
    border: 1px solid #1e293b;
    padding: 14px;
    border-radius: 14px;
}
.thinc-card {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    border: 1px solid #22c55e;
    border-radius: 16px;
    padding: 18px;
    margin: 12px 0;
}
.thinc-warning {
    background: #422006;
    border: 1px solid #f59e0b;
    border-radius: 16px;
    padding: 18px;
    margin: 12px 0;
}
</style>
""",
    unsafe_allow_html=True,
)


def cached_run_all_tests() -> dict[str, object]:
    """Cache framework tests so Streamlit reruns do not re-execute the full suite."""
    return run_all_tests()


if not TYPE_CHECKING:
    cached_run_all_tests = st.cache_data(show_spinner=False)(cached_run_all_tests)


st.sidebar.title("🧠 THINC™ v4.0")
st.sidebar.caption("THINC v4.0 — Invented by Dr. Ehab Taha")
st.sidebar.caption("Adaptive Commerce Intelligence")
page = st.sidebar.radio(
    "اختر القسم:",
    [
        "📊 Dashboard",
        "📚 Scientific Registry",
        "🇪🇬 Egyptianization",
        "🏗️ Business Architecture",
        "🧭 Category & Competition",
        "🧑‍💼 Founder OS",
        "🤖 AI Stack",
        "🎓 Academy OS",
        "🧬 Full Assessment",
        "📥 Export",
        "✅ Tests",
    ],
)

# -----------------------------------------------------------------------------
# Dashboard
# -----------------------------------------------------------------------------
if page == "📊 Dashboard":
    st.title("📊 THINC v4.0 Dashboard")
    st.markdown(f"### {PROGRAM_POSITIONING}")
    st.caption(ACADEMY_NAME)

    tests = cached_run_all_tests()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Theories", ScientificTheoryRegistry.count())
    c2.metric("Tests", f"{tests['passed']}/{tests['total']}")
    c3.metric("Success Rate", f"{tests['success_rate']}%")
    c4.metric("Status", "Operational" if tests["failed"] == 0 else "Needs Review")

    st.markdown("### المحركات الأساسية")
    engines = pd.DataFrame(
        [
            ["v3 Behavioral Commerce Core", "Persona + THINC Core + Profit + Reality + Decision", "Active"],
            ["Scientific Theory Registry", "50+ theories with evidence levels and update cadence", "Active"],
            ["Egyptianization Engine", "مصري/عربي حسب الجيل ومستوى الخبرة", "Active"],
            ["Business Architecture", "SOPs + fulfillment + risk controls", "Active"],
            ["Competitive Intelligence", "Positioning + offer + creative + trust gaps", "Active"],
            ["Category Design", "تحويل الكورس إلى فئة جديدة", "Active"],
            ["Founder OS", "تقييم الطالب كرائد مشروع", "Active"],
            ["AI Operating Layer", "ChatGPT + Codex + Canva + CapCut + ElevenLabs", "Active"],
            ["Auto Update Layer", "API/RAG-ready stubs", "Ready"],
        ],
        columns=["Engine", "Purpose", "Status"],
    )
    st.dataframe(engines, use_container_width=True, hide_index=True)
    st.code(get_watermark())

# -----------------------------------------------------------------------------
# Scientific Registry
# -----------------------------------------------------------------------------
elif page == "📚 Scientific Registry":
    st.title("📚 Scientific Theory Registry")
    theories = ScientificTheoryRegistry.default_theories()
    df = pd.DataFrame(
        [
            {
                "ID": t.id,
                "Theory": t.name_en,
                "Arabic": t.name_ar,
                "Domain": t.domain.value,
                "Evidence": t.evidence_level.value,
                "Purpose": t.purpose_in_thinc,
                "Applied To": " | ".join(t.applied_to),
                "Update": t.update_cadence.value,
                "Egyptianization Note": t.egyptianization_note,
                "Caution": t.caution,
            }
            for t in theories
        ]
    )
    st.metric("عدد النظريات والنماذج", len(theories))
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown("### التوزيع حسب المجال")
    st.bar_chart(pd.Series(ScientificTheoryRegistry.by_domain()))

    st.markdown("### حالة التحديث الأوتوماتيك")
    st.json(AutoUpdateResearchLayer.status())

# -----------------------------------------------------------------------------
# Egyptianization
# -----------------------------------------------------------------------------
elif page == "🇪🇬 Egyptianization":
    st.title("🇪🇬 Egyptianization Engine")
    col1, col2 = st.columns(2)
    with col1:
        generation = cast(EgyptianAudienceGeneration, st.selectbox("الجيل", list(EgyptianAudienceGeneration), format_func=lambda x: x.value))
    with col2:
        skill = cast(AudienceSkillLevel, st.selectbox("مستوى الخبرة", list(AudienceSkillLevel), format_func=lambda x: x.value))

    profile = EgyptianizationEngine.build_profile(generation, skill)
    msg = EgyptianizationEngine.generate_offer_message(profile)

    c1, c2, c3 = st.columns(3)
    c1.metric("Generation", profile.generation.value)
    c2.metric("Skill", profile.skill_level.value)
    c3.metric("Tone", profile.tone[:30] + "...")

    st.markdown("### رسالة جاهزة")
    st.success(msg)
    st.markdown("### مفردات مناسبة")
    st.write(profile.preferred_words)
    st.markdown("### مفردات يفضل تجنبها")
    st.write(profile.avoided_words)

# -----------------------------------------------------------------------------
# Business Architecture
# -----------------------------------------------------------------------------
elif page == "🏗️ Business Architecture":
    st.title("🏗️ Business Architecture Layer")
    arch = BusinessArchitecture()
    st.metric("Readiness Score", f"{arch.readiness_score()}/10")
    st.markdown("### Revenue Model")
    st.info(arch.revenue_model)
    st.markdown("### Fulfillment Model")
    st.info(arch.fulfillment_model)
    st.markdown("### Offline Trust Point")
    st.success(arch.offline_trust_point)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Required SOPs")
        st.write(arch.required_sops)
    with col2:
        st.markdown("### Risk Controls")
        st.write(arch.risk_controls)

# -----------------------------------------------------------------------------
# Category & Competition
# -----------------------------------------------------------------------------
elif page == "🧭 Category & Competition":
    st.title("🧭 Category Design & Competitive Intelligence")
    cat = CategoryDesign()
    st.metric("Category Strength", f"{cat.category_strength()}/10")
    st.markdown("### Old Category")
    st.error(cat.old_category)
    st.markdown("### New Category")
    st.success(cat.new_category)
    st.markdown("### Enemy")
    st.warning(cat.enemy)
    st.markdown("### Point of View")
    st.info(cat.point_of_view)
    st.markdown("### Proof Stack")
    st.write(cat.category_proof)

    st.markdown("---")
    st.markdown("### Competitive Intelligence Demo")
    comp = CompetitiveIntelligence(
        competitors=[
            CompetitorProfile("كورس دروبشيبينج", "تعليم فقط", "2000-7000", 5, 5, 4, 2, "لا يوجد تشغيل فعلي"),
            CompetitorProfile("أكاديمية تسويق", "شهادة ومحاضرات", "3000-12000", 6, 6, 6, 3, "ضعف التطبيق"),
        ],
        market_gap="السوق مليان كورسات نظرية، لكن قليل جدًا برامج فيها تشغيل حقيقي ومكان فعلي ودعم AI ونادي تجار.",
    )
    st.metric("Differentiation Score", f"{comp.differentiation_score()}/10")
    st.dataframe(pd.DataFrame(competitor_rows(comp.competitors)), use_container_width=True)

# -----------------------------------------------------------------------------
# Founder OS
# -----------------------------------------------------------------------------
elif page == "🧑‍💼 Founder OS":
    st.title("🧑‍💼 Founder OS")
    col1, col2 = st.columns(2)
    with col1:
        execution = st.slider("Execution", 0.0, 10.0, 7.0, 0.5)
        discipline = st.slider("Discipline", 0.0, 10.0, 7.0, 0.5)
        learning = st.slider("Learning Speed", 0.0, 10.0, 8.0, 0.5)
    with col2:
        resilience = st.slider("Resilience", 0.0, 10.0, 7.0, 0.5)
        focus = st.slider("Focus", 0.0, 10.0, 7.0, 0.5)
        financial = st.slider("Financial Discipline", 0.0, 10.0, 6.5, 0.5)

    founder = FounderOS(execution, discipline, learning, resilience, focus, financial)
    readiness = founder.founder_readiness()
    st.metric("Founder Readiness", f"{readiness['score']}/10")
    st.success(readiness["verdict"])
    st.markdown("### Coaching Recommendations")
    st.write(founder.coaching_recommendations())

# -----------------------------------------------------------------------------
# AI Stack
# -----------------------------------------------------------------------------
elif page == "🤖 AI Stack":
    st.title("🤖 AI Operating Layer")
    task = cast(AITaskType, st.selectbox("اختر المهمة", list(AITaskType), format_func=lambda x: x.value))
    tools = AIOperatingLayer.recommend_stack(task)
    df = pd.DataFrame([t.__dict__ | {"task_types": " | ".join(tt.value for tt in t.task_types)} for t in tools])
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("### حساب فرق التكلفة")
    col1, col2 = st.columns(2)
    with col1:
        individual_cost = st.number_input("تكلفة الأدوات منفردة/شهر EGP", value=6500.0, min_value=0.0, step=100.0)
    with col2:
        club_fee = st.number_input("اشتراك النادي/شهر EGP", value=750.0, min_value=1.0, step=50.0)
    st.success(AIOperatingLayer.cost_saving_message(club_fee, individual_cost))

# -----------------------------------------------------------------------------
# Academy OS
# -----------------------------------------------------------------------------
elif page == "🎓 Academy OS":
    st.title("🎓 Academy Operating System")
    academy = AcademyOperatingSystem()
    st.metric("Value Stack Score", f"{academy.value_stack_score()}/10")
    st.success(academy.public_summary())
    st.markdown("### Student Outputs")
    st.write(academy.student_outputs)

# -----------------------------------------------------------------------------
# Full Assessment
# -----------------------------------------------------------------------------
elif page == "🧬 Full Assessment":
    st.title("🧬 THINC v4.0 Full Assessment")
    project_name = st.text_input("اسم المشروع", value="برنامج بناء مشروع تجارة إلكترونية مدعوم بالكامل")
    col1, col2 = st.columns(2)
    with col1:
        generation = cast(EgyptianAudienceGeneration, st.selectbox("الجيل المستهدف", list(EgyptianAudienceGeneration), index=3, format_func=lambda x: x.value))
        skill = cast(AudienceSkillLevel, st.selectbox("مستوى الجمهور", list(AudienceSkillLevel), index=1, format_func=lambda x: x.value))
        persona = st.slider("Persona Completeness %", 0.0, 100.0, 88.0, 1.0)
        taha = st.slider("Taha Index", 0.0, 10.0, 8.5, 0.5)
    with col2:
        profit = st.slider("Profitability Score (-1 لو مفيش بيانات)", -1.0, 10.0, 7.2, 0.5)
        reality = st.slider("Reality Score (-1 لو لسه)", -1.0, 10.0, -1.0, 0.5)
        gen_align = st.slider("Generational Alignment", 0.0, 1.0, 0.92, 0.05)

    project = THINCV4ProjectInput(
        project_name=project_name,
        target_generation=generation,
        skill_level=skill,
        persona_completeness=persona,
        taha_index=taha,
        profitability_score=profit,
        reality_score=reality,
        generational_alignment=gen_align,
        founder_os=FounderOS(7, 7, 8, 7, 7, 6.5),
        competitive_intelligence=CompetitiveIntelligence(
            competitors=[
                CompetitorProfile("كورس دروبشيبينج", "تعليم فقط", "2000-7000", 5, 5, 4, 2, "لا يوجد تشغيل فعلي"),
                CompetitorProfile("أكاديمية تسويق", "شهادة ومحاضرات", "3000-12000", 6, 6, 6, 3, "ضعف التطبيق"),
            ],
            market_gap="السوق مليان كورسات نظرية، لكن قليل جدًا برامج فيها تشغيل حقيقي ومكان فعلي ودعم AI ونادي تجار.",
        ),
    )
    report = THINCV4Engine.assess(project)

    c1, c2, c3 = st.columns(3)
    c1.metric("Final Score", f"{report.final_score}/10")
    c2.metric("Grade", report.grade)
    c3.metric("Theories", report.theory_count)
    st.markdown("### Components")
    st.json(report.components)
    st.markdown("### Message")
    st.success(report.message)
    st.markdown("### Recommendations")
    st.write(report.recommendations)

# -----------------------------------------------------------------------------
# Export
# -----------------------------------------------------------------------------
elif page == "📥 Export":
    st.title("📥 Export")
    report = example_academy_project()
    report_json = json.dumps(report.to_dict(), ensure_ascii=False, indent=2)
    st.download_button("تحميل تقرير المثال JSON", report_json, "thinc_v4_report.json", "application/json")

    theories_df = pd.DataFrame(
        [
            {
                "id": t.id,
                "name_en": t.name_en,
                "name_ar": t.name_ar,
                "domain": t.domain.value,
                "evidence_level": t.evidence_level.value,
                "purpose": t.purpose_in_thinc,
                "update": t.update_cadence.value,
                "egyptianization_note": t.egyptianization_note,
                "caution": t.caution,
            }
            for t in ScientificTheoryRegistry.default_theories()
        ]
    )
    csv = theories_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("تحميل Theory Registry CSV", csv, "thinc_v4_theory_registry.csv", "text/csv")
    st.dataframe(theories_df, use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
elif page == "✅ Tests":
    st.title("✅ Framework Tests")
    res = cached_run_all_tests()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Passed", str(res["passed"]))
    c2.metric("Failed", str(res["failed"]))
    c3.metric("Success Rate", f"{res['success_rate']}%")
    c4.metric("v3 status", str(res["v3_status"]))
    if res["failed"] == 0:
        st.success("كل اختبارات THINC v4.0 نجحت.")
    else:
        st.error("هناك اختبارات فشلت.")
        st.write(res["failed_names"])
    st.json(res)
