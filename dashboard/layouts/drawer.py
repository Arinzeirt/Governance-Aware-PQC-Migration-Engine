import streamlit as st


MENU = [

    ("COMMAND CENTER", None),

    ("Dashboard", "dashboard"),

    (None, None),

    ("DISCOVERY", None),

    ("Assessment", "assessment"),

    ("Inventory", "inventory"),

    ("Repository Explorer", "repository"),

    (None, None),

    ("GOVERNANCE", None),

    ("Migration Orchestrator", "migration"),

    ("Reports", "reports"),

    (None, None),

    ("KNOWLEDGE", None),

    ("Research Centre", "research"),

    (None, None),

    ("SYSTEM", None),

    ("About", "about"),

]


def navigation_button(title, page):

    active = (
        st.session_state.page == page
    )

    if active:

        st.markdown(
            f"""
<div style="
background:#2563EB;
padding:10px 14px;
border-radius:10px;
border-left:4px solid white;
font-weight:600;
color:white;
margin-bottom:8px;
">
{title}
</div>
""",
            unsafe_allow_html=True,
        )

        return

    if st.button(
        title,
        key=f"nav_{page}",
        use_container_width=True,
    ):

        st.session_state.page = page

        st.session_state.drawer_open = False

        st.rerun()


def show():

    st.markdown("### Navigation")

    for title, page in MENU:

        if title is None:

            st.write("")

            continue

        if page is None:

            st.caption(title)

            continue

        navigation_button(
            title,
            page
        )

    st.divider()

    st.caption(
        "Technology Preview v2.0 RC1"
    )

    st.caption(
        "© Enet Technologies"
    )

