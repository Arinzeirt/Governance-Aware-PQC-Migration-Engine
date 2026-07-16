import streamlit as st


def row(name, value):

    st.markdown(
        f"""
<div style="
display:flex;
justify-content:space-between;
align-items:center;
padding:10px 0;
border-bottom:1px solid #334155;
">

<div style="color:#CBD5E1;">
{name}
</div>

<div style="
color:#F8FAFC;
font-weight:600;
">
{value}
</div>

</div>
""",
        unsafe_allow_html=True,
    )


def card(title):

    st.markdown(
        f"""
<div style="
background:#1E293B;
border:1px solid #334155;
border-radius:14px;
padding:18px;
margin-bottom:12px;
">

<div style="
font-size:18px;
font-weight:700;
color:#F8FAFC;
margin-bottom:14px;
">
{title}
</div>

</div>
""",
        unsafe_allow_html=True,
    )


def show():

    left, right = st.columns(2)

    #
    # Compliance
    #

    with left:

        card("Compliance Readiness")

        row("NDPC", "Review Required")

        row("ISO/IEC 27001", "Review Controls")

        row("PCI DSS", "High Impact")

        row("NIST PQC", "Migration Required")

        row("FIPS 203", "Applicable")

        row("FIPS 204", "Applicable")

        row("FIPS 205", "Monitor")

    #
    # Executive Decision
    #

    with right:

        card("Executive Decision")

        row("Threat Level", "HIGH")

        row("Migration Strategy", "Governance-led")

        row("Deployment", "Hybrid")

        row("Recommended State", "Planning")

        row("Confidence", "92%")

