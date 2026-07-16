import streamlit as st


def metric_card(title, value, subtitle, accent):

    st.markdown(
        f"""
<div style="
background:#111827;
border:1px solid #334155;
border-top:4px solid {accent};
border-radius:14px;
padding:22px;
height:170px;
display:flex;
flex-direction:column;
justify-content:space-between;
">

<div style="
font-size:14px;
font-weight:600;
color:#CBD5E1;
">

{title}

</div>

<div style="
font-size:42px;
font-weight:800;
color:{accent};
line-height:1;
margin-top:8px;
margin-bottom:8px;
">

{value}

</div>

<div style="
font-size:14px;
color:#94A3B8;
">

{subtitle}

</div>

</div>
""",
        unsafe_allow_html=True,
    )


def show():

    st.markdown("## Enterprise Risk Overview")

    st.write("")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        metric_card(

            "Overall Risk",

            "HIGH",

            "Immediate Attention Required",

            "#EF4444",

        )

    with c2:

        metric_card(

            "Readiness Score",

            "72%",

            "Moderate Readiness",

            "#F59E0B",

        )

    with c3:

        metric_card(

            "Total Findings",

            "13",

            "Assets Identified",

            "#3B82F6",

        )

    with c4:

        metric_card(

            "Critical Assets",

            "1",

            "Require Immediate Action",

            "#EF4444",

        )

