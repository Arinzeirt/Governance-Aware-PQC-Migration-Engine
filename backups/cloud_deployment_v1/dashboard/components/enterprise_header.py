import streamlit as st


def show():

    left, right = st.columns([8, 2])

    with left:

        st.markdown(
            """
### ENET TECHNOLOGIES

Enterprise Quantum Migration Platform
"""
        )

    with right:

        st.markdown(
            """
<div style="text-align:right;padding-top:10px;">

<span style="
background:#0F766E;
color:white;
padding:6px 14px;
border-radius:999px;
font-size:12px;
font-weight:600;
">

● LIVE

</span>

</div>
""",
            unsafe_allow_html=True,
        )

    st.divider()

