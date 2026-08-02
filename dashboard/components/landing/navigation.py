import streamlit as st


def show():

    left, right = st.columns([2, 5])

    with left:

        st.markdown(
            """
### <span style="color:#2F80ED;">ENET</span>

<span style="color:#AEB7C5;font-size:12px;letter-spacing:1px;">
TECHNOLOGIES
</span>
""",
            unsafe_allow_html=True,
        )

    with right:

        c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 2])

        with c1:
            st.button(
                "Research",
                use_container_width=True,
                key="nav_research",
            )

        with c2:
            st.button(
                "Frameworks",
                use_container_width=True,
                key="nav_frameworks",
            )

        with c3:
            st.button(
                "About",
                use_container_width=True,
                key="nav_about",
            )

        with c4:
            st.button(
                "Contact",
                use_container_width=True,
                key="nav_contact",
            )

        with c5:
            st.button(
                "Start Basic Assessment",
                type="primary",
                use_container_width=True,
                key="nav_start_assessment",
            )

    st.divider()
