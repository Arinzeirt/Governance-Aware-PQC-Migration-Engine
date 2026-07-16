import streamlit as st


def item(title, page):

    if st.button(
        title,
        use_container_width=True,
        key=page
    ):
        st.session_state.page = page
        st.rerun()


def show():

    st.markdown("## EQMP")

    st.markdown("### Executive Workspace")

    item("🏠 Dashboard","dashboard")
    item("🛡 Assessment","assessment")
    item("📊 Inventory","inventory")
    item("📈 Reports","reports")
    item("🧭 Migration Planner","migration")

    st.divider()

    st.markdown("### Engineering Workspace")

    item("💻 Repository Explorer","repository")

    st.button(
        "🏗 Architecture",
        disabled=True,
        use_container_width=True
    )

    st.button(
        "⚙ Developer Portal",
        disabled=True,
        use_container_width=True
    )

    st.divider()

    st.markdown("### Research Centre")

    item("📚 Research Notes","research")

    st.button(
        "📄 Publications",
        disabled=True,
        use_container_width=True
    )

    st.divider()

    st.markdown("### Platform")

    item("ℹ About EQMP","about")

