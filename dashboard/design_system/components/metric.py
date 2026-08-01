"""
Enterprise Design System (EDS)

EDS-005 — Metric Tile
Version: 2.0.0
"""

import streamlit as st

COMPONENT_ID = "EDS-005"
VERSION = "2.0.0"


_ACCENTS = {
    "primary": "#2563EB",
    "success": "#16A34A",
    "warning": "#D97706",
    "critical": "#DC2626",
    "neutral": "#64748B",
}


def show(
    title: str,
    value,
    subtitle: str = "",
    accent: str = "primary",
):

    colour = _ACCENTS.get(
        accent,
        _ACCENTS["primary"],
    )

    st.markdown(
        f"""
<div style="
border:1px solid #334155;
border-radius:14px;
padding:20px;
height:160px;
">

<div style="
font-size:14px;
font-weight:600;
color:#94A3B8;
margin-bottom:14px;
">
{title}
</div>

<div style="
font-size:38px;
font-weight:700;
color:{colour};
margin-bottom:12px;
">
{value}
</div>

<div style="
font-size:14px;
color:#CBD5E1;
">
{subtitle}
</div>

</div>
""",
        unsafe_allow_html=True,
    )
