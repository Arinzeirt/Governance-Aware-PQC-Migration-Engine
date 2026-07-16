import streamlit as st


def show():

    #
    # FIRST ROW
    #
    left, right = st.columns([2, 1])

    with left:

        st.markdown("## Enterprise Scan Results")

        st.table({

            "Algorithm": [

                "RSA",

                "ECDSA",

                "ECDH",

                "TLS",

                "OpenSSL",

                "SHA-1",

                "SHA-256"

            ],

            "Occurrences":[

                132,

                48,

                31,

                67,

                56,

                18,

                221

            ]

        })

    with right:

        st.markdown("## Assessment Information")

        st.metric("Repository", "Git")

        st.metric("Files", "15,080")

        st.metric("Languages", "5")

        st.metric("Project Size", "848 MB")

        st.metric("Status", "Completed")

        st.metric("Duration", "18 sec")

    st.divider()

    #
    # SECOND ROW
    #
    left, right = st.columns([2,1])

    with left:

        st.markdown("## Compliance Readiness")

        st.table({

            "Framework":[

                "NDPC",

                "ISO/IEC 27001",

                "PCI DSS",

                "NIST PQC",

                "FIPS 203",

                "FIPS 204",

                "FIPS 205"

            ],

            "Status":[

                "Review Required",

                "Review Controls",

                "High Impact",

                "Migration Required",

                "Applicable",

                "Applicable",

                "Monitor"

            ]

        })

    with right:

        st.markdown("## Executive Decision")

        st.success("Governance-led Migration")

        st.metric("Overall Risk","HIGH")

        st.metric("Migration","Hybrid")

        st.metric("Priority","Phase 1")

        st.metric("Confidence","92%")
