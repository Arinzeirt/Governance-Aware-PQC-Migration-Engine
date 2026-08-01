import streamlit as st


def show(
    title: str,
    venue: str,
    status: str,
    year: str,
    button_label: str = "View Publication",
    disabled: bool = True,
):

    with st.container(border=True):

        st.caption("Publication")

        st.markdown(
            f"""
<div style="
height:72px;
font-size:20px;
font-weight:700;
line-height:1.35;
overflow:hidden;
margin-bottom:18px;
">
{title}
</div>
""",
            unsafe_allow_html=True,
        )

        left, right = st.columns(2)

        with left:
            st.caption("Status")
            st.write(status)

        with right:
            st.caption("Target")
            st.write(venue)

        st.caption("Expected Publication")
        st.write(year)

        st.button(
            button_label,
            key=f"pub_{title}",
            use_container_width=True,
            disabled=disabled,
        )
