import streamlit as st


def show(step, title, description):

    with st.container(border=True):

        st.markdown(f"## {step}")

        st.markdown(f"### {title}")

        st.caption(description)
