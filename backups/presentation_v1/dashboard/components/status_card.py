import streamlit as st


def show_status_card(title, value, colour="blue"):

    colours = {
        "red": "🔴",
        "orange": "🟠",
        "green": "🟢",
        "blue": "🔵",
    }

    icon = colours.get(colour, "⚪")

    with st.container(border=True):

        st.caption(title)

        st.markdown(
            f"## {icon} {value}"
        )

