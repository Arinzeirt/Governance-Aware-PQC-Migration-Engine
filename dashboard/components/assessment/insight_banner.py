import streamlit as st

from content.insights import INSIGHT


def show():

    st.markdown(
        f"""
<div style="
background:linear-gradient(135deg,#10233C,#162E4F);
border:1px solid rgba(77,163,255,.25);
border-radius:18px;
padding:28px;
margin:20px 0 35px 0;
">

<div style="
color:#4DA3FF;
font-size:13px;
font-weight:700;
letter-spacing:1px;
text-transform:uppercase;
margin-bottom:10px;
">

Quantum Intelligence Brief

</div>

<div style="
color:white;
font-size:28px;
font-weight:700;
margin-bottom:15px;
">

{INSIGHT["title"]}

</div>

<div style="
color:#C8D4DF;
font-size:17px;
line-height:1.8;
">

{INSIGHT["body"]}

</div>

<div style="
margin-top:20px;
color:#7FA9D6;
font-size:13px;
">

📖 {INSIGHT["footer"]}

</div>

</div>
""",
        unsafe_allow_html=True,
    )
