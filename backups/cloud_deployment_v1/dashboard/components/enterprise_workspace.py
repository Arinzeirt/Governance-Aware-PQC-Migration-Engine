import streamlit as st

from components.enterprise_findings import show as show_findings
from components.migration_roadmap import show as show_roadmap


def show():

    left, right = st.columns(
        [3, 2],
        gap="large"
    )

    with left:

        show_findings()

    with right:

        show_roadmap()
