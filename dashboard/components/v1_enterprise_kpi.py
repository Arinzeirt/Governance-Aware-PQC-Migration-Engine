import streamlit as st


def kpi(title, value, color="#F8FAFC"):

    st.markdown(
        f"""
<div style="
background:#1E293B;
border:1px solid #334155;
border-radius:14px;
padding:18px;
height:120px;
display:flex;
flex-direction:column;
justify-content:center;
text-align:center;
">

<div style="
font-size:14px;
color:#94A3B8;
font-weight:600;
">

{title}

</div>

<div style="
margin-top:10px;
font-size:32px;
font-weight:700;
color:{color};
">

{value}

</div>

</div>
""",
        unsafe_allow_html=True,
    )


def show():

    row1 = st.columns(4)

    with row1[0]:
        kpi("Assets", "573")

    with row1[1]:
        kpi("Risk", "CRITICAL", "#EF4444")

    with row1[2]:
        kpi("Readiness", "18%")

    with row1[3]:
        kpi("Critical Assets", "38")


    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)


    row2 = st.columns(4)

    with row2[0]:
        kpi("Compliance", "Review")

    with row2[1]:
        kpi("Confidence", "92%")

    with row2[2]:
        kpi("Recommendation", "Planning", "#3B82F6")

    with row2[3]:
        kpi("Top Findings", "RSA / TLS")

