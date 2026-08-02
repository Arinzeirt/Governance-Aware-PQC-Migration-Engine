import streamlit as st


def glass_card(title, text):

    st.markdown(
        f"""
<div style="

background:linear-gradient(
180deg,
#0B1730,
#081325
);

border:1px solid #1D4ED8;

border-radius:18px;

padding:26px;

min-height:165px;

box-shadow:

0 0 30px rgba(37,99,235,.12);

">

<h4 style="
margin-bottom:14px;
color:white;
">

{title}

</h4>

<div style="
color:#B7C3D7;
line-height:1.8;
">

{text}

</div>

</div>
""",
        unsafe_allow_html=True,
    )
