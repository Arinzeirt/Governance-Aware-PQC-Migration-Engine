def assess_coverage(classification):

    coverage_map = {

        "RSA-OAEP Encryption": {
            "coverage_status": "Horizon Short",
            "coverage_reason":
            "Relies on RSA which is vulnerable to future quantum attacks."
        },

        "Public Key Encryption": {
            "coverage_status": "Horizon Short",
            "coverage_reason":
            "Public key protection requires PQC migration planning."
        },

        "Digital Signature Verification": {
            "coverage_status": "Horizon Short",
            "coverage_reason":
            "Future migration toward ML-DSA or SLH-DSA should be considered."
        },

        "JWT Authentication Strategy": {
            "coverage_status": "Not Yet Assessed",
            "coverage_reason":
            "Coverage depends on underlying signing algorithms."
        },

        "JWT Authentication Service": {
            "coverage_status": "Not Yet Assessed",
            "coverage_reason":
            "Authentication mechanisms require further evaluation."
        },

        "Public Key Handling": {
            "coverage_status": "Not Yet Assessed",
            "coverage_reason":
            "Key lifecycle coverage requires further review."
        },

        "Cryptographically Secure Random Generation": {
            "coverage_status": "Covers",
            "coverage_reason":
            "Random generation remains generally suitable."
        }
    }

    return coverage_map.get(
        classification,
        {
            "coverage_status": "Unknown",
            "coverage_reason": "No coverage rule defined."
        }
    )
