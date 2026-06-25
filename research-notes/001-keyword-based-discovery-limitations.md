# Limitations of Keyword-Based Cryptographic Discovery for PQC Readiness Assessment

Observation ID: 001
Date: 2026-06-14
Project: PQC Migration Engine
Case Study: Streple Backend

## Context

As part of the development of the Governance-Aware Post-Quantum Cryptographic Migration Engine, an initial cryptographic discovery scan was conducted against the Streple backend system.

The current discovery module relies primarily on keyword-based identification of cryptographic assets.

## Observation

The initial scan identified an RSA-related finding within the wallet service module.

Further manual inspection revealed that the finding corresponded to an active RSA-OAEP encryption operation rather than a simple keyword occurrence.

Example:

publicKey.encrypt(..., 'RSA-OAEP', ...)

Additional inspection identified several other cryptographic and security-related operations within the backend, including:

- Public key handling
- Digital signature verification
- RSA-OAEP encryption
- Symmetric or application-level encryption
- Cryptographically secure random number generation
- JWT-based authentication

## Evidence Collected

The following evidence categories were identified during the Streple backend assessment:

| Evidence Pattern | Classification |
|---|---|
| crypto.createPublicKey(...) | Public Key Handling |
| crypto.verify(...) | Digital Signature Verification |
| publicKey.encrypt(..., 'RSA-OAEP', ...) | RSA-OAEP Encryption |
| security.encrypt(...) | Symmetric or Application-Level Encryption |
| crypto.randomBytes(...) / randomBytes(...) | Secure Random Generation |
| JwtService / passport-jwt / jwtConstants.secret | JWT Authentication |

No direct `crypto.createHash(...)` usage was identified during this scan.

## Key Insight

Keyword-based cryptographic discovery is insufficient for accurate PQC readiness assessment.

A keyword match such as "RSA" does not reveal the actual nature of the cryptographic asset. The same indicator may represent:

- Cryptographic algorithms
- Cryptographic operations
- Key material
- Certificates
- Library imports
- Encrypted payloads
- Protocol implementations
- Authentication mechanisms

Each category has different migration implications and risk levels.

## Implication for PQC Migration

Accurate post-quantum migration planning requires context-aware cryptographic asset discovery capable of distinguishing between:

- Algorithms
- Cryptographic operations
- Key management functions
- Certificates and key material
- Cryptographic libraries
- Security protocols
- Authentication mechanisms
- Application-level encryption functions

rather than relying solely on keyword matching.

## Preliminary Research Insight

The effectiveness of PQC migration planning depends not only on discovering cryptographic assets, but also on correctly classifying their operational role within the system.

For example:

- RSA-OAEP encryption may require future migration toward quantum-resistant key establishment or hybrid encryption mechanisms.
- Digital signature verification may require future evaluation against PQC signature schemes such as ML-DSA or SLH-DSA.
- Secure random generation is cryptographically relevant but is not itself a direct PQC migration target.
- JWT usage may depend on the underlying signing algorithm and key-management approach.

This suggests that future PQC discovery tools should move beyond pattern matching toward semantic cryptographic asset classification and automated inventory generation.

## Potential Contribution

A context-aware cryptographic discovery and classification framework may provide more accurate PQC readiness assessments than traditional keyword-based discovery approaches, particularly within complex financial and digital asset infrastructures.
