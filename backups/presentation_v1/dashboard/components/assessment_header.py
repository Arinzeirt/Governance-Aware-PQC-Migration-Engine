import streamlit as st


def show():

    st.markdown(
        """
<div style="
background:#111827;
border:1px solid #334155;
border-radius:16px;
padding:28px;
margin-bottom:20px;
">

<div style="
display:flex;
justify-content:space-between;
align-items:center;
">

<div>

<div style="
font-size:30px;
font-weight:700;
color:#F8FAFC;
margin-bottom:8px;
">

Enterprise Quantum Readiness Assessment

</div>

<div style="
font-size:15px;
color:#94A3B8;
">

Evaluate cryptographic assets, governance readiness,
and migration priorities using the Enterprise Quantum
Migration Governance Framework (EQMGF).

</div>

</div>

<div>

<div class="eqmp-badge">

Technology Preview v0.9 RC1

</div>

</div>

</div>

</div>
""",
        unsafe_allow_html=True,
    )
