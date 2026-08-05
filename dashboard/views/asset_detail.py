import streamlit as st

from components.asset_metadata import show as show_metadata
from components.related_assets import show as show_related
from components.breadcrumb import show as show_breadcrumb
from components.landing.footer import show as show_footer

from utils.asset_loader import load_asset


def show():

    asset_id = st.session_state.get("selected_asset")

    if not asset_id:
        st.warning("No asset selected.")
        return

    asset = load_asset(asset_id)

    if asset is None:
        st.error("Asset not found.")
        return

    origin = st.session_state.get(
        "asset_origin",
        "research",
    )

    if st.button("← Back to Research Centre"):

        st.session_state.page = origin
        st.rerun()

    show_breadcrumb(
        "Research Centre",
        asset["type"],
        asset["id"],
    )

    st.caption(
        f"{asset['type']} • {asset['id']}"
    )

    st.title(
        asset["title"]
    )

    show_metadata(
        asset.get("metadata", {})
    )

    st.divider()

    st.markdown(
        asset["content"]
    )

    metadata = asset.get("metadata", {})

    has_related = (
        metadata.get("related")
        or asset["id"].startswith("EQMP-RN-")
    )

    if has_related:

        st.divider()

        show_related(asset)

    st.divider()

    show_footer()

