import streamlit as st

from components.tag import show as show_tag
from utils.asset_router import open_asset


def show(
    asset_id: str,
    title: str,
):

    with st.container(border=True):

        show_tag(
            asset_type="Research Note",
            asset_id=asset_id,
        )

        st.markdown(
            f"""
<div style="
height:78px;
font-size:20px;
font-weight:700;
line-height:1.35;
overflow:hidden;
margin-bottom:18px;
">
{title}
</div>
""",
            unsafe_allow_html=True,
        )

        if st.button(
            "Read Note",
            key=asset_id,
            use_container_width=True,
        ):
            open_asset(asset_id)
