import streamlit as st


def show_executive_kpis(decision):

    metrics = decision["metrics"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            label="Assets",
            value=metrics["total_assets"],
            help="Total assets analysed"
        )

        st.caption("Assessment Inventory")

    with col2:

        st.metric(
            label="Readiness",
            value=f"{metrics['average_readiness']}%"
        )

        st.caption("Migration Readiness")

    with col3:

        st.metric(
            label="Threat",
            value=decision["threat"]
        )

        st.caption("Current Risk Level")

    with col4:

        st.metric(
            label="Strategy",
            value=decision["strategy"]
        )

        st.caption("Recommended Action")

