import streamlit as st


def show(
    title="",
    body="",
    icon="",
):

    with st.container(border=True):

        top, = st.columns(1)

        with top:

            if icon:

                st.markdown(f"# {icon}")

            if title:

                st.markdown(
                    f"### {title}"
                )

            if body:

                st.caption(body)

        st.write("")
