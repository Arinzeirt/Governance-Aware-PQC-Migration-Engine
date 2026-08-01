import os

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from engine.runtime import runtime
from engine.session import session

from components.workflow_ribbon import show as show_workflow_ribbon

#
# Enterprise Design System
#
from design_system.components import (
    hero,
    panel,
    metric,
    badge,
    section,
)


# -------------------------------------------------------
# Discovery Card
# -------------------------------------------------------

def discovery_card(item):

    with panel():

        st.markdown(
            f"### {item['title']}"
        )

        st.caption(
            os.path.basename(item["file"])
        )

        badge(
            item["severity"],
            (
                "critical"
                if item["severity"] == "High"
                else "warning"
                if item["severity"] == "Medium"
                else "success"
            ),
        )


# -------------------------------------------------------
# Activity Card
# -------------------------------------------------------

def activity_card(item):

    with panel():

        left, right = st.columns([1, 5])

        with left:

            st.caption(item["time"])

        with right:

            st.write(item["message"])


# -------------------------------------------------------
# Runtime Dashboard
# -------------------------------------------------------

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
    # Hero
    #

    hero(

        title="Enterprise Discovery",

        subtitle=(
            "Discover cryptographic assets across enterprise "
            "systems and prepare governance-aware "
            "post-quantum migration."
        ),

        eyebrow="Enterprise Workspace",

        status=runtime.status,

    )

    #
    # Workflow
    #

    show_workflow_ribbon()

    st.write("")

    #
    # Runtime Overview
    #

    left, right = st.columns([2, 1], gap="large")

    with left:

        with panel(

            title="Runtime Activity",

            subtitle="Current enterprise discovery session.",

        ):

            st.progress(

                runtime.progress / 100,

                text=f"{runtime.progress}% Complete",

            )

            st.write("")

            if runtime.current_file:

                st.code(

                    os.path.basename(
                        runtime.current_file
                    ),

                    language="text",

                )

            else:

                st.info(
                    "Waiting for assessment..."
                )

            c1, c2 = st.columns(2)

            with c1:

                metric(

                    title="Current Stage",

                    value=runtime.stage,

                    subtitle="Assessment workflow",

                )

            with c2:

                metric(

                    title="Elapsed",

                    value=runtime.elapsed(),

                    subtitle="Runtime duration",

                )

    with right:

        with panel(

            title="Repository Overview",

            subtitle="Current assessment target.",

        ):

            metric(

                title="Repository",

                value=repository or "-",

                subtitle="Assessment target",

            )

            metric(

                title="Type",

                value=runtime.repository_type or "-",

                subtitle="Repository type",

            )

            metric(

                title="Files",

                value=f"{runtime.files_scanned}/{runtime.total_files}",

                subtitle="Processed",

            )

            metric(

                title="Status",

                value=runtime.status,

                subtitle="Runtime",

            )

    st.write("")

    #
    # Enterprise Metrics
    #

    section(
        "Enterprise Metrics",
        "Live operational metrics from the current discovery session.",
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:

        metric(
            title="Files",
            value=f"{runtime.files_scanned}/{runtime.total_files}",
            subtitle="Processed",
        )

    with c2:

        metric(
            title="Findings",
            value=runtime.findings,
            subtitle="Assets identified",
        )

    with c3:

        metric(
            title="Critical",
            value=runtime.critical,
            subtitle="Immediate action",
            accent="critical",
        )

    with c4:

        metric(
            title="Medium",
            value=runtime.medium,
            subtitle="Planned migration",
            accent="warning",
        )

    with c5:

        metric(
            title="Low",
            value=runtime.low,
            subtitle="Monitor",
            accent="success",
        )

    st.write("")

    #
    # Discovery Workspace
    #

    left, right = st.columns([2, 2], gap="large")

    with left:

        section(
            "Live Discovery Feed",
            "Cryptographic assets identified during assessment.",
        )

        if runtime.discoveries:

            for item in runtime.discoveries[:10]:

                discovery_card(item)

        else:

            st.info("No cryptographic discoveries yet.")

    with right:

        section(
            "Enterprise Activity Timeline",
            "Assessment events generated by the runtime engine.",
        )

        if runtime.activity:

            for item in runtime.activity[:20]:

                activity_card(item)

        else:

            st.info("Assessment ready.")

    st.write("")

    #
    # Executive Summary
    #

    with panel(

        title="Executive Discovery Summary",

        subtitle="Current enterprise discovery outcome.",

    ):

        if runtime.running:

            st.info(
                "Enterprise discovery is currently executing. Inventory and migration intelligence are being generated."
            )

        else:

            st.success(
                "Enterprise discovery completed successfully."
            )

        a, b, c = st.columns(3)

        with a:

            metric(

                title="Assets",

                value=runtime.findings,

                subtitle="Discovered",

            )

        with b:

            metric(

                title="Stage",

                value=runtime.stage,

                subtitle="Workflow",

            )

        with c:

            metric(

                title="Progress",

                value=f"{runtime.progress}%",

                subtitle="Completion",

            )

    st.write("")
