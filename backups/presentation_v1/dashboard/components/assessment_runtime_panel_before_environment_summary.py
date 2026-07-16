import streamlit as st

from controllers.runtime_engine import advance_runtime


def show_assessment_runtime(state):

    st.subheader("Assessment Runtime")

    st.progress(state["progress"] / 100)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Current Stage",
            state["stage"]
        )

    with col2:
        st.metric(
            "Progress",
            f'{state["progress"]}%'
        )

    st.divider()

    st.markdown("### Recent Events")

    logs = state.get("logs", [])

    if logs:

        for event in logs:

            st.write(f"• {event}")

    else:

        st.info("Waiting for assessment to start...")

    st.divider()

    if state["running"]:

        if st.button(
            "▶ Next Stage",
            type="primary",
            use_container_width=True
        ):

            advance_runtime()

            st.rerun()

    st.divider()

    with st.expander("Runtime Debug", expanded=False):

        st.json(state)
