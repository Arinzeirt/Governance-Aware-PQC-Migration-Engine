import streamlit as st


def begin(title):

    st.markdown(
        f"""
<div style="
background:#1E293B;
border:1px solid #334155;
border-radius:12px;
padding:18px;
margin-bottom:16px;
">

<h3 style="margin-top:0;margin-bottom:18px;">

{title}

</h3>
""",
        unsafe_allow_html=True,
    )


def end():

    st.markdown(

        "</div>",

        unsafe_allow_html=True,

    )
