GOVERNANCE_RULES = {

    "RSA-OAEP Encryption": {
        "owner": "Security Team",
        "criticality": "High",
        "approver": "CISO",
        "evidence": "Architecture Review",
        "migration_status": "Planned"
    },

    "Public Key Encryption": {
        "owner": "Security Team",
        "criticality": "High",
        "approver": "CISO",
        "evidence": "Cryptographic Assessment",
        "migration_status": "Planned"
    },

    "Digital Signature Verification": {
        "owner": "Security Team",
        "criticality": "High",
        "approver": "CISO",
        "evidence": "Signature Validation Review",
        "migration_status": "Planned"
    },

    "Public Key Handling": {
        "owner": "Infrastructure Team",
        "criticality": "Medium",
        "approver": "Security Manager",
        "evidence": "Key Management Review",
        "migration_status": "Under Review"
    },

    "JWT Authentication Service": {
        "owner": "Application Team",
        "criticality": "Medium",
        "approver": "Application Security Lead",
        "evidence": "Authentication Review",
        "migration_status": "Under Review"
    },

    "JWT Authentication Strategy": {
        "owner": "Application Team",
        "criticality": "Medium",
        "approver": "Application Security Lead",
        "evidence": "Authentication Review",
        "migration_status": "Under Review"
    },

    "Cryptographically Secure Random Generation": {
        "owner": "Platform Team",
        "criticality": "Low",
        "approver": "Security Manager",
        "evidence": "Periodic Review",
        "migration_status": "Monitor"
    }
}

def get_governance(classification):

    return GOVERNANCE_RULES.get(
        classification,
        {
            "owner": "Unknown",
            "criticality": "Unknown",
            "approver": "Unknown",
            "evidence": "Manual Assessment",
            "migration_status": "Unknown"
        }
    )
