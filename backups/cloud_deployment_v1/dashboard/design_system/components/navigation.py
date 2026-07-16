import streamlit as st


def render(
    title: str,
    active: bool = False,
):

    background = "#2563EB" if active else "#111827"

    border = "#2563EB" if active else "#334155"

    color = "#FFFFFF" if active else "#CBD5E1"

    st.markdown(
        f"""
<div style="
background:{background};
border:1px solid {border};
border-radius:12px;
padding:12px 16px;
margin-bottom:10px;
color:{color};
font-weight:600;
cursor:pointer;
">

{title}

</div>
""",
        unsafe_allow_html=True,
    )
