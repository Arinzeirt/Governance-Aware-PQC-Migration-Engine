import streamlit as st

from components.assessment.store import (
    save,
    load,
)

from components.assessment.validation import (
    technology_complete,
)


def show():

    existing = load("technology")

    with st.container(border=True):

        st.markdown("## Technology Landscape")

        st.caption(
            "Describe your organisation's technology environment to support enterprise quantum readiness analysis."
        )

        left, right = st.columns(2)

        with left:

            st.selectbox(
                "Deployment Model *",
                [
                    "On-Premises",
                    "Cloud",
                    "Hybrid",
                ],
                key="deployment_model",
                index=None,
                placeholder="Select Deployment Model",
            )

            st.selectbox(
                "Primary Cloud Provider *",
                [
                    "AWS",
                    "Microsoft Azure",
                    "Google Cloud",
                    "Oracle Cloud",
                    "Multiple",
                    "None",
                ],
                key="cloud_provider",
                index=None,
                placeholder="Select Cloud Provider",
            )

            st.selectbox(
                "Identity Provider *",
                [
                    "Active Directory",
                    "Microsoft Entra ID",
                    "Okta",
                    "Google Workspace",
                    "Other",
                    "None",
                ],
                key="identity_provider",
                index=None,
                placeholder="Select Identity Provider",
            )

        with right:

            st.radio(
                "Public Key Infrastructure (PKI) *",
                ["Yes", "No", "Unknown"],
                horizontal=True,
                key="pki",
            )

            st.radio(
                "Hardware Security Modules (HSMs) *",
                ["Yes", "No", "Unknown"],
                horizontal=True,
                key="hsm",
            )

            st.radio(
                "Customer-Facing Applications *",
                ["Yes", "No"],
                horizontal=True,
                key="customer_apps",
            )

            st.radio(
                "Public APIs *",
                ["Yes", "No"],
                horizontal=True,
                key="public_api",
            )

    data = {

        "deployment_model":
            st.session_state.get("deployment_model"),

        "cloud_provider":
            st.session_state.get("cloud_provider"),

        "identity_provider":
            st.session_state.get("identity_provider"),

        "pki":
            st.session_state.get("pki"),

        "hsm":
            st.session_state.get("hsm"),

        "customer_apps":
            st.session_state.get("customer_apps"),

        "public_api":
            st.session_state.get("public_api"),

    }

    save(
        "technology",
        data,
    )

    completed, total = technology_complete(data)

    return {

        "completed": completed,

        "total": total,

        "can_continue":
            completed == total,

        "on_continue":
            lambda: save(
                "technology",
                data,
            ),

    }
