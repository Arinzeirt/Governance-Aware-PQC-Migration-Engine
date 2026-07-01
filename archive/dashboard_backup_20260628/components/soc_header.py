import streamlit as st


def show_header(session_id, progress):

    st.markdown("# ENET TECHNOLOGIES")

    st.caption(
        "Governance-Aware PQC Migration Platform • SOC Assessment Console"
    )

    st.divider()

    col1, col2, col3 = st.columns([2,1,1])

    with col1:
        st.success("🟢 Assessment Running")

    with col2:
        st.metric("Session", session_id)

    with col3:
        st.metric("Progress", f"{progress}%")
