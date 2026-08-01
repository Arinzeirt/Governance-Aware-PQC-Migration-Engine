import streamlit as st


NAVIGATION = {

    "ENET TECHNOLOGIES": [

        ("Dashboard", "dashboard"),
        ("Assessment", "assessment"),
        ("Repository", "repository"),
        ("Research Centre", "research"),
        ("About", "about"),

    ]

}


def show():

    with st.sidebar:

        st.markdown(
            """
# ENET TECHNOLOGIES

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
                    key=f"nav_{page}"
                ):

                    st.session_state.page = page

                    st.rerun()

        st.divider()

        st.caption("Version 2.0")
        st.caption("© Enet Technologies")
