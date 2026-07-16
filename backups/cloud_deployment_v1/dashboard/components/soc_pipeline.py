import streamlit as st


def show_pipeline(completed, current, pending):

    st.markdown("### Assessment Pipeline")

    text = ""

    for stage in completed:
        text += f"✅ {stage}\n"

    text += f"\n🔄 {current}\n"

    for stage in pending:
        text += f"\n⬜ {stage}"

    st.text(text)

