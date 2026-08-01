import streamlit as st


NAVIGATION = {

    "EXECUTIVE WORKSPACE": [

        ("Dashboard", "dashboard"),
        ("Assessment", "assessment"),
        ("Inventory", "inventory"),
        ("Reports", "reports"),
        ("Migration Planner", "migration"),

    ],

    "ENGINEERING": [

        ("Repository Explorer", "repository"),
        ("Architecture", "repository"),
        ("Developer Portal", "repository"),

    ],

    "RESEARCH": [

        ("Research Centre", "research"),
        ("Research Notes", "research"),
        ("Frameworks & Publications", "research"),

    ],

    "ABOUT": [

        ("About EQMP", "about"),
        ("Research Portfolio", "about"),

    ]

}


def show():

    with st.sidebar:

        st.markdown(
            """
# ENET

Enterprise Quantum Migration Platform
"""
        )

        st.divider()

        for section, pages in NAVIGATION.items():

            st.caption(section)

            for title, page in pages:

                if st.button(
                    title,
                    use_container_width=True,
                    key=f"nav_{page}_{title}"
                ):

                    st.session_state.page = page

                    st.rerun()

            st.divider()

        st.caption("Version 2.0 DEV")
        st.caption("© Enet Technologies")
