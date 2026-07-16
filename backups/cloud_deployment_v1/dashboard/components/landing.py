import streamlit as st


def show():

    st.markdown(
        """
<style>

.hero{

padding:40px;
border-radius:16px;
background:#0f172a;
color:white;

}

.metric{

padding:18px;
border-radius:10px;
background:#f8fafc;
border:1px solid #e5e7eb;

text-align:center;

}

.big{

font-size:42px;
font-weight:bold;

}

.small{

color:#94a3b8;

}

</style>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="hero">

<h4>ENET TECHNOLOGIES</h4>

<h1>Governance-Aware<br>PQC Migration Engine</h1>

<h4>Enterprise Prototype v2.0</h4>

<p>

Discover cryptographic assets.<br>

Assess migration readiness.<br>

Evaluate business impact.<br>

Generate executive migration reports.

</p>

</div>

""",
        unsafe_allow_html=True,
    )

    st.write("")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(
            """
<div class="metric">

<h2>Discovery</h2>

Cryptographic Asset Inventory

</div>

""",
            unsafe_allow_html=True,
        )

    with c2:

        st.markdown(
            """
<div class="metric">

<h2>Governance</h2>

Business & Regulatory Mapping

</div>

""",
            unsafe_allow_html=True,
        )

    with c3:

        st.markdown(
            """
<div class="metric">

<h2>Migration</h2>

Roadmap & Executive Reporting

</div>

""",
            unsafe_allow_html=True,
        )

    st.write("")

    return st.button(
        "▶ Start Enterprise Assessment",
        type="primary",
        use_container_width=True,
    )
