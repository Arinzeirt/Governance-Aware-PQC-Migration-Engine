import streamlit as st


def show(
    title,
    description,
    item_id,
    button_label="View Details",
):
    disabled = button_label == "Coming Soon"

    with st.container(border=True):

        # Fixed-height title area
        st.markdown(
            f"""
<div style="
height:80px;
display:flex;
align-items:flex-start;
font-size:28px;
font-weight:700;
line-height:1.25;
">
{title}
</div>
""",
            unsafe_allow_html=True,
        )

        # Fixed-height description area
        st.markdown(
            f"""
<div style="
height:90px;
color:#CBD5E1;
font-size:15px;
line-height:1.6;
overflow:hidden;
">
{description}
</div>
""",
            unsafe_allow_html=True,
        )

        st.write("")

        if st.button(
            button_label,
            key=f"research_{item_id}",
            use_container_width=True,
            disabled=disabled,
        ):
            st.session_state.research_item = title
            st.session_state.page = "research_detail"
            st.rerun()
