import streamlit as st


def show_events(events):

    st.markdown("## Enterprise Event Log")

    if not events:
        st.info("Assessment session starting...")
        return

    for event in events:
        st.text(event)
