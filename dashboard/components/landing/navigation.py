import streamlit as st


def show():

    #
    # Clicking the logo returns to the landing page.
    #
    if "home" in st.query_params:

        st.session_state.page = "landing"

        st.query_params.clear()

        st.rerun()

    left, right = st.columns([2, 5])

    with left:

        st.markdown(
            """
<a href="?home=true" target="_self" style="text-decoration:none;">

<h3 style="
margin:0;
color:#2F80ED;
font-weight:700;
">
ENET
</h3>

<div style="
color:#AEB7C5;
font-size:12px;
letter-spacing:1px;
margin-top:-2px;
">
TECHNOLOGIES
</div>

</a>
""",
            unsafe_allow_html=True,
        )

    with right:

        c1, c2, c3, c4 = st.columns([1, 1, 1, 2])

        with c1:

            if st.button(
                "Research",
                use_container_width=True,
                key="nav_research",
            ):

                st.session_state.page = "research"
                st.rerun()

        with c2:

            if st.button(
                "Frameworks",
                use_container_width=True,
                key="nav_frameworks",
            ):

                st.session_state.page = "frameworks"
                st.rerun()

        with c3:

            if st.button(
                "About",
                use_container_width=True,
                key="nav_about",
            ):

                st.session_state.page = "about"
                st.rerun()

        with c4:

            if st.button(
                "Start Enterprise Assessment",
                type="primary",
                use_container_width=True,
                key="nav_start_assessment",
            ):

                st.session_state.page = "enterprise_assessment"
                st.rerun()

    st.divider()

