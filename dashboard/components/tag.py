import streamlit as st


def show(asset_type: str, asset_id: str):

    st.markdown(
        f"""
<div style="
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:16px;
">

<div style="
font-size:12px;
font-weight:700;
letter-spacing:1px;
text-transform:uppercase;
color:#60A5FA;
">
{asset_type}
</div>

<div style="
font-size:13px;
font-weight:600;
color:#94A3B8;
">
{asset_id}
</div>

</div>
""",
        unsafe_allow_html=True,
    )
