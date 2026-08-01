import streamlit as st


def show(
    title: str,
    industry: str,
    status: str,
    button_label: str = "View Case Study",
    disabled: bool = True,
):

    with st.container(border=True):

        st.caption("Case Study")

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
            st.caption("Industry")
            st.write(industry)

        with right:
            st.caption("Status")
            st.write(status)

        st.button(
            button_label,
            key=f"case_{title}",
            use_container_width=True,
            disabled=disabled,
        )
