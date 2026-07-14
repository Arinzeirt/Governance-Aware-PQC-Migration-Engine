import streamlit as st

from engine.runtime import runtime
from engine.session import session
from engine.runner import runner


def calculate_risk():

    if runtime.critical > 0:
        return "HIGH", "Required"

    if runtime.medium > 0:
        return "MEDIUM", "Recommended"

    return "LOW", "Not Required"


def show():

    st.success(

        "Assessment completed successfully."

    )

    st.markdown(

        "# Enterprise Assessment Summary"

    )

    #
    # Toolbar
    #

    left, middle, right = st.columns([2,2,2])

    with left:

        if st.button(

            "🔄 New Assessment",

            use_container_width=True,

            type="primary",

        ):

            runtime.new_assessment()

            session.reset()

            runner.running = False

            st.rerun()

    with middle:

        st.button(

            "📄 Export Report",

            use_container_width=True,

            disabled=True,

        )

    with right:

        st.button(

            "📊 Executive Summary",

            use_container_width=True,

            disabled=True,

        )

    st.divider()

    #
    # Statistics
    #

    risk, migration = calculate_risk()

    a, b, c, d = st.columns(4)

    with a:

        st.metric(

            "Findings",

            runtime.findings,

        )

    with b:

        st.metric(

            "Critical",

            runtime.critical,

        )

    with c:

        st.metric(

            "Risk",

            risk,

        )

    with d:

        st.metric(

            "Migration",

            migration,

        )

    st.divider()

    #
    # Discoveries
    #

    st.subheader(

        "Algorithms Detected"

    )

    if runtime.discoveries:

        displayed = set()

        for item in runtime.discoveries:

            if item["title"] not in displayed:

                st.markdown(

                    f"• **{item['title']}**"

                )

                displayed.add(

                    item["title"]

                )

    else:

        st.info(

            "No algorithms detected."

        )

    st.divider()

    #
    # Assessment Information
    #

    left, right = st.columns(2)

    with left:

        st.metric(

            "Repository",

            runtime.repository_name

            or "-",

        )

    with right:

        st.metric(

            "Assessment Duration",

            runtime.elapsed(),

        )

