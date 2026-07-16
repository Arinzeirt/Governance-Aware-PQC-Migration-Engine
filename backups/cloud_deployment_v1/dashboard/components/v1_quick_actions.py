import streamlit as st


def show():

    c1, c2, c3 = st.columns(3)

    #
    # Executive Report
    #

    with c1:

        if st.button(
            "📄 Executive Report",
            use_container_width=True,
        ):

            st.toast("Executive Report generated.")

    #
    # Technical Inventory
    #

    with c2:

        if st.button(
            "🗂 Technical Inventory",
            use_container_width=True,
        ):

            st.toast("Opening technical inventory...")

    #
    # Migration Planner
    #

    with c3:

        if st.button(
            "🚀 Launch Migration Planner",
            use_container_width=True,
        ):

            st.info(
                "Enterprise Edition Feature.\n\n"
                "Migration Planner will be available in the Enterprise release."
            )

