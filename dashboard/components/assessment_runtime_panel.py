import streamlit as st

from controllers.runtime_engine import advance_runtime


def show_assessment_runtime(state):

    st.subheader("Assessment Runtime")

    st.progress(state["progress"] / 100)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Current Stage", state["stage"])

    with col2:
        st.metric("Progress", f"{state['progress']}%")

    st.divider()

    left, right = st.columns([2, 1])

    with left:

        st.markdown("### Assessment Activity")

        logs = state.get("logs", [])

        if logs:

            for log in logs:
                st.success(log)

        else:

            st.info("No activity yet.")

    with right:

        st.markdown("### Environment Summary")

        env = state.get("environment", {})

        if env:

            st.metric(
                "Repository",
                "Git" if env["git_repository"] else "No"
            )

            st.metric(
                "Files",
                f"{env['file_count']:,}"
            )

            st.metric(
                "Languages",
                len(env["languages"])
            )

            st.metric(
                "Project Size",
                f"{env['estimated_size_mb']} MB"
            )

            st.metric(
                "Status",
                "Ready" if env["valid"] else "Invalid"
            )

        else:

            st.info("Waiting for validation...")

    st.divider()

    if state["running"]:

        if st.button(
            "▶ Next Stage",
            type="primary",
            use_container_width=True
        ):

            advance_runtime()

            st.rerun()
