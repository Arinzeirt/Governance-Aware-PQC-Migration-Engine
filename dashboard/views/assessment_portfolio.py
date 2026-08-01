import streamlit as st


def show():

    st.title("Enterprise Assessment Portfolio")

    st.caption(
        "Manage enterprise cryptographic assessment projects throughout their lifecycle."
    )

    st.divider()

    left, right = st.columns([1, 4])

    with left:

        st.button(
            "New Assessment",
            type="primary",
            use_container_width=True,
        )

    st.write("")

    with st.container(border=True):

        st.subheader("No Assessment Projects")

        st.caption(
            "Create your first enterprise assessment to begin."
        )
