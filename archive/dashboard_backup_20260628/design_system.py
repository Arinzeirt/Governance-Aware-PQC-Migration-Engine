import streamlit as st


def section_title(title, subtitle=None):

    st.markdown(f"## {title}")

    if subtitle:

        st.caption(subtitle)

    st.divider()


def executive_divider():

    st.divider()


def status_badge(status):

    colours = {

        "HIGH": "🔴",

        "MEDIUM": "🟠",

        "LOW": "🟢",

        "PENDING": "🟠",

        "VALID": "🟢",

        "PARTIAL": "🟠",

        "ADEQUATE": "🟢",

        "ACTION REQUIRED": "🔴",

        "MONITOR": "🟠",

        "HEALTHY": "🟢",

    }

    icon = colours.get(status, "⚪")

    st.markdown(f"**{icon} {status}**")


def executive_metric(label, value):

    st.metric(label, value)

