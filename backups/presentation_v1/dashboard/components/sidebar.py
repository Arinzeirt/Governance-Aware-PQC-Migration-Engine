import streamlit as st


def show_sidebar():

    with st.sidebar:

        st.image(
            "dashboard/assets/enet_logo.png",
            width=72
        )

        st.markdown("## EQMP")

        st.caption("Enterprise Edition")

        st.divider()

        st.markdown("### Navigation")

        st.button("🏠  Command Center", use_container_width=True)

        st.button("📋  Assessments", disabled=True, use_container_width=True)

        st.button("🗂️  Inventory", disabled=True, use_container_width=True)

        st.button("⚠️  Risks", disabled=True, use_container_width=True)

        st.button("🛡️  Compliance", disabled=True, use_container_width=True)

        st.button("🧭  Roadmap", disabled=True, use_container_width=True)

        st.button("📄  Reports", disabled=True, use_container_width=True)

        st.button("⚙️  Settings", disabled=True, use_container_width=True)

        st.divider()

        st.caption("EQMP Version 1")

        st.caption("Powered by Enet Technologies")
