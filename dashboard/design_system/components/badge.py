"""
Enterprise Design System (EDS)

EDS-003 — Status Badge
Version: 2.0.0
"""

import streamlit as st

COMPONENT_ID = "EDS-003"
VERSION = "2.0.0"


_COLOURS = {
    "primary": ("#2563EB", "#DBEAFE"),
    "success": ("#16A34A", "#DCFCE7"),
    "warning": ("#D97706", "#FEF3C7"),
    "critical": ("#DC2626", "#FEE2E2"),
    "neutral": ("#475569", "#E2E8F0"),
}


def show(
    label: str,
    status: str = "primary",
):

    colour, background = _COLOURS.get(
        status,
        _COLOURS["primary"],
    )

    st.markdown(
        f"""
<span style="
display:inline-block;
padding:6px 12px;
border-radius:999px;
font-size:12px;
font-weight:700;
background:{background};
color:{colour};
border:1px solid {colour};
">
{label}
</span>
""",
        unsafe_allow_html=True,
    )
