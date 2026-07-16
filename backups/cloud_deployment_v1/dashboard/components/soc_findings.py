import streamlit as st


def show_findings(findings):

    st.markdown("### Live Findings")

    if not findings:
        st.text("Waiting for discoveries...")
        return

    output = ""

    for item in findings:
        output += f"✅ {item}\n"

    st.text(output)

