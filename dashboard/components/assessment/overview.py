import streamlit as st

from content.industries import INDUSTRIES
from content.countries import COUNTRIES

from components.assessment.summary_panel import show as summary_panel
from components.assessment.insight_banner import show as insight_banner

from components.assessment.validation import (
    overview_complete,
    valid_email,
)

from components.assessment.store import (
    save,
    load,
    assessment_id,
    set_assessment_id,
)

from components.assessment.id_generator import generate


def show():

    existing = load("overview")

    # -------------------------------
    # Quantum Intelligence Brief
    # -------------------------------

    insight_banner()

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # -------------------------------
    # Main Assessment Layout
    # -------------------------------

    left, right = st.columns([7,3], gap="large")

    with left:

        with st.container(border=True):

            st.markdown("## Organisation Information")

            st.caption(
                "Provide information about your organisation before beginning the assessment."
            )

            c1, c2 = st.columns(2)

            with c1:

                st.text_input(
                    "Organisation Name *",
                    key="organisation_name",
                    value=existing.get(
                        "organisation_name",
                        "",
                    ),
                    placeholder="Enet Technologies Ltd",
                )

                st.selectbox(
                    "Industry *",
                    INDUSTRIES,
                    key="industry",
                    index=None,
                    placeholder="Select Industry",
                )

                st.radio(
                    "Critical Infrastructure *",
                    ["Yes", "No"],
                    horizontal=True,
                    key="critical_infrastructure",
                )

            with c2:

                st.text_input(
                    "Official Business Email *",
                    key="organisation_email",
                    value=existing.get(
                        "organisation_email",
                        "",
                    ),
                    placeholder="security@company.com",
                )

                st.selectbox(
                    "Country *",
                    COUNTRIES,
                    key="country",
                    index=None,
                    placeholder="Select Country",
                )

                st.selectbox(
                    "Organisation Size *",
                    [
                        "1–50",
                        "51–250",
                        "251–1000",
                        "1000+",
                    ],
                    key="organisation_size",
                    index=None,
                    placeholder="Select Organisation Size",
                )

    data = {

        "organisation_name":
            st.session_state.get("organisation_name", ""),

        "organisation_email":
            st.session_state.get("organisation_email", ""),

        "industry":
            st.session_state.get("industry"),

        "country":
            st.session_state.get("country"),

        "organisation_size":
            st.session_state.get("organisation_size"),

        "critical_infrastructure":
            st.session_state.get("critical_infrastructure"),

    }

    save(
        "overview",
        data,
    )

    if (
        assessment_id() is None
        and data["country"]
        and data["industry"]
    ):

        set_assessment_id(

            generate(
                data["country"],
                data["industry"],
            )

        )

    completed, total = overview_complete(data)

    email_ok = valid_email(
        data["organisation_email"]
    )

    can_continue = (
        completed == total
        and email_ok
    )

    if data["organisation_email"] and not email_ok:

        st.error(
            "Please enter a valid business email address."
        )

    with right:

        summary_panel(
            current_step="Overview",
            completed=completed,
            total=total,
        )

    return {

        "can_continue": can_continue,

        "on_continue": lambda: save(
            "overview",
            data,
        ),

    }
