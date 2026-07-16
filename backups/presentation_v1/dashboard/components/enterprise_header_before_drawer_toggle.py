import streamlit as st


def show():

    left, right = st.columns([9, 3])

    with left:

        st.markdown(
            """
<div style="line-height:1.2;">

<div style="
font-size:30px;
font-weight:700;
color:#FFFFFF;
letter-spacing:0.5px;
">

ENET TECHNOLOGIES

</div>

<div style="
font-size:15px;
color:#CBD5E1;
margin-top:6px;
">

Enterprise Quantum Migration Platform

</div>

</div>
""",
            unsafe_allow_html=True,
        )

    with right:

        st.markdown(
            """
<div style="
display:flex;
justify-content:flex-end;
align-items:center;
height:100%;
">

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

    st.markdown(
        """
<hr style="
border:none;
border-top:1px solid #1E293B;
margin-top:18px;
margin-bottom:18px;
">
""",
        unsafe_allow_html=True,
    )
