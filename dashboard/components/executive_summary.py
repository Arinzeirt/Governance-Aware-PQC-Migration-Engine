import streamlit as st


def show():

    st.markdown(
        """
<div style="
background:#111827;
border:1px solid #334155;
border-radius:14px;
padding:24px;
margin-bottom:22px;
">

<div style="
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:18px;
">

<div>

<div style="
font-size:24px;
font-weight:700;
color:#F8FAFC;
">

Executive Summary

</div>

<div style="
font-size:14px;
color:#94A3B8;
">

Governance-Aware Post-Quantum Readiness

</div>

</div>

<div style="
background:#065F46;
color:white;
padding:8px 14px;
border-radius:999px;
font-size:13px;
font-weight:600;
">

🟢 Assessment Complete

</div>

</div>

<div style="
font-size:16px;
line-height:1.8;
color:#E2E8F0;
margin-bottom:20px;
">

Your enterprise has significant exposure to cryptographic assets that
require migration planning before the quantum threat becomes operational.

</div>

<div style="
font-size:15px;
font-weight:700;
color:#F8FAFC;
margin-bottom:10px;
">

Primary Governance Recommendation

</div>

<div style="
font-size:15px;
line-height:1.7;
color:#CBD5E1;
margin-bottom:24px;
">

Begin a phased, governance-led cryptographic transformation programme
focused on business-critical systems, externally exposed services,
and regulatory assets.

</div>

<hr style="
border:none;
border-top:1px solid #334155;
margin:20px 0;
">

<div style="
display:grid;
grid-template-columns:220px 1fr;
row-gap:12px;
column-gap:20px;
font-size:14px;
">

<div style="color:#94A3B8;"><strong>Assessment Scope</strong></div>
<div style="color:#E2E8F0;">Enterprise Infrastructure</div>

<div style="color:#94A3B8;"><strong>Analysis Type</strong></div>
<div style="color:#E2E8F0;">
Cryptographic Inventory & Readiness Assessment
</div>

<div style="color:#94A3B8;"><strong>Recommendation</strong></div>
<div style="color:#E2E8F0;">
Governance-Led Phased Migration
</div>

</div>

</div>
""",
        unsafe_allow_html=True,
    )
