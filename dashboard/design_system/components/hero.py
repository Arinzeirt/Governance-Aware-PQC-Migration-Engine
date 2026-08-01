"""
Enterprise Design System (EDS)

EDS-004 — Hero
Version: 2.0.0
"""

import streamlit as st

COMPONENT_ID = "EDS-004"
VERSION = "2.0.0"


def show(
    title: str,
    subtitle: str = "",
    eyebrow: str = "",
    status: str | None = None,
):

    with st.container(border=True):

        left, right = st.columns([6, 1])

        with left:

            if eyebrow:

                st.caption(eyebrow.upper())

            st.markdown(
                f"# {title}"
            )

            if subtitle:

                st.markdown(
                    subtitle
                )

        with right:

            if status:

                st.markdown(
                    f"""
<div style="
text-align:right;
padding-top:8px;
">

<span style="
background:#DBEAFE;
color:#2563EB;
padding:6px 14px;
border-radius:999px;
font-size:12px;
font-weight:700;
border:1px solid #2563EB;
">

{status}

</span>

</div>
""",
                    unsafe_allow_html=True,
                )
