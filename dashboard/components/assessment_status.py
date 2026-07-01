import streamlit as st


def show_assessment_status(state):

    with st.container(border=True):

        st.markdown("## Live Assessment")

        st.progress(
            state["progress"] / 100
        )

        left, right = st.columns([3, 2])

        with left:

            st.metric(
                "Current Stage",
                state["current"]
            )

            st.info(
                state["operation"]
            )

        with right:

            st.metric(
                "Session",
                state["session"]
            )

            if state["progress"] < 100:

                st.success("🟢 Assessment Running")

            else:

                st.success("✅ Assessment Complete")
