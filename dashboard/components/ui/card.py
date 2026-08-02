import streamlit as st


def show(
    title: str,
    body: str,
    icon: str = "",
    height: int = 205,
):

    st.markdown(
        f"""
<div style="
background:linear-gradient(180deg,#102238,#0C1828);
border:1px solid rgba(80,150,255,.18);
border-radius:18px;
padding:22px;
height:{height}px;
box-shadow:0 0 28px rgba(30,90,180,.08);
display:flex;
flex-direction:column;
justify-content:flex-start;
">

<div style="
font-size:40px;
margin-bottom:14px;
">
{icon}
</div>

<div style="
font-size:18px;
font-weight:700;
color:white;
margin-bottom:12px;
line-height:1.35;
min-height:52px;
">
{title}
</div>

<div style="
font-size:14px;
line-height:1.75;
color:#B7C4D6;
flex:1;
">
{body}
</div>

</div>
""",
        unsafe_allow_html=True,
    )
