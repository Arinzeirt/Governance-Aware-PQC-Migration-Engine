import streamlit as st

from engine.runtime import runtime
from engine.session import session
from engine.runner import runner


def calculate_risk():

    if runtime.critical > 0:
        return "HIGH", "Immediate"

    if runtime.medium > 0:
        return "MEDIUM", "Planned"

    return "LOW", "Monitor"


def readiness_score():

    score = 100

    score -= runtime.critical * 20
    score -= runtime.medium * 8
    score -= runtime.low * 2

    return max(score, 0)


def readiness_label(score):

    if score >= 90:
        return "Excellent Readiness"

    if score >= 75:
        return "Good Readiness"

    if score >= 60:
        return "Moderate Readiness"

    return "Immediate Action Required"


def executive_decision(risk):

    if risk == "HIGH":
        return (
            "Immediate Migration Required",
            "Critical cryptographic assets require immediate planning and executive oversight."
        )

    if risk == "MEDIUM":
        return (
            "Migration Planning Required",
            "Migration planning should begin with business-critical services."
        )

    return (
        "Continue Monitoring",
        "Maintain governance and continue periodic assessments."
    )


def show():

    risk, migration = calculate_risk()

    score = readiness_score()

    decision, explanation = executive_decision(risk)

    #
    # Enterprise Header
    #

    with st.container(border=True):

        left, right = st.columns([5,1])

        with left:

            st.markdown(
                "# Enterprise Assessment Completed"
            )

            st.caption(
                "Enterprise Quantum Migration Platform (EQMP)"
            )

        with right:

            st.metric(
                "Status",
                "SUCCESS"
            )

    st.write("")

    #
    # Executive KPIs
    #

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Quantum Readiness",
            f"{score}%"
        )

        st.caption(
            readiness_label(score)
        )

    with c2:

        st.metric(
            "Overall Risk",
            risk
        )

    with c3:

        st.metric(
            "Migration Priority",
            migration
        )

    with c4:

        st.metric(
            "Assessment Duration",
            runtime.elapsed()
        )

    st.divider()

    #
    # Executive Decision
    #

    st.markdown("### Executive Decision")

    st.info(
        f"""
**Assessment Outcome**

Executive Decision: **{decision}**

{explanation}
"""
    )

    st.divider()

    #
    # Assessment Metadata
    #

    st.markdown("### Assessment Metadata")

    m1, m2, m3 = st.columns(3)

    with m1:

        st.metric(
            "Repository",
            runtime.repository_name or "-"
        )

    with m2:

        st.metric(
            "Files Scanned",
            runtime.total_files
        )

    with m3:

        st.metric(
            "Session",
            session.session_id
        )

    st.divider()

    #
    # Statistics
    #

    s1, s2, s3 = st.columns(3)

    with s1:

        st.metric(
            "Findings",
            runtime.findings
        )

    with s2:

        st.metric(
            "Critical",
            runtime.critical
        )

    with s3:

        st.metric(
            "Medium",
            runtime.medium
        )

    st.divider()

    #
    # Cryptographic Assets
    #

    st.markdown("### Cryptographic Assets Identified")

    if runtime.discoveries:

        displayed = set()

        cols = st.columns(3)

        index = 0

        for item in runtime.discoveries:

            if item["title"] in displayed:
                continue

            displayed.add(item["title"])

            icon = "🟡"

            if item["severity"] == "High":
                icon = "🔴"

            elif item["severity"] == "Low":
                icon = "🟢"

            with cols[index % 3]:

                st.info(
                    f"{icon} {item['title']}"
                )

            index += 1

    else:

        st.info(
            "No cryptographic assets detected."
        )

    st.divider()

    #
    # Toolbar
    #

    left, middle, right = st.columns(3)

    with left:

        if st.button(

            "🔄 New Assessment",

            type="primary",

            use_container_width=True,

        ):

            runtime.new_assessment()

            session.reset()

            runner.running = False

            st.rerun()

    with middle:

        st.button(

            "📄 Export Executive Report",

            disabled=True,

            use_container_width=True,

        )

    with right:

        st.button(

            "📊 View Inventory",

            disabled=True,

            use_container_width=True,

        )

