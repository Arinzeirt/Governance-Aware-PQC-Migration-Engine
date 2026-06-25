RISK_RULES = {
    "RSA": {
        "risk": "High",
        "pqc_status": "Migration Required",
        "reason": "RSA is vulnerable to future cryptographically relevant quantum computers."
    },
    "ECC": {
        "risk": "High",
        "pqc_status": "Migration Required",
        "reason": "ECC is vulnerable to Shor's algorithm."
    },
    "ECDSA": {
        "risk": "High",
        "pqc_status": "Migration Required",
        "reason": "ECDSA depends on elliptic curve cryptography."
    },
    "ECDH": {
        "risk": "High",
        "pqc_status": "Migration Required",
        "reason": "ECDH depends on elliptic curve discrete logarithms."
    },
    "TLS": {
        "risk": "Medium",
        "pqc_status": "Review Required",
        "reason": "TLS may depend on RSA or ECC certificates and key exchange."
    },
    "SSL": {
        "risk": "High",
        "pqc_status": "Replace Immediately",
        "reason": "SSL is obsolete and should not be used."
    },
    "OpenSSL": {
        "risk": "Medium",
        "pqc_status": "Review Library Configuration",
        "reason": "OpenSSL usage requires checking enabled algorithms and protocol versions."
    },
    "SHA-256": {
        "risk": "Low",
        "pqc_status": "Generally Acceptable",
        "reason": "SHA-256 is not broken by quantum attacks, though Grover's algorithm reduces effective security."
    }
}

def assess_risk(algorithm):
    return RISK_RULES.get(algorithm, {
        "risk": "Unknown",
        "pqc_status": "Manual Review Required",
        "reason": "No rule exists yet for this cryptographic indicator."
    })
