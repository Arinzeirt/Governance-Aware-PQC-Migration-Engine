import streamlit as st


def show(
    title,
    description,
    item_id,
    button_label="View Details",
):
    with st.container(border=True):

        st.subheader(title)

        st.write(description)

        st.write("")

        if st.button(
            button_label,
            key=f"research_{item_id}",
            use_container_width=True,
        ):
            st.session_state.research_item = title
            st.session_state.page = "research_detail"
            st.rerun()
