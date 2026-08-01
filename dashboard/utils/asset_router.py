import streamlit as st


def open_asset(asset_id: str):
    """
    Open an EQMP knowledge asset.

    The router also remembers the page that launched
    the asset so the Back button returns the user to
    the correct location.
    """

    st.session_state["asset_origin"] = st.session_state.get(
        "page",
        "research",
    )

    st.session_state["selected_asset"] = asset_id

    st.session_state["page"] = "asset_detail"

    st.rerun()
