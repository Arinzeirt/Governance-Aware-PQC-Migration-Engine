import streamlit as st


def show(value: str, title: str, subtitle: str = ""):

    st.markdown(
        f"""
<div style="
background:#111827;
border:1px solid #334155;
border-radius:14px;
padding:20px;
min-height:135px;
">

<div style="
font-size:34px;
font-weight:700;
color:white;
margin-bottom:8px;
">
{value}
</div>

<div style="
font-size:16px;
font-weight:600;
color:white;
margin-bottom:8px;
">
{title}
</div>

<div style="
font-size:14px;
line-height:1.6;
color:#94A3B8;
">
{subtitle}
</div>

</div>
""",
        unsafe_allow_html=True,
    )
