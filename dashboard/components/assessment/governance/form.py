import streamlit as st

from components.assessment.store import (
    save,
    load,
)

from components.assessment.validation import (
    governance_complete,
)


def show():

    existing = load("governance")

    with st.container(border=True):

        st.markdown("## Governance & Risk")

        st.caption(
            "Assess your organisation's governance maturity and readiness for post-quantum migration."
        )

        left, right = st.columns(2)

        with left:

            st.radio(
                "Formal Cybersecurity Governance Framework *",
                ["Yes", "No"],
                horizontal=True,
                key="security_governance",
            )

            st.radio(
                "Post-Quantum Migration Strategy *",
                ["Yes", "No", "In Development"],
                horizontal=True,
                key="pqc_strategy",
            )

            st.radio(
                "Cryptographic Policies *",
                ["Documented", "Partial", "None"],
                horizontal=True,
                key="crypto_policy",
            )

        with right:

            st.radio(
                "Enterprise Risk Register *",
                ["Yes", "No"],
                horizontal=True,
                key="risk_register",
            )

            st.radio(
                "Regulatory Compliance Programme *",
                ["Yes", "No"],
                horizontal=True,
                key="compliance_program",
            )

            st.radio(
                "Executive Sponsorship *",
                ["Yes", "No"],
                horizontal=True,
                key="executive_support",
            )

    data = {

        "security_governance":
            st.session_state.get("security_governance"),

        "pqc_strategy":
            st.session_state.get("pqc_strategy"),

        "crypto_policy":
            st.session_state.get("crypto_policy"),

        "risk_register":
            st.session_state.get("risk_register"),

        "compliance_program":
            st.session_state.get("compliance_program"),

        "executive_support":
            st.session_state.get("executive_support"),

    }

    save(
        "governance",
        data,
    )

    completed, total = governance_complete(data)

    return {

        "completed": completed,

        "total": total,

        "can_continue":
            completed == total,

        "on_continue":
            lambda: save(
                "governance",
                data,
            ),

    }
