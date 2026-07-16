import streamlit as st


PHASES = [

    "Asset Discovery & Inventory",

    "Risk Prioritisation",

    "Pilot Migration",

    "Enterprise Deployment",

    "Continuous Cryptographic Agility",

]


def phase(number, title, last=False):

    connector = ""

    if not last:

        connector = """
<div style="
margin-left:16px;
width:2px;
height:26px;
background:#2563EB;
margin-top:4px;
margin-bottom:4px;
">
</div>
"""

    st.markdown(
        f"""
<div style="display:flex;align-items:flex-start;">

<div>

<div style="
width:34px;
height:34px;
border-radius:50%;
background:#2563EB;
display:flex;
align-items:center;
justify-content:center;
font-weight:700;
color:white;
">

{number}

</div>

{connector}

</div>

<div style="
padding-top:6px;
margin-left:14px;
">

<div style="
font-size:15px;
font-weight:600;
color:#F8FAFC;
">

Phase {number}

</div>

<div style="
font-size:14px;
color:#CBD5E1;
margin-top:4px;
line-height:1.6;
">

{title}

</div>

</div>

</div>
""",
        unsafe_allow_html=True,
    )


def show():

    st.markdown(
        """
<div style="
background:#111827;
border:1px solid #334155;
border-radius:14px;
padding:22px;
margin-bottom:20px;
">

<div style="
font-size:22px;
font-weight:700;
color:#F8FAFC;
margin-bottom:20px;
">

Migration Roadmap

</div>
""",
        unsafe_allow_html=True,
    )

    for index, item in enumerate(PHASES):

        phase(
            index + 1,
            item,
            last=index == len(PHASES) - 1,
        )

    st.markdown("</div>", unsafe_allow_html=True)
