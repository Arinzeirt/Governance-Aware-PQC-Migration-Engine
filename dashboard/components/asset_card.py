import streamlit as st

from components.tag import show as show_tag
from utils.asset_router import open_asset


def show(
    asset_type: str,
    asset_id: str,
    title: str,
    description: str,
    button_label: str = "View",
):

    with st.container(border=True):

        show_tag(
            asset_type=asset_type,
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
margin-bottom:14px;
">
{title}
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
<div style="
height:92px;
font-size:15px;
line-height:1.6;
color:#CBD5E1;
overflow:hidden;
margin-bottom:18px;
">
{description}
</div>
""",
            unsafe_allow_html=True,
        )

        if st.button(
            button_label,
            key=asset_id,
            use_container_width=True,
        ):
            open_asset(asset_id)
