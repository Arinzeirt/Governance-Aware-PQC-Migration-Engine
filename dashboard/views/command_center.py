import streamlit as st


def show():

    # =========================================================
    # Authentication guard
    # =========================================================

    if not st.session_state.get(
        "eqmp_authenticated",
        False,
    ):

        st.session_state.page = "login"
        st.rerun()

        return

    # =========================================================
    # Current Position
    # =========================================================

    st.markdown(
        """
<div style="
    margin-bottom:10px;
    font-size:0.68rem;
    letter-spacing:1.4px;
    font-weight:700;
    color:#7F91A6;
">
CURRENT POSITION
</div>
""",
        unsafe_allow_html=True,
    )

    risk, governance, accountability, migration_status = st.columns(
        4,
        gap="small",
    )

    cards = [
        (
            risk,
            "QUANTUM RISK",
            "Elevated",
            "Requires attention",
        ),
        (
            governance,
            "GOVERNANCE",
            "Attention",
            "Decision controls need review",
        ),
        (
            accountability,
            "ACCOUNTABILITY",
            "3 Open",
            "Actions requiring ownership",
        ),
        (
            migration_status,
            "MIGRATION",
            "Not Started",
            "Planning has not been established",
        ),
    ]

    for column, label, value, description in cards:

        with column:

            st.markdown(
                f"""
<div style="
    border:1px solid rgba(255,255,255,.10);
    border-radius:8px;
    padding:12px 11px;
    min-height:74px;
">

<div style="
    font-size:0.62rem;
    letter-spacing:1.1px;
    color:#7F91A6;
    font-weight:700;
    margin-bottom:8px;
">
{label}
</div>

<div style="
    font-size:0.88rem;
    font-weight:750;
    color:#F5F7FA;
    margin-bottom:5px;
">
{value}
</div>

<div style="
    font-size:0.64rem;
    line-height:1.35;
    color:#718096;
">
{description}
</div>

</div>
""",
                unsafe_allow_html=True,
            )

    # =========================================================
    # Recent Governance Actions
    # =========================================================

    st.markdown(
        '<div style="height:20px"></div>',
        unsafe_allow_html=True,
    )

    actions_column, priority_column = st.columns(
        [1.55, 1],
        gap="medium",
    )

    with actions_column:

        st.markdown(
            """
<div style="
    font-size:0.82rem;
    font-weight:750;
    color:#F5F7FA;
    margin-bottom:9px;
">
Recent Governance Actions
</div>
""",
            unsafe_allow_html=True,
        )

        actions = [
            (
                "Assign PQC migration owner",
                "Owner: Security Leadership",
                "Open",
            ),
            (
                "Review cryptographic inventory",
                "Owner: Security",
                "Open",
            ),
            (
                "Define migration decision authority",
                "Owner: Executive",
                "Pending",
            ),
        ]

        for action, owner, status in actions:

            st.markdown(
                f"""
<div style="
    border:1px solid rgba(255,255,255,.10);
    border-radius:7px;
    padding:10px 11px;
    margin-bottom:8px;
">

<div style="
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:10px;
">

<span style="
    font-size:0.69rem;
    font-weight:650;
    color:#D5DCE5;
">
{action}
</span>

<span style="
    font-size:0.60rem;
    color:#718096;
">
{status}
</span>

</div>

<div style="
    margin-top:7px;
    font-size:0.58rem;
    color:#718096;
">
{owner}
</div>

</div>
""",
                unsafe_allow_html=True,
            )

    # =========================================================
    # Priority Attention
    # =========================================================

    with priority_column:

        st.markdown(
            """
<div style="
    font-size:0.82rem;
    font-weight:750;
    color:#F5F7FA;
    margin-bottom:9px;
">
Priority Attention
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div style="
    border:1px solid rgba(47,129,247,.55);
    border-left:2px solid #2F81F7;
    border-radius:7px;
    padding:12px 11px;
    min-height:86px;
">

<div style="
    font-size:0.70rem;
    font-weight:750;
    color:#D5DCE5;
    margin-bottom:7px;
">
Governance ownership gap
</div>

<div style="
    font-size:0.62rem;
    line-height:1.45;
    color:#8FA1B5;
">
The organisation currently has no confirmed
post-quantum migration owner. Establishing
decision ownership is the immediate governance priority.
</div>

</div>
""",
            unsafe_allow_html=True,
        )

    # =========================================================
    # Governance Snapshot
    # =========================================================

    st.markdown(
        '<div style="height:10px"></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div style="
    margin-top:8px;
    margin-bottom:10px;
    font-size:0.68rem;
    letter-spacing:1.4px;
    font-weight:700;
    color:#7F91A6;
">
GOVERNANCE SNAPSHOT
</div>
""",
        unsafe_allow_html=True,
    )

    snapshot_left, snapshot_right = st.columns(
        2,
        gap="medium",
    )

    snapshot_items = [
        (
            "PQC STRATEGY",
            "Not Started",
        ),
        (
            "MIGRATION OWNERSHIP",
            "Not Assigned",
        ),
        (
            "EXECUTIVE SPONSORSHIP",
            "Under Consideration",
        ),
        (
            "CRYPTOGRAPHIC RISK",
            "Not Integrated",
        ),
    ]

    for index, (label, value) in enumerate(
        snapshot_items
    ):

        column = (
            snapshot_left
            if index % 2 == 0
            else snapshot_right
        )

        with column:

            st.markdown(
                f"""
<div style="
    border:1px solid rgba(255,255,255,.08);
    border-radius:7px;
    padding:9px 11px;
    margin-bottom:7px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:15px;
">

<span style="
    font-size:0.60rem;
    letter-spacing:.8px;
    color:#7F91A6;
    font-weight:700;
">
{label}
</span>

<span style="
    font-size:0.66rem;
    color:#D5DCE5;
    text-align:right;
">
{value}
</span>

</div>
""",
                unsafe_allow_html=True,
            )
