import streamlit as st

from components.landing import show

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="Governance-Aware PQC Migration Engine",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------------------------------
# Session State
# ----------------------------------------------------

if "started" not in st.session_state:
    st.session_state.started = False

# ----------------------------------------------------
# Landing Page
# ----------------------------------------------------

if not st.session_state.started:

    if show():
        st.session_state.started = True
        st.rerun()

    st.stop()

# ----------------------------------------------------
# Assessment Screen (Temporary)
# ----------------------------------------------------

st.title("Governance-Aware PQC Migration Engine")

st.success("Assessment Started")

st.info(
    """
The Enterprise UI is now active.

In the next step we will automatically scan the embedded
Reference Financial Backend instead of asking users
to upload a project.
"""
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Discovery", "Pending")

with col2:
    st.metric("Readiness", "Pending")

with col3:
    st.metric("Business Impact", "Pending")

st.divider()

st.subheader("Assessment Status")

st.progress(0)

st.write(
    """
The assessment engine will be connected in the next sprint.

The following modules will execute automatically:

- Cryptographic Discovery
- Asset Classification
- Readiness Assessment
- Governance Mapping
- Regulatory Analysis
- Executive Reporting
"""
)
