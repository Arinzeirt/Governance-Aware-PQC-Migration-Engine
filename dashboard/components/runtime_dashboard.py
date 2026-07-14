import os

import streamlit as st

from engine.runtime import runtime
from engine.session import session

from components.workflow_ribbon import show as show_workflow_ribbon
from components.footer import show as show_footer


PROGRESS = {

    "IDLE": 0,
    "INITIALIZING": 10,
    "TARGET": 20,
    "DISCOVERY": 50,
    "INVENTORY": 75,
    "REPORT": 90,
    "COMPLETED": 100,
    "FAILED": 100,

}


def kpi(title, value):

    st.metric(

        label=title,

        value=value,

    )


def discovery_card(item):

    icon = "🟡"

    if item["severity"] == "High":

        icon = "🔴"

    elif item["severity"] == "Low":

        icon = "🟢"

    st.markdown(

        f"**{icon} {item['title']}**"

    )

    st.caption(

        os.path.basename(

            item["file"]

        )

    )

    st.divider()


def activity_card(item):

    st.markdown(

        f"✅ {item['message']}"

    )

    st.caption(

        item["time"]

    )

    st.divider()


def show():

    progress = PROGRESS.get(

        session.state,

        runtime.progress,

    )

    #
    # Executive Header
    #

    st.title(

        "Enterprise Assessment Runtime"

    )

    repository = runtime.repository_name or "-"

    repository_type = runtime.repository_type or "Local Directory"

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "Assessment Session",

            session.session_id,

        )

    with c2:

        st.metric(

            "Repository",

            repository,

        )

    with c3:

        st.metric(

            "Assessment State",

            session.state,

        )

    st.progress(

        progress / 100

    )

    st.caption(

        runtime.status

    )

    #
    # Temporary Runtime Debug
    #

    with st.expander(

        "Runtime Debug",

        expanded=False,

    ):

        st.code(

            {

                "Repository": runtime.repository_name,

                "Repository Type": runtime.repository_type,

                "Files": runtime.files_scanned,

                "Total": runtime.total_files,

                "Current File": runtime.current_file,

                "Findings": runtime.findings,

                "Stage": runtime.stage,

                "Status": runtime.status,

                "Refresh Counter": runtime.refresh_counter,

            },

            language="python",

        )

    #
    # Workflow
    #

    show_workflow_ribbon()

    st.divider()

    #
    # Repository Row
    #

    left, right = st.columns(2)

    with left:

        st.subheader(

            "Repository"

        )

        st.write(

            repository

        )

        st.caption(

            repository_type

        )

    with right:

        st.subheader(

            "Current File"

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

                "Waiting for scan..."

            )

    st.divider()

    #
    # KPI Row
    #

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:

        kpi(

            "Files",

            f"{runtime.files_scanned}/{runtime.total_files}"

        )

    with k2:

        kpi(

            "Findings",

            runtime.findings,

        )

    with k3:

        kpi(

            "Critical",

            runtime.critical,

        )

    with k4:

        kpi(

            "Medium",

            runtime.medium,

        )

    with k5:

        kpi(

            "Low",

            runtime.low,

        )

    st.divider()

    #
    # Runtime Workspace
    #

    left, right = st.columns([3, 2])

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

    show_footer()

