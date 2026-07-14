import streamlit as st


def feature(title, description, icon):

    st.markdown(
        f"""
<div style="
background:#111827;
border:1px solid #334155;
border-radius:16px;
padding:20px;
height:190px;
text-align:center;
">

<div style="
font-size:32px;
margin-bottom:14px;
">

{icon}

</div>

<div style="
font-size:22px;
font-weight:700;
color:#F8FAFC;
margin-bottom:10px;
">

{title}

</div>

<div style="
font-size:14px;
line-height:1.75;
color:#94A3B8;
">

{description}

</div>

</div>
""",
        unsafe_allow_html=True,
    )


def capability(text):

    st.markdown(
        f"""
<div style="
background:#111827;
border:1px solid #334155;
border-radius:999px;
padding:12px;
text-align:center;
font-weight:600;
color:#CBD5E1;
">

{text}

</div>
""",
        unsafe_allow_html=True,
    )


def show():

    #
    # Top spacing
    #

    st.markdown(
        "<div style='height:35px'></div>",
        unsafe_allow_html=True,
    )

    #
    # Branding
    #

    st.markdown(
        """
<div style="text-align:center;">

<div style="
font-size:15px;
letter-spacing:4px;
font-weight:700;
color:#2563EB;
margin-bottom:20px;
">

ENET TECHNOLOGIES

</div>

<div style="
font-size:56px;
font-weight:800;
color:#F8FAFC;
margin-bottom:8px;
">

EQMP

</div>

<div style="
font-size:30px;
font-weight:700;
color:#F8FAFC;
margin-bottom:16px;
">

Enterprise Quantum Migration Platform

</div>

<div style="
font-size:19px;
color:#CBD5E1;
margin-bottom:24px;
">

Governance-Led Post-Quantum Transformation

</div>

<div style="
display:inline-block;
padding:8px 18px;
border-radius:999px;
border:1px solid #2563EB;
background:#172554;
color:#BFDBFE;
font-size:13px;
font-weight:700;
">

Technology Preview v0.9 RC1

</div>

</div>
""",
        unsafe_allow_html=True,
    )

    #
    # Product Description
    #

    st.markdown(
        """
<div style="
text-align:center;
font-size:16px;
line-height:1.8;
color:#94A3B8;
max-width:850px;
margin:28px auto 42px auto;
">

Helping organizations discover cryptographic assets,
evaluate governance readiness,
and orchestrate risk-based post-quantum migration
through the Enterprise Quantum Migration Governance Framework (EQMGF).

</div>
""",
        unsafe_allow_html=True,
    )

    #
    # Platform Pillars
    #

    col1, col2, col3 = st.columns(3)

    with col1:

        feature(
            "Discover",
            "Identify cryptographic assets, dependencies and enterprise exposure.",
            "🔍"
        )

    with col2:

        feature(
            "Govern",
            "Evaluate governance maturity, migration readiness and business priorities.",
            "🛡"
        )

    with col3:

        feature(
            "Migrate",
            "Plan governance-led post-quantum migration across enterprise systems.",
            "➜"
        )

    st.markdown(
        "<div style='height:42px'></div>",
        unsafe_allow_html=True,
    )

    #
    # Launch Button
    #

    left, center, right = st.columns([1.4,2.2,1.4])

    with center:

        launch = st.button(
            "Launch Executive Command Center",
            use_container_width=True,
            type="primary",
        )

    st.markdown(
        "<div style='height:45px'></div>",
        unsafe_allow_html=True,
    )

    #
    # Capability Strip
    #

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        capability("Governance-Led")

    with c2:
        capability("Quantum-Safe")

    with c3:
        capability("Enterprise Scale")

    with c4:
        capability("Cryptographic Agility")

    st.markdown(
        "<div style='height:35px'></div>",
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        """
<div style="
text-align:center;
padding-top:18px;
padding-bottom:22px;
">

<div style="
font-size:15px;
font-weight:700;
color:#F8FAFC;
">

Enterprise Quantum Migration Governance Framework (EQMGF)

</div>

<div style="
font-size:13px;
color:#94A3B8;
margin-top:10px;
">

Powered by Enet Technologies

</div>

<div style="
font-size:12px;
color:#64748B;
margin-top:6px;
">

Technology Preview v0.9 RC1

</div>

</div>
""",
        unsafe_allow_html=True,
    )

    return launch

