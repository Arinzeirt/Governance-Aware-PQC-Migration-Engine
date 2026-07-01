# Governance as a First-Class Component of PQC Migration

Observation ID: 004

Date: 2026-06-15

Project: PQC Migration Engine

Case Study: Streple Backend

## Context

Previous observations established that effective post-quantum migration requires more than cryptographic discovery.

Observation 001 demonstrated the limitations of keyword-based discovery.

Observation 002 showed the importance of cryptographic asset classification.

Observation 003 introduced the concept of coverage assessment as a mechanism for evaluating whether existing cryptographic protections remain adequate under future threat conditions.

While developing the prototype further, another limitation became apparent.

Even when cryptographic assets are identified, classified, risk-rated, and associated with migration recommendations, an important question remains:

Who is responsible for acting on the findings?

## Observation

Most cryptographic migration discussions focus heavily on technology.

Algorithms.

Protocols.

Performance.

Interoperability.

However, real-world migration decisions are rarely driven by technical findings alone.

Migration activities often require:

* Ownership assignment
* Risk acceptance decisions
* Evidence collection
* Compliance validation
* Management approval
* Change governance processes

Without governance structures, cryptographic findings may remain visible but not actionable.

## Prototype Findings

During assessment of the Streple Backend system, the prototype successfully identified:

* RSA-OAEP Encryption
* Public Key Encryption
* Digital Signature Verification
* JWT Authentication Services
* Public Key Management Functions
* Cryptographically Secure Random Number Generation

The technical findings were useful, but they did not answer governance questions such as:

* Which team owns the asset?
* Who approves migration decisions?
* What evidence must be collected?
* What is the current migration status?
* Which findings require immediate attention?

To address this limitation, a governance layer was introduced into the prototype.

## Governance Model

Each classified asset was enriched with governance metadata:

* Owner
* Criticality
* Approver
* Required Evidence
* Migration Status

Example:

RSA-OAEP Encryption

Owner: Security Team

Criticality: High

Approver: CISO

Evidence Required: Architecture Review

Migration Status: Planned

This transformed technical findings into governance-aware migration records.

## Key Insight

Organizations do not migrate cryptography through discovery alone.

Organizations migrate through decisions.

Those decisions are influenced by governance structures that determine ownership, accountability, evidence requirements, approval workflows, and implementation priorities.

As a result, governance should not be treated as a supporting activity after migration planning.

Governance may itself be a core component of migration planning.

## Implication for PQC Migration

A technically accurate migration recommendation may still fail if:

* Ownership is unclear
* Approval authority is undefined
* Evidence requirements are missing
* Migration responsibilities are not assigned

Therefore, successful post-quantum migration may require both technical readiness and governance readiness.

## Emerging Framework

Current prototype evolution:

Discovery
↓
Classification
↓
Risk Assessment
↓
Migration Recommendation
↓
Governance Assessment
↓
Migration Planning

This structure begins to move PQC migration away from simple cryptographic inventory management and toward a governance-aware decision-support framework.

## Potential Contribution

This observation suggests that governance metadata may provide an important bridge between technical cryptographic assessment and organizational migration execution.

Future work will explore how governance mechanisms can be integrated into adaptive and governance-aware PQC migration frameworks for financial and digital infrastructures.
