import streamlit as st


def show():

    st.markdown(
        """
        <style>

        .eqmp-nav {
            display:flex;
            align-items:center;
            justify-content:space-between;
            padding:10px 0 14px 0;
        }

        .eqmp-brand {
            font-size:1.05rem;
            font-weight:800;
            letter-spacing:-0.02em;
        }

        .eqmp-nav-links {
            display:flex;
            align-items:center;
            gap:8px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    left, login, frameworks, research, assessment = st.columns(
        [5, 1, 1, 1, 1.55],
        gap="small",
    )

    with left:

        if st.button(
            "EQMP",
            key="nav_home",
            use_container_width=False,
        ):

            st.session_state.page = "landing"
            st.rerun()

    with login:

        if st.button(
            "Login",
            key="nav_login",
            use_container_width=True,
        ):

            st.session_state[
                "eqmp_login_requested"
            ] = True

            st.rerun()

    with frameworks:

        if st.button(
            "Frameworks",
            key="nav_frameworks",
            use_container_width=True,
        ):

            st.session_state.page = "frameworks"
            st.rerun()

    with research:

        if st.button(
            "Research",
            key="nav_research",
            use_container_width=True,
        ):

            st.session_state.page = "research"
            st.rerun()

    with assessment:

        if st.button(
            "Enterprise Assessment",
            key="nav_assessment",
            type="primary",
            use_container_width=True,
        ):

            st.session_state.page = "enterprise_assessment"
            st.rerun()
