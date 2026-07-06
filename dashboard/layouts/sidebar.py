import streamlit as st


def nav_item(title, active=False):

    if active:

        st.markdown(
            f"""
<div style="
background:#2563EB;
padding:12px 16px;
border-radius:10px;
margin-bottom:8px;
font-weight:700;
color:white;
">
{title}
</div>
""",
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            f"""
<div style="
background:#1E293B;
padding:12px 16px;
border-radius:10px;
margin-bottom:8px;
border:1px solid #334155;
color:#CBD5E1;
">
{title}
</div>
""",
            unsafe_allow_html=True,
        )


def tool_item(title):

    st.markdown(
        f"""
<div style="
padding:10px 14px;
margin-bottom:6px;
color:#CBD5E1;
border-radius:8px;
">
{title}
</div>
""",
        unsafe_allow_html=True,
    )


def show():

    st.markdown(
        """
<div style="margin-bottom:24px;">

<div style="
font-size:30px;
font-weight:800;
color:white;
">

EQMP

</div>

<div style="
font-size:13px;
color:#94A3B8;
">

Research-Backed Prototype

</div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("### Navigation")

    nav_item("🏠 Dashboard", True)

    nav_item("📊 Enterprise Scan Results")

    nav_item("🛡 Compliance Readiness")

    nav_item("📄 Executive Findings")

    nav_item("🗺 Migration Roadmap")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### Enterprise Tools")

    tool_item("🚀 Migration Planner")

    tool_item("📥 Executive Report")

    tool_item("📥 Technical Inventory")

    st.markdown("<br>", unsafe_allow_html=True)

    st.caption("Version 1.0")

