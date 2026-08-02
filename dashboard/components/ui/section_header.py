import streamlit as st


def show(title: str, subtitle: str = ""):

    st.markdown(
        f"""
<div style="margin-top:30px;margin-bottom:24px;">

<div style="
font-size:42px;
font-weight:700;
color:white;
margin-bottom:10px;
">
{title}
</div>

<div style="
font-size:17px;
color:#9EB0C6;
line-height:1.7;
max-width:760px;
">
{subtitle}
</div>

</div>
""",
        unsafe_allow_html=True,
    )
