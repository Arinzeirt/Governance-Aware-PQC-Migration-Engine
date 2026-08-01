import os

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from engine.runtime import runtime
from engine.session import session

from components.workflow_ribbon import show as show_workflow_ribbon


#
# --------------------------------------------------
# KPI Tile
# --------------------------------------------------
#

def kpi(title, value):

    st.metric(title, value)


#
# --------------------------------------------------
# Discovery Card
# --------------------------------------------------
#

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


#
# --------------------------------------------------
# Activity Card
# --------------------------------------------------
#

def activity_card(item):

    with st.container(border=True):

        left, right = st.columns([1, 5])

        with left:

            st.caption(item["time"])

        with right:

            st.write(item["message"])


#
# --------------------------------------------------
# Runtime Dashboard
# --------------------------------------------------
#

def show():

    #
    # Auto Refresh
    #

    if runtime.running:

        st_autorefresh(

            interval=400,

            key="runtime-refresh-v2",

        )

    repository = runtime.repository_name

    if not repository and session.target:

        repository = os.path.basename(
            session.target
        )

    #
    # Page Title
    #

    st.title(
        "Enterprise Discovery Runtime"
    )

    #
    # Hero
    #

    with st.container(border=True):

        st.markdown(
            "## Live Assessment Status"
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Assessment",
                session.session_id
            )

        with c2:

            st.metric(
                "Repository",
                repository or "-"
            )

        with c3:

            st.metric(
                "Stage",
                runtime.stage
            )

        with c4:

            st.metric(
                "Elapsed",
                runtime.elapsed()
            )

        st.write("")

        st.progress(

            runtime.progress / 100,

            text=f"{runtime.progress}% Complete"

        )

        if runtime.current_file:

            st.caption(

                f"Scanning **{os.path.basename(runtime.current_file)}**"

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

    st.write("")

    #
    # Enterprise Workspace
    #

    with st.container(border=True):

        left, right = st.columns(2)

        #
        # Repository
        #

        with left:

            st.caption("Repository")

            st.metric(

                "Repository",

                repository or "-"

            )

            st.metric(

                "Repository Type",

                runtime.repository_type or "-"

            )

            st.metric(

                "Files Scanned",

                f"{runtime.files_scanned}/{runtime.total_files}"

            )

            st.metric(

                "Assessment Status",

                runtime.status

            )

        #
        # Current Processing
        #

        with right:

            st.caption("Current Processing")

            if runtime.current_file:

                st.code(

                    os.path.basename(

                        runtime.current_file

                    ),

                    language="text",

                )

            else:

                st.code(

                    "Waiting for scan...",

                    language="text",

                )

            st.metric(

                "Current Stage",

                runtime.stage

            )

            st.metric(

                "Elapsed",

                runtime.elapsed()

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
    # Live Discovery Workspace
    #

    left, right = st.columns([1, 1])

    #
    # Latest Discoveries
    #

    with left:

        st.subheader(
            "Latest Discoveries"
        )

        if runtime.discoveries:

            for item in runtime.discoveries[:10]:

                discovery_card(item)

        else:

            st.info(

                "No cryptographic discoveries yet."

            )

    #
    # Activity Timeline
    #

    with right:

        st.subheader(
            "Enterprise Activity Timeline"
        )

        if runtime.activity:

            for item in runtime.activity[:20]:

                activity_card(item)

        else:

            st.info(

                "Assessment Ready"

            )

    st.divider()

    #
    # Runtime Summary
    #

    with st.container(border=True):

        st.markdown(
            "### Enterprise Discovery Summary"
        )

        if runtime.running:

            st.info(

                "Assessment is currently executing. Enterprise inventory and migration intelligence are being generated."

            )

        else:

            st.success(

                "Assessment completed successfully."

            )

        a, b, c = st.columns(3)

        with a:

            st.metric(

                "Assets Identified",

                runtime.findings

            )

        with b:

            st.metric(

                "Current Stage",

                runtime.stage

            )

        with c:

            st.metric(

                "Progress",

                f"{runtime.progress}%"

            )

    st.write("")
