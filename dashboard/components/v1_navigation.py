import streamlit as st


def item(title, active=False):

    if active:

        color = "#F8FAFC"
        border = "#2563EB"

    else:

        color = "#94A3B8"
        border = "transparent"

    st.markdown(
        f"""
<div style="
text-align:center;
padding:10px 0;
font-size:14px;
font-weight:600;
color:{color};
border-bottom:3px solid {border};
cursor:pointer;
">

{title}

</div>
""",
        unsafe_allow_html=True,
    )


def tool(title):

    st.markdown(
        f"""
<div style="
text-align:center;
padding:10px 0;
font-size:13px;
color:#CBD5E1;
">

{title}

</div>
""",
        unsafe_allow_html=True,
    )


def show():

    c1,c2,c3,c4,c5,space,c6,c7,c8 = st.columns(
        [1.2,1.5,1.3,1.3,1.3,.5,1.2,1.2,1.2]
    )

    with c1:
        item("Dashboard",True)

    with c2:
        item("Scan Results")

    with c3:
        item("Compliance")

    with c4:
        item("Findings")

    with c5:
        item("Roadmap")

    with c6:
        tool("📄 Report")

    with c7:
        tool("📦 Inventory")

    with c8:
        tool("🚀 Planner")

    st.markdown(
        "<div style='height:12px'></div>",
        unsafe_allow_html=True,
    )

