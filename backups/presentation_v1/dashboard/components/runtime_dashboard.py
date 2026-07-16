import os
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from engine.runtime import runtime
from engine.session import session

from components.workflow_ribbon import show as show_workflow_ribbon


def kpi(title, value):
    st.metric(title, value)


def discovery_card(item):

    icon = "🟡"

    if item["severity"] == "High":
        icon = "🔴"

    elif item["severity"] == "Low":
        icon = "🟢"

    with st.container(border=True):

        st.markdown(
            f"**{icon} {item['title']}**"
        )

        st.caption(
            os.path.basename(item["file"])
        )


def activity_card(item):

    st.markdown(
        f"**{item['time']}**"
    )

    st.write(
        item["message"]
    )

    st.divider()


def show():

    #
    # Auto Refresh
    #

    if runtime.running:

        st_autorefresh(

            interval=400,

            key="runtime-refresh",

        )

    progress = runtime.progress

    repository = runtime.repository_name

    if not repository and session.target:

        repository = os.path.basename(
            session.target
        )

    #
    # Page Title
    #

    st.title(
        "Enterprise Assessment Runtime"
    )

    #
    # ===============================
    # HERO STATUS PANEL
    # ===============================
    #

    with st.container(border=True):

        st.markdown(
            "## Live Assessment Status"
        )

        a, b, c, d = st.columns(4)

        with a:

            st.metric(
                "Assessment",
                session.session_id
            )

        with b:

            st.metric(
                "Repository",
                repository or "-"
            )

        with c:

            st.metric(
                "Stage",
                runtime.stage
            )

        with d:

            st.metric(
                "Elapsed",
                runtime.elapsed()
            )

        st.write("")

        st.progress(

            progress / 100,

            text=f"{progress}% Complete"

        )

        if runtime.current_file:

            st.caption(

                f"Scanning: **{os.path.basename(runtime.current_file)}**"

            )

        else:

            st.caption(

                "Waiting for assessment..."

            )

    st.write("")

    #
    # Workflow
    #

    show_workflow_ribbon()

    st.divider()

    #
    # Assessment Details
    #

    with st.container(border=True):

        left, right = st.columns(2)

        with left:

            st.markdown(
                "### Assessment Details"
            )

            st.write(
                f"**Repository:** {repository}"
            )

            st.write(
                f"**Repository Type:** {runtime.repository_type}"
            )

            st.write(
                f"**Files Scanned:** {runtime.files_scanned}/{runtime.total_files}"
            )

        with right:

            st.markdown(
                "### Current Processing"
            )

            if runtime.current_file:

                st.code(

                    os.path.basename(
                        runtime.current_file
                    ),

                    language="text",

                )

            else:

                st.info(
                    "Waiting..."
                )

    st.divider()

    #
    # Executive KPIs
    #

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:

        kpi(

            "Files",

            f"{runtime.files_scanned}/{runtime.total_files}"

        )

    with c2:

        kpi(

            "Findings",

            runtime.findings

        )

    with c3:

        kpi(

            "Critical",

            runtime.critical

        )

    with c4:

        kpi(

            "Medium",

            runtime.medium

        )

    with c5:

        kpi(

            "Low",

            runtime.low

        )

    st.divider()

    #
    # Live Workspace
    #

    left, right = st.columns(2)

    with left:

        st.subheader(
            "Latest Discoveries"
        )

        if runtime.discoveries:

            for item in runtime.discoveries[:6]:

                discovery_card(item)

        else:

            st.info(
                "No discoveries yet."
            )

    with right:

        st.subheader(
            "Activity Timeline"
        )

        if runtime.activity:

            for item in runtime.activity[:8]:

                activity_card(item)

        else:

            st.info(
                "Assessment Ready"
            )

    st.divider()


