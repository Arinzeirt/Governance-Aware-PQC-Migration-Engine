import streamlit as st


def show():

    st.divider()

    st.markdown("### Next Phase")

    st.success(
        """
Enterprise Discovery has completed successfully.

A governance-aware cryptographic inventory has been generated.

The environment is now ready for migration planning,
prioritisation and governance review.

Continue to the Migration workspace to review the
inventory and prepare a migration strategy.
"""
    )
