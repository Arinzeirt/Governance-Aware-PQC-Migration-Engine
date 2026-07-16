RECOMMENDATIONS = {
    "RSA-OAEP Encryption": {
        "priority": "High",
        "recommendation": "Evaluate hybrid RSA + ML-KEM deployment.",
        "timeline": "Near-Term"
    },

    "Public Key Encryption": {
        "priority": "High",
        "recommendation": "Review public key encryption dependencies and PQC alternatives.",
        "timeline": "Near-Term"
    },

    "Digital Signature Verification": {
        "priority": "High",
        "recommendation": "Evaluate migration path toward ML-DSA or SLH-DSA.",
        "timeline": "Near-Term"
    },

    "Public Key Handling": {
        "priority": "Medium",
        "recommendation": "Review certificate and key lifecycle management for crypto agility.",
        "timeline": "Mid-Term"
    },

    "JWT Authentication Service": {
        "priority": "Medium",
        "recommendation": "Review signing algorithms and key management dependencies.",
        "timeline": "Mid-Term"
    },

    "JWT Authentication Strategy": {
        "priority": "Medium",
        "recommendation": "Assess authentication infrastructure for PQC readiness.",
        "timeline": "Mid-Term"
    },

    "Cryptographically Secure Random Generation": {
        "priority": "Low",
        "recommendation": "Monitor but typically not a direct PQC migration target.",
        "timeline": "Long-Term"
    }
}

def get_recommendation(classification):
    return RECOMMENDATIONS.get(
        classification,
        {
            "priority": "Unknown",
            "recommendation": "Manual review required.",
            "timeline": "Unknown"
        }
    )
