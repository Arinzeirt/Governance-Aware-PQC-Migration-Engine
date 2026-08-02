import streamlit as st


CARD_STYLE = """
background:linear-gradient(180deg,#10233A 0%,#0A1626 100%);
border:1px solid rgba(64,142,255,.20);
border-radius:20px;
padding:24px;
height:190px;
display:flex;
flex-direction:column;
justify-content:flex-start;
box-shadow:
    inset 0 1px 0 rgba(255,255,255,.03),
    0 12px 30px rgba(0,40,120,.12);
"""


def card(title, subtitle, body):

    subtitle_html = ""

    if subtitle.strip():
        subtitle_html = f"""
<div style="
font-size:15px;
font-weight:500;
color:#9FB5CC;
margin-bottom:16px;
">
{subtitle}
</div>
"""

    st.markdown(
        f"""
<div style="{CARD_STYLE}">

<div style="
font-size:20px;
font-weight:700;
color:white;
line-height:1.25;
margin-bottom:12px;
">

{title}

</div>

{subtitle_html}

<div style="
font-size:14px;
line-height:1.65;
color:#B7C4D6;
">

{body}

</div>

</div>
""",
        unsafe_allow_html=True,
    )


def show():

    st.markdown("## Why Organisations Need EQMP")

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4, gap="large")

    with c1:
        card(
            "Harvest Now,<br>Decrypt Later",
            "",
            "Sensitive encrypted data may already be at risk.",
        )

    with c2:
        card(
            "Unknown<br>Cryptography",
            "",
            "Most organisations don't know where cryptography exists.",
        )

    with c3:
        card(
            "Migration<br>Complexity",
            "",
            "PQC migration requires governance and prioritisation.",
        )

    with c4:
        card(
            "Research Driven",
            "",
            "Built on governance-aware post-quantum migration research.",
        )

    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

    st.divider()
