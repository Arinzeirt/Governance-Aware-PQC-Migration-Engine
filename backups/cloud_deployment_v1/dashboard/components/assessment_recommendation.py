import streamlit as st

from engine.runtime import runtime


def show():

    st.markdown("## Executive Recommendations")

    #
    # Immediate Actions
    #
    with st.container(border=True):

        st.markdown("### Immediate Actions")

        recommendations = [

            "Replace quantum-vulnerable cryptographic algorithms beginning with RSA-based implementations.",

            "Establish a complete enterprise cryptographic inventory and ownership register.",

            "Introduce cryptographic agility so algorithms can be replaced without application redesign.",

            "Prioritize Internet-facing and business-critical services for the first migration wave.",

            "Create a governance-led Post-Quantum Migration Program with executive oversight.",

        ]

        for item in recommendations:
            st.markdown(f"✓ {item}")

    st.write("")

    #
    # Governance + Compliance
    #
    left, right = st.columns(2)

    with left:

        with st.container(border=True):

            st.markdown("### Governance Framework")

            st.info(
"""
Enterprise Quantum Migration Governance Framework (EQMGF)

• Discover

• Classify

• Prioritize

• Govern

• Migrate

• Monitor
"""
            )

    with right:

        with st.container(border=True):

            st.markdown("### Regulatory & Compliance Alignment")

            st.success(
"""
✓ NIST SP 800-208
Quantum-resistant migration planning.

✓ NIST IR 8547
Maintain a complete cryptographic inventory.

✓ CNSA 2.0
Replace vulnerable public-key cryptography.

✓ DORA
Integrate PQC into ICT risk management.

✓ PCI DSS 4.0
Assess cryptographic controls protecting payment data.

✓ ISO/IEC 27001
Update cryptographic governance and key management.
"""
            )

    st.write("")

    #
    # Executive Recommendation
    #
    with st.container(border=True):

        st.markdown("### Executive Recommendation")

        if runtime.critical > 0:

            st.error(
                """
Immediate migration planning is strongly recommended.

Critical cryptographic assets have been identified that may be exposed to future quantum attacks.

**Recommended Executive Decision**

• Launch a governance-led PQC migration programme immediately.

• Prioritize Internet-facing and business-critical systems.

• Complete enterprise cryptographic discovery and ownership validation.

• Establish board-level oversight for migration execution.
"""
            )

        elif runtime.medium > 0:

            st.warning(
                """
Migration planning should begin.

Several medium-priority cryptographic assets require governance review and phased migration planning.

Focus should be placed on cryptographic inventory, dependency analysis, and migration readiness.
"""
            )

        else:

            st.success(
                """
Current assessment indicates a low migration priority.

Continue periodic discovery, governance reviews, and cryptographic agility planning to maintain post-quantum readiness.
"""
            )
