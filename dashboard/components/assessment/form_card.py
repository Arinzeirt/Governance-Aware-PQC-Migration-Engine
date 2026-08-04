import streamlit as st
from contextlib import contextmanager


@contextmanager
def form_card(title, description):

    st.markdown(
        f"""
<div style="
background:linear-gradient(180deg,#10233A 0%,#0A1626 100%);
border:1px solid rgba(64,142,255,.18);
border-radius:22px;
padding:28px;
margin-bottom:20px;
box-shadow:
0 12px 30px rgba(0,40,120,.12);
">

<h2 style="
margin-top:0;
margin-bottom:8px;
color:white;
">

{title}

</h2>

<div style="
color:#AFC0D5;
margin-bottom:26px;
">

{description}

</div>
""",
        unsafe_allow_html=True,
    )

    yield

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )
