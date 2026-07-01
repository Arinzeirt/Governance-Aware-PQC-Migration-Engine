import streamlit as st

from product import PRODUCT


def show_executive_header():

    left, right = st.columns([5, 1])

    with left:

        st.markdown(
            f"## {PRODUCT['name']} | {PRODUCT['full_name']}"
        )

    with right:

        st.caption(
            f"v{PRODUCT['version']}"
        )

    st.divider()

