import streamlit as st

from components.assessment.store import save, load
from components.assessment.validation import cryptography_complete


def show():

    existing = load("cryptography")

    with st.container(border=True):

        st.markdown("## Cryptographic Posture")

        st.caption(
            "Identify the cryptographic mechanisms, assets and dependencies that influence quantum exposure."
        )

        left, right = st.columns(2, gap="small")

        with left:

            st.multiselect(
                "Cryptographic Algorithms in Use *",
                [
                    "RSA",
                    "ECC",
                    "AES",
                    "SHA-2",
                    "SHA-3",
                    "HMAC",
                    "Ed25519",
                    "Other",
                    "Unknown",
                ],
                key="crypto_algorithms",
                default=existing.get(
                    "crypto_algorithms",
                    [],
                ),
                placeholder="Select algorithms",
            )

            st.multiselect(
                "Cryptographic Technologies *",
                [
                    "TLS / SSL",
                    "PKI",
                    "VPN",
                    "SSH",
                    "Code Signing",
                    "Database Encryption",
                    "Email Encryption",
                    "Hardware Security Modules",
                    "Digital Certificates",
                ],
                key="crypto_technologies",
                default=existing.get(
                    "crypto_technologies",
                    [],
                ),
                placeholder="Select technologies",
            )

            st.multiselect(
                "Critical Systems Using Cryptography *",
                [
                    "Internet Banking",
                    "Mobile Applications",
                    "Internal Business Applications",
                    "APIs",
                    "Email Systems",
                    "VPN",
                    "Identity & Access Management",
                    "Database Servers",
                    "File Storage",
                    "Payment Systems",
                    "Cloud Workloads",
                    "DevOps / CI-CD",
                    "Endpoints",
                    "IoT / OT Systems",
                    "Other",
                ],
                key="crypto_business_systems",
                default=existing.get(
                    "crypto_business_systems",
                    [],
                ),
                placeholder="Select critical systems",
            )

        with right:

            st.selectbox(
                "PKI Maturity *",
                [
                    "Fully Managed",
                    "Partially Managed",
                    "Limited Visibility",
                    "Unknown",
                ],
                key="pki_maturity",
                index=None,
                placeholder="Select PKI maturity",
            )

            st.selectbox(
                "Certificate Inventory *",
                [
                    "Complete",
                    "Partial",
                    "None",
                    "Unknown",
                ],
                key="certificate_inventory",
                index=None,
                placeholder="Select inventory status",
            )

            st.radio(
                "Cryptographic Asset Inventory *",
                ["Yes", "No", "In Progress"],
                horizontal=True,
                key="crypto_inventory",
            )

            st.radio(
                "Cryptographic Agility *",
                ["Yes", "No", "Unknown"],
                horizontal=True,
                key="crypto_agility",
            )

            st.radio(
                "Long-Term Sensitive Data *",
                ["Yes", "No", "Unknown"],
                horizontal=True,
                key="long_term_data",
            )

    data = {
        "crypto_algorithms":
            st.session_state.get(
                "crypto_algorithms",
                [],
            ),

        "crypto_technologies":
            st.session_state.get(
                "crypto_technologies",
                [],
            ),

        "crypto_business_systems":
            st.session_state.get(
                "crypto_business_systems",
                [],
            ),

        "pki_maturity":
            st.session_state.get(
                "pki_maturity"
            ),

        "certificate_inventory":
            st.session_state.get(
                "certificate_inventory"
            ),

        "crypto_inventory":
            st.session_state.get(
                "crypto_inventory"
            ),

        "crypto_agility":
            st.session_state.get(
                "crypto_agility"
            ),

        "long_term_data":
            st.session_state.get(
                "long_term_data"
            ),
    }

    save(
        "cryptography",
        data,
    )

    completed, total = cryptography_complete(
        data
    )

    return {
        "completed": completed,
        "total": total,
        "can_continue": completed == total,
        "on_continue": lambda: save(
            "cryptography",
            data,
        ),
    }
