import streamlit as st


CARD_STYLE = """
background:linear-gradient(180deg,#10233A 0%,#0A1626 100%);
border:1px solid rgba(64,142,255,.20);
border-radius:20px;
padding:20px 22px;
height:220px;
box-shadow:
    inset 0 1px 0 rgba(255,255,255,.03),
    0 12px 30px rgba(0,40,120,.12);
"""


def card(number, title, body):

    st.markdown(
        f"""
<div style="{CARD_STYLE}">

<div style="
width:30px;
height:30px;
border-radius:50%;
background:#0F5BFF;
display:flex;
align-items:center;
justify-content:center;
font-weight:700;
font-size:13px;
color:white;
margin-bottom:10px;
">

{number}

</div>

<div style="
font-size:18px;
font-weight:700;
line-height:1.25;
color:white;
margin-bottom:8px;
">

{title}

</div>

<div style="
font-size:14px;
line-height:1.6;
color:#B7C4D6;
">

{body}

</div>

</div>
""",
        unsafe_allow_html=True,
    )


def show():

    st.markdown("## Your Assessment Journey")

    st.caption(
        "Complete your first governance-aware assessment in four guided steps."
    )

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4, gap="large")

    with c1:
        card(
            "1",
            "Register",
            "Provide your official business email to begin your assessment.",
        )

    with c2:
        card(
            "2",
            "Run Assessment",
            "Upload a repository or use the demo environment to discover cryptographic assets.",
        )

    with c3:
        card(
            "3",
            "Receive Report",
            "Download your executive PDF with migration readiness and findings.",
        )

    with c4:
        card(
            "4",
            "Begin Migration",
            "Continue into your guided post-quantum migration programme.",
        )

    st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)

    st.divider()
