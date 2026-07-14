import streamlit as st

from version import (
    PRODUCT_NAME,
    VERSION,
    BUILD,
    ORGANIZATION,
)


def show():

    st.divider()

    c1, c2 = st.columns([3,1])

    with c1:

        st.caption(

            f"{PRODUCT_NAME} • {VERSION}"

        )

        st.caption(

            ORGANIZATION

        )

    with c2:

        st.caption(

            f"Build {BUILD}"

        )

