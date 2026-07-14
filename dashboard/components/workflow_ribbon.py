import streamlit as st

from engine.session import session


STAGES = [

    "INITIALIZING",

    "TARGET",

    "DISCOVERY",

    "INVENTORY",

    "REPORT",

    "COMPLETED",

]


def status(index, current):

    if index < current:

        return "🟢"

    elif index == current:

        return "🔵"

    return "⚪"


def show():

    current = -1

    if session.state in STAGES:

        current = STAGES.index(

            session.state

        )

    cols = st.columns(

        len(STAGES)

    )

    for i, stage in enumerate(STAGES):

        with cols[i]:

            st.markdown(

                f"### {status(i,current)}"

            )

            st.caption(

                stage.title()

            )

