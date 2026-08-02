import streamlit as st


def primary(text):

    st.markdown(
        f"""
<div style="

background:linear-gradient(
90deg,
#1D4ED8,
#2563EB
);

padding:16px;

border-radius:14px;

text-align:center;

font-weight:700;

font-size:18px;

color:white;

box-shadow:

0 0 30px rgba(37,99,235,.35);

">

{text}

→

</div>
""",
unsafe_allow_html=True)
