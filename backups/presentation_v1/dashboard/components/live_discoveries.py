import streamlit as st

from engine.runtime import runtime


def show():

    st.markdown("## Latest Discoveries")

    if not runtime.discoveries:

        st.info(

            "No discoveries yet."

        )

        return

    for item in runtime.discoveries:

        with st.container(border=True):

            st.markdown(

                f"""
**{item['algorithm']}**

`{item['file']}`

{item['time']}
"""

            )

