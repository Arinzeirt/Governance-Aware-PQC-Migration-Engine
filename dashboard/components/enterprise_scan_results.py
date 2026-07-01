import streamlit as st


def show_enterprise_scan_results(runtime):

    st.subheader("Enterprise Scan Results")

    inventory = runtime.get("inventory", [])

    keyword_counts = {}

    for item in inventory:

        if item.get("finding_type") != "keyword":
            continue

        algorithm = item.get("algorithm", "Unknown")

        keyword_counts[algorithm] = (
            keyword_counts.get(algorithm, 0) + 1
        )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "RSA",
            keyword_counts.get("RSA", 0)
        )

        st.metric(
            "ECDSA",
            keyword_counts.get("ECDSA", 0)
        )

        st.metric(
            "ECDH",
            keyword_counts.get("ECDH", 0)
        )

    with col2:

        st.metric(
            "TLS",
            keyword_counts.get("TLS", 0)
        )

        st.metric(
            "SHA-1",
            keyword_counts.get("SHA-1", 0)
        )

        st.metric(
            "SHA-256",
            keyword_counts.get("SHA-256", 0)
        )

    with col3:

        st.metric(
            "OpenSSL",
            keyword_counts.get("OpenSSL", 0)
        )

        st.metric(
            "Inventory",
            len(inventory)
        )

        high = sum(
            1
            for item in inventory
            if item.get("risk") == "High"
        )

        st.metric(
            "High Risk",
            high
        )
