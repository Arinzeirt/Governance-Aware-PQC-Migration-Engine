import streamlit as st


def show_executive_summary(runtime):

    st.subheader("Executive Assessment")

    if runtime["running"]:

        st.info("Enterprise Assessment Running")

        st.progress(runtime["progress"] / 100)

        stages = {
            "Environment Validation": "Validating enterprise environment...",
            "Enterprise Scan": "Discovering cryptographic assets...",
            "Migration Readiness": "Calculating migration readiness...",
            "Governance Analysis": "Evaluating governance posture...",
            "Executive Decision": "Generating executive recommendations..."
        }

        st.markdown(
            f"**Current Operation:** {stages.get(runtime['stage'], runtime['stage'])}"
        )

        st.caption("Governance-Aware Post-Quantum Migration Assessment")

    elif runtime["complete"]:

        decision = runtime["decision"]

        st.success("Enterprise Assessment Completed Successfully")

        st.markdown(
            f"""
### Executive Summary

**Overall Risk:** {decision['threat']}

**Migration Readiness:** {decision['metrics']['average_readiness']}%

**Recommended Strategy:** {decision['strategy']}

**Confidence:** {decision['confidence']}%

The assessment identified cryptographic assets that require
post-quantum migration planning. Governance and compliance
activities should proceed alongside phased technical migration.
"""
        )

    else:

        st.info("Waiting to begin assessment...")
