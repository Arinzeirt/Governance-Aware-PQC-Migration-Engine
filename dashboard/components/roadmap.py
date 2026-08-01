import streamlit as st


def show():

    st.subheader("Research Roadmap")

    phases = [

        (
            "2026",
            "Research Foundation",
            "Research notes, literature review, enterprise architecture and initial EQMP prototype.",
            "Active Research",
        ),

        (
            "Early 2027",
            "Framework Advancement",
            "Advance and mature the Governance Framework, Enterprise Quantum Readiness Framework, Migration Decision Engine and supporting research.",
            "Planned",
        ),

        (
            "Late 2027",
            "Prototype Deployment",
            "Deploy the EQMP prototype for enterprise validation, stakeholder engagement and pilot assessments.",
            "Planned",
        ),

        (
            "2027 – 2030",
            "Continuous Refinement",
            "Continuous platform refinement, publications, industry collaboration and research validation throughout the PhD.",
            "Ongoing",
        ),
    ]

    cols = st.columns(2)

    for index, (timeline, title, description, status) in enumerate(phases):

        with cols[index % 2]:

            with st.container(border=True):

                st.caption(timeline)

                st.markdown(
                    f"### {title}"
                )

                st.write(description)

                st.caption(f"Status: {status}")
