import streamlit as st


def show():

    if not st.session_state.get(
        "eqmp_authenticated",
        False,
    ):

        st.session_state.page = "login"
        st.rerun()

    # =========================================================
    # Migration Position
    # =========================================================

    st.markdown(
        """
<div style="
    font-size:0.68rem;
    letter-spacing:1.4px;
    color:#7F91A6;
    font-weight:700;
    margin-bottom:9px;
">
MIGRATION POSITION
</div>
""",
        unsafe_allow_html=True,
    )

    position_1, position_2, position_3, position_4 = st.columns(
        4,
        gap="small",
    )

    positions = [

        (
            position_1,
            "MIGRATION STATUS",
            "Not Started",
            "Programme has not been established",
        ),

        (
            position_2,
            "READINESS",
            "0%",
            "Migration readiness not yet established",
        ),

        (
            position_3,
            "PRIORITY EXPOSURE",
            "High",
            "Priority systems require investigation",
        ),

        (
            position_4,
            "TARGET COMPLETION",
            "Not Established",
            "Migration timeline has not been defined",
        ),

    ]

    for column, label, value, description in positions:

        with column:

            st.markdown(
                f"""
<div style="
    border:1px solid rgba(255,255,255,.10);
    border-radius:8px;
    padding:13px;
    min-height:88px;
">

<div style="
    font-size:0.64rem;
    letter-spacing:1px;
    color:#7F91A6;
    font-weight:700;
    margin-bottom:7px;
">
{label}
</div>

<div style="
    font-size:1.02rem;
    font-weight:750;
    color:#F5F7FA;
    margin-bottom:5px;
">
{value}
</div>

<div style="
    font-size:0.72rem;
    color:#718096;
    line-height:1.4;
">
{description}
</div>

</div>
""",
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div style="height:20px"></div>',
        unsafe_allow_html=True,
    )

    # =========================================================
    # Programme + Governance
    # =========================================================

    left, right = st.columns(
        [1.65, 1],
        gap="large",
    )

    # ---------------------------------------------------------
    # Migration Programme
    # ---------------------------------------------------------

    with left:

        st.markdown(
            """
<div style="
    font-size:0.92rem;
    font-weight:750;
    margin-bottom:9px;
">
Migration Programme
</div>
""",
            unsafe_allow_html=True,
        )

        stages = [

            (
                "01",
                "Inventory & Dependency Analysis",
                "Establish the cryptographic assets, systems "
                "and dependencies requiring migration.",
            ),

            (
                "02",
                "Prioritisation",
                "Determine which systems, data and services "
                "require migration first.",
            ),

            (
                "03",
                "Architecture & Algorithm Decisions",
                "Define target cryptographic architecture, "
                "algorithms and implementation strategy.",
            ),

            (
                "04",
                "Pilot & Validation",
                "Validate migration approaches against "
                "representative enterprise workloads.",
            ),

            (
                "05",
                "Production Migration",
                "Execute controlled migration across "
                "prioritised enterprise environments.",
            ),

            (
                "06",
                "Verification & Assurance",
                "Confirm migration outcomes, governance "
                "controls and residual exposure.",
            ),

        ]

        for number, title, description in stages:

            st.markdown(
                f"""
<div style="
    border:1px solid rgba(255,255,255,.10);
    border-radius:8px;
    padding:11px 13px;
    margin-bottom:8px;
">

<div style="
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:5px;
">

<div style="
    font-size:0.82rem;
    font-weight:700;
">

<span style="
    color:#2F81F7;
    margin-right:8px;
">
{number}
</span>

{title}

</div>

<div style="
    font-size:0.65rem;
    color:#718096;
">
Not Started
</div>

</div>

<div style="
    font-size:0.72rem;
    color:#8FA1B5;
    line-height:1.4;
">
{description}
</div>

</div>
""",
                unsafe_allow_html=True,
            )

    # ---------------------------------------------------------
    # Governance & Accountability
    # ---------------------------------------------------------

    with right:

        st.markdown(
            """
<div style="
    font-size:0.92rem;
    font-weight:750;
    margin-bottom:9px;
">
Governance & Accountability
</div>
""",
            unsafe_allow_html=True,
        )

        governance_items = [

            (
                "Executive Owner",
                "Not Assigned",
            ),

            (
                "Migration Programme Owner",
                "Not Assigned",
            ),

            (
                "Technical Owner",
                "Not Assigned",
            ),

            (
                "Open Decisions",
                "3",
            ),

            (
                "Overdue Actions",
                "0",
            ),

        ]

        for label, value in governance_items:

            st.markdown(
                f"""
<div style="
    border:1px solid rgba(255,255,255,.10);
    border-radius:8px;
    padding:12px 13px;
    margin-bottom:8px;
">

<div style="
    font-size:0.67rem;
    color:#7F91A6;
    text-transform:uppercase;
    letter-spacing:.7px;
    margin-bottom:5px;
">
{label}
</div>

<div style="
    font-size:0.84rem;
    font-weight:700;
">
{value}
</div>

</div>
""",
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div style="height:18px"></div>',
        unsafe_allow_html=True,
    )

    # =========================================================
    # Migration Priorities
    # =========================================================

    st.markdown(
        """
<div style="
    font-size:0.92rem;
    font-weight:750;
    margin-bottom:9px;
">
Migration Priorities
</div>
""",
        unsafe_allow_html=True,
    )

    priorities = [

        (
            "01",
            "Cryptographic inventory",
            "Not Started",
            "Security",
        ),

        (
            "02",
            "Critical systems",
            "Not Assessed",
            "Architecture",
        ),

        (
            "03",
            "PKI & certificates",
            "Not Assessed",
            "Infrastructure",
        ),

        (
            "04",
            "PQC architecture",
            "Not Established",
            "Engineering",
        ),

    ]

    header = st.columns(
        [0.55, 2, 1, 1],
        gap="small",
    )

    for column, value in zip(
        header,
        ["Priority", "Area", "Status", "Owner"],
    ):

        with column:

            st.markdown(
                f"""
<div style="
    color:#7F91A6;
    font-size:0.65rem;
    font-weight:700;
    letter-spacing:.7px;
    text-transform:uppercase;
    padding-bottom:7px;
">
{value}
</div>
""",
                unsafe_allow_html=True,
            )

    for priority, area, status, owner in priorities:

        columns = st.columns(
            [0.55, 2, 1, 1],
            gap="small",
        )

        values = [
            priority,
            area,
            status,
            owner,
        ]

        for column, value in zip(
            columns,
            values,
        ):

            with column:

                st.markdown(
                    f"""
<div style="
    border-top:1px solid rgba(255,255,255,.07);
    padding:10px 0;
    font-size:0.72rem;
    color:#AEBCCE;
">
{value}
</div>
""",
                    unsafe_allow_html=True,
                )

    st.markdown(
        '<div style="height:18px"></div>',
        unsafe_allow_html=True,
    )

    # =========================================================
    # Next Action
    # =========================================================

    st.markdown(
        """
<div style="
    border-left:3px solid #2F81F7;
    border-radius:0 7px 7px 0;
    padding:13px 15px;
    background:rgba(47,129,247,.05);
    margin-bottom:10px;
">

<div style="
    font-size:0.65rem;
    letter-spacing:1px;
    color:#7F91A6;
    font-weight:700;
    margin-bottom:5px;
">
NEXT ACTION
</div>

<div style="
    font-size:0.92rem;
    font-weight:750;
    margin-bottom:4px;
">
Begin Migration Programme
</div>

<div style="
    font-size:0.74rem;
    color:#8FA1B5;
    line-height:1.4;
">
Establish the evidence, ownership and priorities required
before migration execution begins.
</div>

</div>
""",
        unsafe_allow_html=True,
    )

    if st.button(
        "Begin Migration Programme →",
        type="primary",
        use_container_width=True,
        key="migration_begin",
    ):

        st.session_state[
            "migration_programme_requested"
        ] = True

        st.info(
            "Migration programme initiation will be connected "
            "to the enterprise migration workflow."
        )

    st.markdown(
        '<div style="height:6px"></div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "Return to Command Center",
        key="migration_return",
    ):

        st.session_state.page = "command_center"
        st.rerun()
