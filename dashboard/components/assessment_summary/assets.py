import streamlit as st

from engine.runtime import runtime


def show():

    st.divider()

    st.markdown(
        "### Cryptographic Assets Identified"
    )

    if runtime.discoveries:

        displayed = set()

        cols = st.columns(3)

        index = 0

        for item in runtime.discoveries:

            if item["title"] in displayed:
                continue

            displayed.add(item["title"])

            with cols[index % 3]:

                with st.container(border=True):

                    st.markdown(
                        f"#### {item['title']}"
                    )

                    st.caption(
                        f"Risk Level: {item['severity']}"
                    )

            index += 1

    else:

        st.info(
            "No cryptographic assets were identified during this assessment."
        )
