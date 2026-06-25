# From Classification to Coverage: Why PQC Migration Requires Asset-Level Coverage Assessment

Observation ID: 003

Date: 2026-06-15

Project: PQC Migration Engine

Case Study: Streple Backend

## Context

Previous observations established that cryptographic discovery alone provides limited visibility into post-quantum migration requirements.

Observation 001 demonstrated that keyword-based discovery often identifies cryptographic indicators without revealing how cryptography is actually used.

Observation 002 showed that cryptographic asset classification improves visibility by identifying operational functions such as encryption, digital signatures, authentication mechanisms, public key management, and randomness generation.

During further discussion and review of prototype findings, a new question emerged:

Is identifying and classifying a cryptographic mechanism sufficient to support migration decisions?

## Observation

The answer appears to be no.

Classification explains what a cryptographic mechanism does, but it does not necessarily explain whether that mechanism provides adequate protection for the asset it is intended to secure.

For example, identifying an RSA-OAEP encryption operation reveals the presence of public-key encryption.

However, the classification alone does not answer:

* What asset is being protected?
* What security property is required?
* How long must protection remain effective?
* What threat assumptions are being considered?
* What regulatory obligations apply?
* What evidence supports the current protection posture?

These questions influence migration decisions just as much as the underlying cryptographic mechanism.

## Evidence from Prototype Assessment

The prototype successfully identified and classified:

* RSA-OAEP Encryption
* Public Key Encryption
* Digital Signature Verification
* Public Key Handling
* JWT Authentication Services
* Cryptographically Secure Random Generation

While classification improved visibility, it became apparent that migration priorities cannot be determined solely by the type of cryptographic mechanism identified.

Two systems may both contain RSA-based encryption while having very different migration requirements depending on the assets protected and the expected protection horizon.

## Key Insight

Organizations do not migrate keywords.

Organizations do not even migrate cryptographic mechanisms in isolation.

Organizations migrate protection requirements.

A migration decision ultimately depends on whether existing cryptographic controls continue to provide sufficient coverage for required security objectives under future threat conditions.

## Coverage Assessment Concept

A potential intermediate layer between classification and migration planning is coverage assessment.

Possible workflow:

Discovery
↓
Classification
↓
Coverage Assessment
↓
Risk Assessment
↓
Migration Recommendation
↓
Governance Review
↓
Migration Execution

Coverage assessment seeks to determine whether a cryptographic mechanism adequately protects a particular asset against anticipated threats over the required protection horizon.

## Example

Finding:

RSA-OAEP Encryption

Classification Outcome:

Public Key Encryption

Coverage Questions:

* Is long-term confidentiality required?
* Is the asset exposed to harvest-now-decrypt-later risk?
* What is the expected data retention period?
* Does the protection requirement extend beyond expected quantum readiness timelines?

Potential Coverage Verdict:

* Covered
* Horizon-Short
* Dimension-Short
* Not Covered
* Not Assessable

## Implication for PQC Migration

This observation suggests that visibility alone may not be sufficient for effective post-quantum migration planning.

Organizations may require mechanisms that evaluate not only what cryptography exists and how it is used, but also whether existing protections remain adequate against future threat scenarios.

Coverage assessment may therefore represent an important bridge between cryptographic classification and governance-aware migration decision-making.

## Preliminary Research Direction

Future development of the PQC Migration Engine may explore asset-level coverage assessment as a decision-support layer capable of evaluating protection adequacy, migration urgency, and governance requirements within complex digital and financial infrastructures.

## Potential Contribution

A governance-aware PQC migration framework that incorporates discovery, classification, coverage assessment, risk evaluation, and migration recommendations may provide a more comprehensive basis for post-quantum migration planning than cryptographic discovery alone.
