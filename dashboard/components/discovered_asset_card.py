import os

import streamlit as st


_BADGE = {
    "High": ("CRITICAL", "#DC2626", "#FEE2E2"),
    "Medium": ("MEDIUM", "#D97706", "#FEF3C7"),
    "Low": ("LOW", "#16A34A", "#DCFCE7"),
}


def show(
    title: str,
    severity: str,
    source: str = "",
):

    label, colour, background = _BADGE.get(
        severity,
        ("UNKNOWN", "#64748B", "#E2E8F0"),
    )

    filename = os.path.basename(source) if source else "-"

    st.markdown(
        f"""
<div style="
border:1px solid #334155;
border-radius:14px;
padding:18px;
height:180px;
display:flex;
flex-direction:column;
justify-content:space-between;
">

<div>

<span style="
display:inline-block;
padding:4px 10px;
border-radius:999px;
background:{background};
color:{colour};
border:1px solid {colour};
font-size:11px;
font-weight:700;
">
{label}
</span>

<div style="
margin-top:16px;
font-size:20px;
font-weight:700;
line-height:1.3;
min-height:56px;
color:white;
">
{title}
</div>

</div>

<div style="
font-size:13px;
color:#94A3B8;
">
Source
</div>

<div style="
font-size:14px;
font-weight:600;
color:#CBD5E1;
overflow:hidden;
text-overflow:ellipsis;
white-space:nowrap;
">
{filename}
</div>

</div>
""",
        unsafe_allow_html=True,
    )
