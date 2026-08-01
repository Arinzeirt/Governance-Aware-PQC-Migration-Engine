"""
Enterprise Design System (EDS)

Component:
    EDS-001 — Section Header

Version:
    2.0.0
"""

import streamlit as st

COMPONENT_ID = "EDS-001"
VERSION = "2.0.0"


def show(
    title: str,
    subtitle: str = "",
    eyebrow: str = "",
    divider: bool = True,
):
    """
    Render a standard EQMP section header.
    """

    if eyebrow:

        st.markdown(
            f"""
<div style="
font-size:12px;
font-weight:700;
letter-spacing:1px;
text-transform:uppercase;
color:#2563EB;
margin-bottom:6px;
">
{eyebrow}
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
<div style="
margin-top:8px;
margin-bottom:18px;
">

<div style="
font-size:30px;
font-weight:700;
line-height:1.2;
color:white;
margin-bottom:8px;
">
{title}
</div>

<div style="
font-size:15px;
line-height:1.7;
color:#94A3B8;
max-width:900px;
">
{subtitle}
</div>

</div>
""",
        unsafe_allow_html=True,
    )

    if divider:
        st.divider()
