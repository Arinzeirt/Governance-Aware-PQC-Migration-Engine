import streamlit as st


def show(text):

    st.markdown(
        f"""
<div style="
display:inline-block;
padding:8px 18px;
border-radius:999px;
background:#0E2338;
border:1px solid rgba(80,150,255,.25);
color:#65AEFF;
font-size:12px;
font-weight:700;
letter-spacing:1px;
text-transform:uppercase;
margin-bottom:18px;
">
{text}
</div>
""",
        unsafe_allow_html=True,
    )
