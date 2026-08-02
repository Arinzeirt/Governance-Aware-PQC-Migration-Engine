import streamlit as st


def card(title, text):

    st.markdown(
        f"""
<div style="
background:linear-gradient(180deg,#10233A 0%,#0A1626 100%);
border:1px solid rgba(64,142,255,.22);
border-radius:20px;
padding:30px 28px;
height:210px;
display:flex;
flex-direction:column;
justify-content:center;
box-shadow:
    inset 0 1px 0 rgba(255,255,255,.03),
    0 12px 35px rgba(0,40,120,.18);
">

<div style="
font-size:22px;
font-weight:700;
color:white;
margin-bottom:18px;
line-height:1.35;
text-align:left;
">

{title}

</div>

<div style="
font-size:16px;
line-height:1.8;
color:#B8C8D9;
text-align:left;
">

{text}

</div>

</div>
""",
        unsafe_allow_html=True,
    )


def show():

    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4, gap="large")

    with c1:
        card(
            "Cloud Native",
            "No installation required.<br>Launch assessments directly from your browser.",
        )

    with c2:
        card(
            "Executive Report",
            "Professional PDF report delivered immediately after assessment.",
        )

    with c3:
        card(
            "Research Driven",
            "Built on governance-aware post-quantum migration research.",
        )

    with c4:
        card(
            "5-Minute Assessment",
            "Rapid discovery of cryptographic assets and migration readiness.",
        )

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
