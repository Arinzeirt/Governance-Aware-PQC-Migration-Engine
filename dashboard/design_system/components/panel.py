"""
Enterprise Design System (EDS)

EDS-002 — Enterprise Panel
Version: 2.0.0
"""

import streamlit as st
from contextlib import contextmanager


COMPONENT_ID = "EDS-002"
VERSION = "2.0.0"


@contextmanager
def show(
    title: str | None = None,
    subtitle: str | None = None,
):
    """
    Enterprise Panel

    Usage:

    with panel.show("Metadata"):
        ...
    """

    with st.container(border=True):

        if title:

            st.markdown(
                f"""
<div style="
font-size:18px;
font-weight:700;
margin-bottom:4px;
">

{title}

</div>
""",
                unsafe_allow_html=True,
            )

        if subtitle:

            st.markdown(
                f"""
<div style="
font-size:14px;
line-height:1.6;
color:#94A3B8;
margin-bottom:18px;
">

{subtitle}

</div>
""",
                unsafe_allow_html=True,
            )

        yield
