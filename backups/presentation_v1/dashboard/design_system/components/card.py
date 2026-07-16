import streamlit as st


def begin():

    st.markdown(
        """
<div style="
background:#111827;
border:1px solid #334155;
border-radius:14px;
padding:20px;
margin-bottom:18px;
box-shadow:0 6px 18px rgba(0,0,0,0.18);
">
""",
        unsafe_allow_html=True,
    )


def end():

    st.markdown(
        """
</div>
""",
        unsafe_allow_html=True,
    )
