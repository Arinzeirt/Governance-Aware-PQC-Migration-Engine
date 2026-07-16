CLASSIFICATION_RULES = {
    "RSA-OAEP": {
        "asset_type": "Encryption Operation",
        "classification": "RSA-OAEP Encryption",
        "pqc_relevance": "High",
        "migration_direction": "Review for hybrid or PQC key establishment such as ML-KEM."
    },
    "publicKey.encrypt": {
        "asset_type": "Encryption Operation",
        "classification": "Public Key Encryption",
        "pqc_relevance": "High",
        "migration_direction": "Assess dependency on RSA/ECC and plan PQC-safe replacement."
    },
    "crypto.createPublicKey": {
        "asset_type": "Key Management",
        "classification": "Public Key Handling",
        "pqc_relevance": "Medium",
        "migration_direction": "Review public key lifecycle and future PQC certificate/key support."
    },
    "crypto.verify": {
        "asset_type": "Signature Verification",
        "classification": "Digital Signature Verification",
        "pqc_relevance": "High",
        "migration_direction": "Review for future PQC signatures such as ML-DSA or SLH-DSA."
    },
    "randomBytes": {
        "asset_type": "Randomness",
        "classification": "Cryptographically Secure Random Generation",
        "pqc_relevance": "Low",
        "migration_direction": "Usually not a direct PQC migration target, but should remain secure."
    },
    "JwtService": {
        "asset_type": "Authentication",
        "classification": "JWT Authentication Service",
        "pqc_relevance": "Medium",
        "migration_direction": "Review JWT signing algorithm and key management."
    },
    "passport-jwt": {
        "asset_type": "Authentication",
        "classification": "JWT Authentication Strategy",
        "pqc_relevance": "Medium",
        "migration_direction": "Review token verification algorithm and secret/key handling."
    }
}

def classify_content(content):
    classifications = []

    for pattern, info in CLASSIFICATION_RULES.items():
        if pattern in content:
            classifications.append({
                "pattern": pattern,
                "asset_type": info["asset_type"],
                "classification": info["classification"],
                "pqc_relevance": info["pqc_relevance"],
                "migration_direction": info["migration_direction"]
            })

    return classifications
