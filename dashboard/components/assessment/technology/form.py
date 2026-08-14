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

        st.markdown(
            "<h2 style='margin:0 0 4px 0;'>Technology Landscape</h2>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div style='font-size:0.78rem;color:#7f8da3;margin-bottom:10px;'>"
            "Identify the technology environment and exposure relevant to your organisation's quantum-readiness posture."
            "</div>",
            unsafe_allow_html=True,
        )

        left, right = st.columns(2, gap="medium")

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
                placeholder="Select deployment model",
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
                placeholder="Select cloud provider",
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
                placeholder="Select identity provider",
            )

            st.selectbox(
                "Technology Environment Profile *",
                [
                    "Modern",
                    "Legacy",
                    "Mixed Legacy and Modern",
                    "Unknown",
                ],
                key="technology_environment_profile",
                index=None,
                placeholder="Select environment profile",
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
                "Public APIs / Internet-Facing Services *",
                ["Yes", "No"],
                horizontal=True,
                key="public_api",
            )

            st.radio(
                "Significant Third-Party Dependencies *",
                ["Yes", "No", "Unknown"],
                horizontal=True,
                key="third_party_dependencies",
            )

    data = {

        "deployment_model":
            st.session_state.get("deployment_model"),

        "cloud_provider":
            st.session_state.get("cloud_provider"),

        "identity_provider":
            st.session_state.get("identity_provider"),

        "technology_environment_profile":
            st.session_state.get(
                "technology_environment_profile"
            ),

        "pki":
            st.session_state.get("pki"),

        "hsm":
            st.session_state.get("hsm"),

        "customer_apps":
            st.session_state.get("customer_apps"),

        "public_api":
            st.session_state.get("public_api"),

        "third_party_dependencies":
            st.session_state.get(
                "third_party_dependencies"
            ),

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
