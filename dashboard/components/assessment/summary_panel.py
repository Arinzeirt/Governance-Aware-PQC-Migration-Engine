import streamlit as st

from components.assessment.status import (
    readiness_percentage,
    readiness_status,
)

from components.assessment.store import (
    last_saved,
    assessment_id,
)


def show(current_step, completed, total):

    progress = readiness_percentage(
        completed,
        total,
    )

    status = readiness_status(
        completed,
        total,
    )

    saved = last_saved()

    aid = assessment_id()

    with st.container(border=True):

        st.markdown("## Assessment Summary")

        st.markdown("**Assessment ID**")

        if aid:

            st.code(aid)

        else:

            st.caption("Pending Assignment")

        st.divider()

        st.markdown(
            f"**Current Step**  \n{current_step}"
        )

        st.markdown(
            f"**Completed Fields**  \n{completed} of {total}"
        )

        st.markdown(
            f"**Completion**  \n{progress}%"
        )

        st.progress(progress / 100)

        st.divider()

        st.markdown("**Assessment Health**")

        if status["level"] == "success":

            st.success(status["label"])

        elif status["level"] == "warning":

            st.warning(status["label"])

        else:

            st.info(status["label"])

        st.markdown("**Auto Save**")

        st.success("Active")

        st.markdown("**Last Saved**")

        if saved:

            st.caption(
                saved.strftime("%H:%M:%S")
            )

        else:

            st.caption("--")

        st.divider()

        st.caption("EQMP Enterprise v1")
