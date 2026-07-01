import streamlit as st


def feature(title, desc):

    st.markdown(
        f"""
<div class="eqmp-feature">

<div class="eqmp-feature-title">

{title}

</div>

<div class="eqmp-feature-desc">

{desc}

</div>

</div>
""",
        unsafe_allow_html=True,
    )


def show():

    #
    # Better vertical centering
    #

    st.markdown(
        "<div style='height:45px'></div>",
        unsafe_allow_html=True,
    )

    #
    # Product Name
    #

    st.markdown(
        """
<div style="text-align:center;">

<h1 style="
font-size:48px;
font-weight:800;
line-height:1.15;
margin-bottom:8px;
white-space:nowrap;
">

Enterprise Quantum Assessment Platform

</h1>

<p style="
font-size:19px;
color:#94A3B8;
margin-bottom:30px;
">

Research-Backed Prototype v1.0

</p>

</div>
""",
        unsafe_allow_html=True,
    )

    #
    # Features
    #

    col1, col2, col3 = st.columns(3)

    with col1:

        feature(
            "Discover",
            "Identify and inventory enterprise cryptographic assets."
        )

    with col2:

        feature(
            "Govern",
            "Assess governance, compliance and migration readiness."
        )

    with col3:

        feature(
            "Transform",
            "Generate governance-led migration recommendations."
        )

    st.markdown(
        "<div style='height:24px'></div>",
        unsafe_allow_html=True,
    )

    #
    # Button
    #

    left, center, right = st.columns([1.3, 2.4, 1.3])

    with center:

        launch = st.button(

            "Launch Enterprise Assessment",

            use_container_width=True,

        )

    #
    # Footer
    #

    st.markdown(
        """
<div style="
text-align:center;
margin-top:24px;
color:#64748B;
font-size:13px;
">

Research-Backed Prototype v1.0

<br><br>

Powered by Enet Technologies

</div>
""",
        unsafe_allow_html=True,
    )

    return launch

