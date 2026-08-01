import streamlit as st

from utils.asset_registry import load_assets


def show():

    assets = list(load_assets().values())

    st.title("Knowledge Library")

    st.caption(
        "Enterprise Quantum Migration Platform • Research Knowledge Base"
    )

    st.divider()

    frameworks = [
        a for a in assets
        if a["type"] == "Framework"
    ]

    notes = [
        a for a in assets
        if a["type"] == "Research Note"
    ]

    publications = [
        a for a in assets
        if a["type"] == "Publication"
    ]

    case_studies = [
        a for a in assets
        if a["type"] == "Case Study"
    ]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Frameworks", len(frameworks))

    with col2:
        st.metric("Research Notes", len(notes))

    with col3:
        st.metric("Publications", len(publications))

    with col4:
        st.metric("Case Studies", len(case_studies))

    st.divider()

    st.subheader("Recently Added")

    recent = sorted(
        assets,
        key=lambda asset: asset["id"],
        reverse=True,
    )[:10]

    for asset in recent:

        with st.container(border=True):

            st.caption(
                f"{asset['type']} • {asset['id']}"
            )

            st.markdown(
                f"### {asset['title']}"
            )

            description = asset.get(
                "description",
                "",
            )

            if description:
                st.caption(description)
