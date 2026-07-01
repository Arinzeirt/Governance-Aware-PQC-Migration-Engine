import streamlit as st

from datetime import datetime


def show_assessment_details():

    now = datetime.now()

    assessment_date = now.strftime("%d %b %Y")
    assessment_time = now.strftime("%H:%M:%S")

    st.subheader("Assessment Details")

    st.metric("Repository", "Git")

    st.metric("Files", "15,080")

    st.metric("Languages", "5")

    st.metric("Project Size", "848 MB")

    st.metric("Status", "Completed")

    st.metric("Assessment Date", assessment_date)

    st.metric("Assessment Time", assessment_time)

    st.metric("Duration", "18 sec")
