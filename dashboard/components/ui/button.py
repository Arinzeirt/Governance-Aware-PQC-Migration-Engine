import streamlit as st


def primary(label, key):

    return st.button(
        label,
        key=key,
        type="primary",
        use_container_width=True,
    )
