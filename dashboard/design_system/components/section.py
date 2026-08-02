import streamlit as st


def show(
    title,
    subtitle="",
):

    st.write("")

    st.markdown(f"# {title}")

    if subtitle:

        st.caption(subtitle)

    st.write("")
