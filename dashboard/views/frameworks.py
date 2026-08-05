import streamlit as st

from components.asset_card import show as show_asset
from components.landing.footer import show as show_footer

from utils.framework_registry import FRAMEWORK_REGISTRY
from content.frameworks import FRAMEWORKS


def show():

    #
    # Header
    #

    st.title("EQMP Framework Portfolio")

    st.caption(
        "Enterprise Quantum Migration Platform • Framework Library"
    )

    st.markdown(
        """
The EQMP Framework Portfolio represents the core methodologies that
power enterprise quantum readiness, governance-aware migration,
cryptographic resilience and long-term post-quantum transformation.
"""
    )

    st.divider()

    cols = st.columns(2)

    for index, (title, description) in enumerate(FRAMEWORKS):

        framework = FRAMEWORK_REGISTRY.get(
            title,
            {
                "type": "Framework",
                "id": "EQMP-UNK-000",
            },
        )

        with cols[index % 2]:

            show_asset(
                asset_type=framework["type"],
                asset_id=framework["id"],
                title=title,
                description=description,
                button_label="View Framework",
            )

    st.divider()

    show_footer()

