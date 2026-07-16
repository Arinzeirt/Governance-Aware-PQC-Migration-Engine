import streamlit as st


def show():

    st.markdown(
        """
<div style="
background:#111827;
border:1px solid #334155;
border-radius:14px;
padding:18px 20px;
margin-bottom:6px;
">

<div style="
display:flex;
justify-content:space-between;
align-items:flex-start;
">

<div>

<div style="
font-size:26px;
font-weight:700;
color:#F8FAFC;
margin-bottom:4px;
">

Executive Summary

</div>

<div style="
font-size:13px;
color:#94A3B8;
">

Governance-Aware Post-Quantum Readiness

</div>

</div>

<div style="
background:#065F46;
color:white;
padding:8px 16px;
border-radius:999px;
font-size:13px;
font-weight:600;
white-space:nowrap;
">

🟢 Assessment Complete

</div>

</div>

<div style="
margin-top:14px;
font-size:15px;
line-height:1.55;
color:#E2E8F0;
">

Your enterprise has significant exposure to cryptographic assets requiring governance-led migration planning before the quantum threat becomes operational.

</div>

<div style="
margin-top:14px;
font-size:15px;
font-weight:700;
color:#F8FAFC;
">

Recommended Action

</div>

<div style="
margin-top:8px;
padding:12px 16px;
background:#172554;
border:1px solid #2563EB;
border-radius:10px;
color:#DBEAFE;
font-size:14px;
line-height:1.45;
">

Begin a governance-led migration programme by prioritizing Internet-facing services, business-critical systems and cryptographic assets with high quantum exposure.

</div>

</div>
""",
        unsafe_allow_html=True,
    )
