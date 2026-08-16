import streamlit as st


WORKSPACES = [
    ("Command Center", "command_center"),
    ("Discovery", "discovery"),
    ("Marketplace", "marketplace"),
    ("Migration", "migration"),
]


def _navigate(page):
    st.session_state.page = page
    st.rerun()


def show(
    page_title,
    page_subtitle,
    content,
):
    """
    Shared authenticated EQMP application shell.

    Provides:
    - page header
    - LIVE indicator
    - role-aware Settings access
    - four primary workspace navigation items
    - authenticated application footer
    """

    if not st.session_state.get(
        "eqmp_authenticated",
        False,
    ):

        st.session_state.page = "login"
        st.rerun()

        return

    user_role = st.session_state.get(
        "eqmp_user_role",
        "user",
    )

    organisation = st.session_state.get(
        "eqmp_organisation",
        "EQMP Test Organisation",
    )

    role_label = (
        "Administrator"
        if user_role == "admin"
        else "Organisation User"
    )

    # =========================================================
    # Shared Header
    # =========================================================

    header_left, header_right = st.columns(
        [8.4, 1.6],
        gap="small",
    )

    with header_left:

        st.markdown(
            f"""
<div style="
    margin-bottom:16px;
">

<div style="
    font-size:1.75rem;
    font-weight:800;
    line-height:1.1;
    color:#F5F7FA;
">
{page_title}
</div>

<div style="
    color:#8FA1B5;
    font-size:0.86rem;
    margin-top:5px;
">
{page_subtitle}
</div>

<div style="
    color:#68778A;
    font-size:0.62rem;
    margin-top:7px;
">
{organisation} · {role_label}
</div>

</div>
""",
            unsafe_allow_html=True,
        )

    with header_right:

        controls = st.columns(
            [1.2, 0.8],
            gap="small",
        )

        with controls[0]:

            st.markdown(
                """
<div style="
    display:flex;
    justify-content:flex-end;
    align-items:center;
    gap:7px;
    margin-top:8px;
">

<div class="eqmp-shell-live-dot"></div>

<span style="
    font-size:0.66rem;
    color:#8FA1B5;
    letter-spacing:.5px;
">
LIVE
</span>

</div>

<style>

.eqmp-shell-live-dot {
    width:7px;
    height:7px;
    border-radius:50%;
    background:#22C55E;
    box-shadow:0 0 0 rgba(34,197,94,.55);
    animation:eqmp-shell-live-pulse 1.8s infinite;
}

@keyframes eqmp-shell-live-pulse {

    0% {
        box-shadow:0 0 0 0 rgba(34,197,94,.55);
    }

    70% {
        box-shadow:0 0 0 6px rgba(34,197,94,0);
    }

    100% {
        box-shadow:0 0 0 0 rgba(34,197,94,0);
    }

}

</style>
""",
                unsafe_allow_html=True,
            )

        with controls[1]:

            if st.button(
                "⚙",
                help="Settings",
                key="eqmp_shell_settings",
            ):

                _navigate("settings")

    # =========================================================
    # Workspace Navigation
    # =========================================================

    nav_columns = st.columns(
        4,
        gap="small",
    )

    for column, (
        label,
        route,
    ) in zip(
        nav_columns,
        WORKSPACES,
    ):

        with column:

            active = (
                st.session_state.page == route
            )

            if st.button(
                label,
                key=f"eqmp_shell_nav_{route}",
                type=(
                    "primary"
                    if active
                    else "secondary"
                ),
                use_container_width=True,
            ):

                _navigate(route)

    st.markdown(
        """
<div style="
    height:18px;
    border-bottom:1px solid rgba(255,255,255,.07);
    margin-bottom:20px;
">
</div>
""",
        unsafe_allow_html=True,
    )

    # =========================================================
    # Page Content
    # =========================================================

    content()

    # =========================================================
    # Shared Application Footer
    # =========================================================

    st.markdown(
        """
<div style="
    border-top:1px solid rgba(255,255,255,.08);
    margin-top:28px;
    padding:12px 0 4px 0;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:20px;
">

<div>

<div style="
    font-size:0.67rem;
    font-weight:750;
    color:#AEBCCE;
">
EQMP
</div>

<div style="
    font-size:0.55rem;
    color:#68778A;
    margin-top:3px;
">
Enterprise Quantum Migration Platform
</div>

</div>

<div style="
    text-align:right;
">

<div style="
    font-size:0.56rem;
    color:#22C55E;
">
● System Operational
</div>

<div style="
    font-size:0.52rem;
    color:#596779;
    margin-top:3px;
">
Master Environment
</div>

</div>

</div>
""",
        unsafe_allow_html=True,
    )
