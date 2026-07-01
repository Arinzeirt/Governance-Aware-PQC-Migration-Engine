import streamlit as st

from components.v1_topbar import show as show_topbar
from components.v1_enterprise_tools import show as show_tools
from components.v1_executive_overview import show as show_overview
from components.v1_enterprise_kpi import show as show_kpi
from components.v1_enterprise_grid import show as show_grid
from components.v1_findings import show as show_findings
from components.v1_roadmap import show as show_roadmap


def show():

    # Header
    show_topbar()

    st.markdown(
        "<div style='height:8px'></div>",
        unsafe_allow_html=True,
    )

    # Enterprise Tools (collapsed)
    show_tools()

    st.markdown(
        "<div style='height:8px'></div>",
        unsafe_allow_html=True,
    )

    # Executive Posture
    show_overview()

    st.markdown(
        "<div style='height:8px'></div>",
        unsafe_allow_html=True,
    )

    # KPI Dashboard
    show_kpi()

    st.markdown(
        "<div style='height:12px'></div>",
        unsafe_allow_html=True,
    )

    # Enterprise Grid
    show_grid()

    st.markdown(
        "<div style='height:12px'></div>",
        unsafe_allow_html=True,
    )

    # Findings
    show_findings()

    st.markdown(
        "<div style='height:12px'></div>",
        unsafe_allow_html=True,
    )

    # Roadmap
    show_roadmap()

    st.markdown(
        "<div style='height:20px'></div>",
        unsafe_allow_html=True,
    )

    st.caption(
        "EQMP Technology Preview v1.0 • Powered by Enet Technologies"
    )
