import streamlit as st


def metric_card(title, value, subtitle, accent):

    st.markdown(
        f"""
<div style="
background:#111827;
border:1px solid #334155;
border-left:5px solid {accent};
border-radius:14px;
padding:18px;
height:150px;
">

<div style="
font-size:13px;
color:#94A3B8;
margin-bottom:14px;
">

{title}

</div>

<div style="
font-size:30px;
font-weight:700;
color:#F8FAFC;
margin-bottom:12px;
">

{value}

</div>

<div style="
font-size:13px;
color:#CBD5E1;
">

{subtitle}

</div>

</div>
""",
        unsafe_allow_html=True,
    )


def show():

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Overall Risk",
            "HIGH",
            "Critical Exposure",
            "#DC2626"
        )

    with c2:
        metric_card(
            "Readiness",
            "18%",
            "Migration Required",
            "#2563EB"
        )

    with c3:
        metric_card(
            "Assets",
            "573",
            "Inventory Complete",
            "#0F766E"
        )

    with c4:
        metric_card(
            "Compliance",
            "Action Required",
            "Governance Review",
            "#F59E0B"
        )
