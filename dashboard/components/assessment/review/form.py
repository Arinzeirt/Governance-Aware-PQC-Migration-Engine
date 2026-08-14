import streamlit as st

from components.assessment.repository import (
    load_assessment,
)

from components.assessment.store import (
    assessment_id,
)


def summary_card(title, data):

    with st.container(border=True):

        st.subheader(title)

        if not data:

            st.info("No information collected.")

            return

        for key, value in data.items():

            if isinstance(value, list):

                value = ", ".join(value)

            if value in ("", None, []):

                continue

            label = key.replace(
                "_",
                " ",
            ).title()

            st.markdown(
                f"""
<div style="margin-bottom:12px;">

<div style="
font-size:12px;
color:#94A3B8;
text-transform:uppercase;
letter-spacing:0.6px;
">
{label}
</div>

<div style="
font-size:16px;
font-weight:600;
color:white;
">
{value}
</div>

</div>
""",
                unsafe_allow_html=True,
            )


def show():

    assessment = load_assessment()

    st.success(
        "Your enterprise assessment is complete. Review the information below before generating your Enterprise Quantum Readiness Report."
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Assessment ID",
            assessment_id() or "Pending",
        )

    with c2:

        st.metric(
            "Sections Completed",
            "4 / 4",
        )

    with c3:

        st.metric(
            "Assessment Status",
            "Ready",
        )

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:

        summary_card(
            "Enterprise Profile",
            assessment.get("overview"),
        )

        summary_card(
            "Cryptographic Posture",
            assessment.get("cryptography"),
        )

    with right:

        summary_card(
            "Technology Landscape",
            assessment.get("technology"),
        )

        summary_card(
            "Governance & Risk",
            assessment.get("governance"),
        )

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    st.info(
        """
### Executive Readiness Summary

The information provided is sufficient to generate an enterprise
Post-Quantum Readiness Assessment.

The generated report will include:

• Executive Summary

• Enterprise Technology Overview

• Cryptographic Posture Analysis

• Governance & Risk Findings

• Migration Priorities

• Strategic Recommendations

• Enterprise Quantum Readiness Roadmap
"""
    )

    return {

        "completed": 5,

        "total": 5,

        "can_continue": True,

    }

