READINESS_RULES = {
    "RSA-OAEP Encryption": {
        "readiness_score": 35,
        "urgency": "High",
        "coverage_status": "Not Yet Assessed"
    },
    "Public Key Encryption": {
        "readiness_score": 40,
        "urgency": "High",
        "coverage_status": "Not Yet Assessed"
    },
    "Digital Signature Verification": {
        "readiness_score": 45,
        "urgency": "High",
        "coverage_status": "Not Yet Assessed"
    },
    "Public Key Handling": {
        "readiness_score": 55,
        "urgency": "Medium",
        "coverage_status": "Not Yet Assessed"
    },
    "JWT Authentication Service": {
        "readiness_score": 60,
        "urgency": "Medium",
        "coverage_status": "Not Yet Assessed"
    },
    "JWT Authentication Strategy": {
        "readiness_score": 60,
        "urgency": "Medium",
        "coverage_status": "Not Yet Assessed"
    },
    "Cryptographically Secure Random Generation": {
        "readiness_score": 80,
        "urgency": "Low",
        "coverage_status": "Generally Adequate"
    }
}

def assess_readiness(classification):
    return READINESS_RULES.get(
        classification,
        {
            "readiness_score": 50,
            "urgency": "Unknown",
            "coverage_status": "Manual Assessment Required"
        }
    )
