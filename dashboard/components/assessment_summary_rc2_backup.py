import streamlit as st

from pathlib import Path

from engine.runtime import runtime
from engine.session import session
from engine.runner import runner


def calculate_risk():

    if runtime.critical > 0:
        return "HIGH", "Immediate"

    if runtime.medium > 0:
        return "MEDIUM", "Planned"

    return "LOW", "Monitor"


def readiness_score():

    score = 100

    score -= runtime.critical * 20
    score -= runtime.medium * 8
    score -= runtime.low * 2

    return max(score, 0)


def readiness_label(score):

    if score >= 90:
        return "Excellent Readiness"

    if score >= 75:
        return "Good Readiness"

    if score >= 60:
        return "Moderate Readiness"

    return "Immediate Action Required"


def discovery_outcome(risk):

    if risk == "HIGH":

        return (

            "Immediate Migration Planning",

            "Critical cryptographic assets have been identified. Governance-led migration planning should begin immediately.",

        )

    if risk == "MEDIUM":

        return (

            "Migration Planning Required",

            "Migration planning should begin with business-critical services and external-facing systems.",

        )

    return (

        "Continue Governance Monitoring",

        "Maintain governance oversight and continue periodic discovery assessments.",

    )


def show():

    risk, migration = calculate_risk()

    score = readiness_score()

    outcome, explanation = discovery_outcome(risk)

    #
    # Discovery Complete
    #

    with st.container(border=True):

        left, right = st.columns([5, 1])

        with left:

            st.markdown(
                "# Enterprise Discovery Complete"
            )

            st.caption(
                "Enterprise Quantum Migration Platform"
            )

        with right:

            st.metric(
                "Status",
                "Completed"
            )

    st.write("")

    #
    # Executive Metrics
    #

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Readiness",
            f"{score}%"
        )

        st.caption(
            readiness_label(score)
        )

    with c2:

        st.metric(
            "Risk",
            risk
        )

    with c3:

        st.metric(
            "Priority",
            migration
        )

    with c4:

        st.metric(
            "Duration",
            runtime.elapsed()
        )

    st.divider()

    #
    # Discovery Outcome
    #

    st.markdown(
        "### Discovery Outcome"
    )

    st.info(
        f"""
**Outcome**

{outcome}

{explanation}
"""
    )

    st.divider()

    #
    # Discovery Metadata
    #

    st.markdown(
        "### Discovery Metadata"
    )

    m1, m2, m3 = st.columns(3)

    with m1:

        st.metric(
            "Repository",
            runtime.repository_name or "-"
        )

    with m2:

        st.metric(
            "Files Scanned",
            runtime.total_files
        )

    with m3:

        st.metric(
            "Session",
            session.session_id
        )

    st.divider()

    #
    # Discovery Statistics
    #

    s1, s2, s3 = st.columns(3)

    with s1:

        st.metric(
            "Assets Identified",
            runtime.findings
        )

    with s2:

        st.metric(
            "High Risk",
            runtime.critical
        )

    with s3:

        st.metric(
            "Medium Risk",
            runtime.medium
        )

    st.divider()
    #
    # Cryptographic Assets
    #

    st.markdown(
        "### Cryptographic Assets Identified"
    )

    if runtime.discoveries:

        displayed = set()

        cols = st.columns(3)

        index = 0

        for item in runtime.discoveries:

            if item["title"] in displayed:
                continue

            displayed.add(item["title"])

            with cols[index % 3]:

                with st.container(border=True):

                    st.markdown(
                        f"#### {item['title']}"
                    )

                    st.caption(
                        f"Risk Level: {item['severity']}"
                    )

            index += 1

    else:

        st.info(
            "No cryptographic assets were identified during this assessment."
        )

    st.divider()

    #
    # Next Phase
    #

    st.markdown(
        "### Next Phase"
    )

    st.success(
        """
Enterprise Discovery has completed successfully.

A governance-aware cryptographic inventory has been generated.

The environment is now ready for migration planning,
prioritisation and governance review.

Continue to the Migration workspace to review the
inventory and prepare a migration strategy.
"""
    )

    st.divider()

    #
    # Actions
    #

    c1, c2, c3 = st.columns(3)

    with c1:

        if st.button(
            "Continue to Migration",
            type="primary",
            use_container_width=True,
        ):

            st.session_state.page = "repository"

            st.rerun()

    with c2:

        report = Path(
            "reports/pqc_executive_report.pdf"
        )

        if report.exists():

            with open(report, "rb") as f:

                st.download_button(

                    "Export Executive Report",

                    data=f,

                    file_name="EQMP_Executive_Report.pdf",

                    mime="application/pdf",

                    use_container_width=True,

                )

        else:

            st.button(

                "Export Executive Report",

                disabled=True,

                use_container_width=True,

            )

    with c3:

        inventory = Path(
            "inventory.json"
        )

        if inventory.exists():

            with open(inventory, "rb") as f:

                st.download_button(

                    "Download Inventory",

                    data=f,

                    file_name="inventory.json",

                    mime="application/json",

                    use_container_width=True,

                )

        else:

            st.button(

                "Download Inventory",

                disabled=True,

                use_container_width=True,

            )

    st.divider()

    st.caption(
        "Enterprise Discovery is the first phase of the governance-aware post-quantum migration lifecycle. Continue to the Migration workspace to review readiness, inventory, and migration priorities."
    )

    st.write("")

    if st.button(
        "Start New Discovery",
        use_container_width=True,
    ):

        runtime.new_assessment()

        session.reset()

        runner.running = False

        st.rerun()

