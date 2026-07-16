import streamlit as st


def show():

    left, right = st.columns([10, 2])

    with left:

        if st.button(
            "☰",
            key="drawer_toggle",
            help="Open Navigation"
        ):

            st.session_state.drawer_open = not st.session_state.get(
                "drawer_open",
                False
            )

        st.markdown(
            """
<div style="margin-top:-6px;">

<div style="
font-size:28px;
font-weight:700;
color:#FFFFFF;
">

ENET TECHNOLOGIES

</div>

<div style="
font-size:15px;
color:#CBD5E1;
margin-top:2px;
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
margin-top:8px;
text-align:right;
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
<div style="
margin-top:12px;
margin-bottom:18px;
border-bottom:1px solid #1E293B;
">
</div>
""",
        unsafe_allow_html=True,
    )
