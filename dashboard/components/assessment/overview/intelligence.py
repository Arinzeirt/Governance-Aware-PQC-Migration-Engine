import streamlit as st


def show():

    with st.container(border=True):

        left, right = st.columns(
            [2, 3],
            gap="large",
        )

        with left:

            st.image(
                "assets/images/quantum_brief.png",
                use_container_width=True,
            )

        with right:

            st.markdown(
                """
### 🛡 Quantum Intelligence Brief
"""
            )

            st.markdown(
                """
## Harvest Now, Decrypt Later
"""
            )

            st.write(
                """
Sensitive encrypted data protected by today's public-key
cryptography may already be harvested and stored by
adversaries. Once cryptographically relevant quantum
computers become available, that data could be decrypted.

Understanding where cryptography exists across your
organisation is therefore the first step toward a successful
governance-aware migration.
"""
            )

            st.markdown("#### Why It Matters")

            st.markdown(
                """
- Discover hidden cryptographic assets.

- Prioritise migration based on organisational risk.

- Support governance and regulatory readiness.

- Build an evidence-driven migration roadmap.
"""
            )

            st.caption(
                "📖 Research Brief • Estimated Reading Time: 20 seconds"
            )
