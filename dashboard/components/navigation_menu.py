import streamlit as st


def page(title, page_name):

    if st.button(
        title,
        use_container_width=True,
        key=f"page_{page_name}"
    ):
        st.session_state.page = page_name
        st.rerun()


def show():

    st.markdown("# EQMP")

    st.caption("Enterprise Navigation")

    st.divider()

    st.markdown("### Executive Workspace")

    page("🏠 Dashboard", "dashboard")

    page("🛡 Assessment", "assessment")

    page("📦 Inventory", "inventory")

    page("📊 Reports", "reports")

    page("🧭 Migration Planner", "migration")

    st.divider()

    st.markdown("### Engineering Workspace")

    page("💻 Repository Explorer", "repository")

    st.button(
        "🏗 Architecture",
        disabled=True,
        use_container_width=True,
    )

    st.button(
        "⚙ Developer Portal",
        disabled=True,
        use_container_width=True,
    )

    st.divider()

    st.markdown("### Research Centre")

    page("📚 Research Notes", "research")

    st.button(
        "📄 Publications",
        disabled=True,
        use_container_width=True,
    )

    st.divider()

    st.markdown("### Platform")

    page("ℹ About EQMP", "about")

