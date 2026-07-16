import streamlit as st


def show():

    st.markdown(
        """
<div style="
background:#2A1E22;
border:1px solid #7F1D1D;
border-left:6px solid #DC2626;
border-radius:14px;
padding:22px;
margin-bottom:16px;
">

<div style="
font-size:22px;
font-weight:700;
color:#F8FAFC;
margin-bottom:10px;
">

Current Enterprise Posture

</div>

<div style="
font-size:15px;
line-height:1.7;
color:#E2E8F0;
">

Critical cryptographic exposure has been identified across
business-critical services.

The assessment indicates extensive reliance on classical
public-key cryptography requiring governance-led migration
planning for post-quantum readiness.

</div>

<hr style="
border:none;
border-top:1px solid #7F1D1D;
margin:18px 0;
">

<div style="
display:flex;
justify-content:space-between;
font-size:13px;
color:#CBD5E1;
">

<span>

Assessment Completed

</span>

<span>

Backend Services

</span>

<span>

Research Prototype v1.0

</span>

</div>

</div>
""",
        unsafe_allow_html=True,
    )

