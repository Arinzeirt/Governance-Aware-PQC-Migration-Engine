# Cryptographic Asset Classification Improves PQC Readiness Visibility

Observation ID: 002
Date: 2026-06-14
Project: PQC Migration Engine
Case Study: Streple Backend

## Context

Following the identification of limitations associated with keyword-based cryptographic discovery, a classification layer was introduced into the PQC Migration Engine.

The objective was to move beyond simple detection of cryptographic terms and provide a more meaningful representation of cryptographic assets and their potential migration implications.

## Observation

The introduction of cryptographic asset classification significantly improved the visibility and interpretability of discovered cryptographic components.

Rather than reporting isolated keywords such as:

* RSA
* JWT
* crypto
* randomBytes

the system was able to classify findings into operational categories such as:

* RSA-OAEP Encryption
* Public Key Handling
* Digital Signature Verification
* JWT Authentication
* Cryptographically Secure Random Generation

This provided a more accurate representation of how cryptography is used within the assessed system.

## Evidence Collected

The Streple backend assessment identified the following classified assets:

| Asset Type             | Classification                             | PQC Relevance |
| ---------------------- | ------------------------------------------ | ------------- |
| Encryption Operation   | RSA-OAEP Encryption                        | High          |
| Encryption Operation   | Public Key Encryption                      | High          |
| Signature Verification | Digital Signature Verification             | High          |
| Key Management         | Public Key Handling                        | Medium        |
| Authentication         | JWT Authentication Service                 | Medium        |
| Authentication         | JWT Authentication Strategy                | Medium        |
| Randomness             | Cryptographically Secure Random Generation | Low           |

## Key Insight

Cryptographic discovery alone does not provide sufficient information for migration planning.

Organizations do not migrate keywords.

Organizations migrate cryptographic functions, protocols, keys, certificates, authentication mechanisms, and operational dependencies.

Asset classification transforms raw discovery data into information that can support migration analysis and decision-making.

## Implication for PQC Migration

Effective PQC readiness assessment requires understanding:

* What cryptographic assets exist
* How those assets are being used
* Where those assets are located
* Which assets are most exposed to quantum-related risks
* Which assets require migration prioritization

Asset classification provides the context necessary to answer these questions.

## Preliminary Research Insight

Cryptographic asset classification may serve as an intermediary layer between cryptographic discovery and migration planning.

A possible migration workflow is:

Discovery
↓
Classification
↓
Risk Assessment
↓
Migration Recommendation
↓
Governance Review
↓
Migration Execution

This approach provides significantly more migration intelligence than keyword discovery alone.

## Potential Contribution

A classification-driven PQC readiness framework may improve organizational visibility into cryptographic dependencies and support more accurate migration planning, prioritization, and governance decision-making within complex digital and financial infrastructures.
