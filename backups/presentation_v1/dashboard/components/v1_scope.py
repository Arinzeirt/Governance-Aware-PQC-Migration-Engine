import streamlit as st


def unavailable():

    st.toast(
        "Available in EQMP Enterprise Edition.",
        icon="ℹ️",
    )


def show():

    st.markdown("### Assessment Scope")

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.checkbox(
            "Backend",
            value=True,
            disabled=True,
        )

    with c2:

        if st.checkbox(
            "GitHub",
            value=False,
        ):
            unavailable()

    with c3:

        if st.checkbox(
            "API",
            value=False,
        ):
            unavailable()

    with c4:

        if st.checkbox(
            "Cloud",
            value=False,
        ):
            unavailable()

    with c5:

        if st.checkbox(
            "Network",
            value=False,
        ):
            unavailable()
