import streamlit as st

from engine.runtime import runtime


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

def discovery_outcome(risk):

    if risk == "HIGH":

        return (

            "Immediate Migration Planning",

            "Critical cryptographic assets have been identified. Governance-led migration planning should begin immediately.",

        )

    if risk == "MEDIUM":

        return (

            "Migration Planning Required",

            "Migration planning should begin with business-critical services and external-facing systems.",

        )

    return (

        "Continue Governance Monitoring",

        "Maintain governance oversight and continue periodic discovery assessments.",

    )


def show():

    risk, migration = calculate_risk()

    score = readiness_score()

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
