import streamlit as st


def show(icon, title, page):

    active = (
        st.session_state.page == page
    )

    label = f"{icon}  {title}"

    if active:
        label = f"🟦 {icon}  {title}"

    if st.button(
        label,
        use_container_width=True,
        key=f"nav_{page}"
    ):
        st.session_state.page = page
        st.rerun()

