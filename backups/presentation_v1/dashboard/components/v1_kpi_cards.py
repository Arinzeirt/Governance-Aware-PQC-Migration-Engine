import streamlit as st


def card(title, value, subtitle):

    st.markdown(
        f"""
<div style="
background:#1E293B;
border:1px solid #334155;
border-radius:12px;
padding:18px;
height:150px;
text-align:center;
">

<div style="
color:#94A3B8;
font-size:13px;
font-weight:600;
margin-bottom:14px;
">

{title}

</div>

<div style="
font-size:34px;
font-weight:700;
color:white;
margin-bottom:14px;
">

{value}

</div>

<div style="
color:#64748B;
font-size:12px;
">

{subtitle}

</div>

</div>
""",
        unsafe_allow_html=True,
    )


def show():

    st.markdown("## Enterprise KPI Dashboard")

    row1 = st.columns(4)

    with row1[0]:
        card(
            "Assets Discovered",
            "573",
            "Enterprise Assets"
        )

    with row1[1]:
        card(
            "Overall Risk",
            "HIGH",
            "Current Exposure"
        )

    with row1[2]:
        card(
            "Migration Readiness",
            "18%",
            "Organization Score"
        )

    with row1[3]:
        card(
            "Compliance Status",
            "Review",
            "Regulatory Posture"
        )

    st.write("")

    row2 = st.columns([1,1,2])

    with row2[0]:
        card(
            "Critical Assets",
            "59",
            "Priority Systems"
        )

    with row2[1]:
        card(
            "Assessment Confidence",
            "92%",
            "Decision Confidence"
        )
