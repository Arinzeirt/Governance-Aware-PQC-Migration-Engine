import streamlit as st


def column(title, items):

    html = f"""
<div style="margin-bottom:18px;
font-size:17px;
font-weight:700;
color:white;">

{title}

</div>
"""

    for item in items:

        html += f"""
<div style="
margin-bottom:10px;
font-size:14px;
color:#9FB5CC;
">

{item}

</div>
"""

    st.markdown(html, unsafe_allow_html=True)


def show():

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    c1,c2,c3,c4,c5 = st.columns([1.6,1,1,1,1])

    with c1:

        st.markdown(
"""
<div style="font-size:28px;
font-weight:800;
color:#2F7DFF;">
ENET
</div>

<div style="
font-size:12px;
letter-spacing:1px;
color:#AEB7C5;
margin-bottom:22px;">
TECHNOLOGIES
</div>

<div style="
font-size:14px;
line-height:1.7;
color:#9FB5CC;
margin-bottom:24px;">
Research-driven, governance-aware
platform for secure post-quantum
migration.
</div>

<div style="
color:#4DA3FF;
font-size:14px;">
LinkedIn &nbsp;&nbsp; GitHub &nbsp;&nbsp; X
</div>
""",
unsafe_allow_html=True)

    with c2:

        column(
            "Platform",
            [
                "Assessment",
                "Migration Wizard",
                "Reports",
                "Knowledge Centre",
            ],
        )

    with c3:

        column(
            "Research",
            [
                "Research Notes",
                "Whitepapers",
                "Framework",
                "Publications",
            ],
        )

    with c4:

        column(
            "Company",
            [
                "About",
                "Mission",
                "Contact",
                "Privacy",
            ],
        )

    with c5:

        column(
            "Ready",
            [
                "Research Backed",
                "Enterprise Ready",
                "Future Focused",
            ],
        )

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    st.markdown(
        '<div style="height:1px;background:#14233C;margin-top:2px;"></div>',
        unsafe_allow_html=True,
    )

    left,right = st.columns([4,2])

    with left:

        st.caption("© 2026 Enet Technologies. All rights reserved.")

    with right:

        st.markdown(
"""
<div style="text-align:right;
color:#7E8EA5;
font-size:13px;">

Privacy &nbsp;&nbsp; Terms &nbsp;&nbsp; Security

</div>
""",
unsafe_allow_html=True)
