# Migration Decision Support as the Next Layer in PQC Migration

Observation ID: 006

Date: 2026-06-16

Project: PQC Migration Engine

Case Study: Streple Backend

## Context

Previous observations established that effective post-quantum migration requires more than cryptographic discovery.

Observation 001 demonstrated the limitations of keyword-based discovery.

Observation 002 highlighted the importance of cryptographic asset classification.

Observation 003 introduced readiness assessment and migration prioritization.

Observation 004 established governance as a critical component of migration planning.

Observation 005 proposed coverage assessment as a mechanism for determining whether identified cryptographic mechanisms continue to provide sufficient protection for future operational requirements.

Together, these capabilities significantly improve visibility into cryptographic assets and their migration requirements.

However, while extending the prototype further, another limitation became apparent.

Even when cryptographic assets are discovered, classified, governed, prioritized, and assessed for protection coverage, an important question remains:

How should organizations transform these findings into actionable migration decisions?

## Observation

The current prototype produces multiple forms of migration intelligence, including:

* Asset Classification
* Risk Assessment
* Readiness Evaluation
* Governance Assignment
* Coverage Assessment
* Migration Recommendations

While these outputs provide valuable information, they remain individual assessment results.

Migration teams must still determine:

* Which assets should migrate first?
* Which findings require immediate attention?
* Whether governance conditions support migration execution?
* Whether migration planning should begin immediately or remain under review?

As the number of identified cryptographic assets increases, manual interpretation of assessment results becomes increasingly difficult.

## Prototype Findings

Testing against the Streple backend demonstrated that multiple assessment layers can be combined to support migration decisions.

Examples include:

### RSA-OAEP Encryption

* High Priority
* Horizon Short Coverage
* Planned Migration Status

### Digital Signature Verification

* High Priority
* Horizon Short Coverage
* Planned Migration Status

### JWT Authentication

* Medium Priority
* Coverage Not Yet Assessed
* Under Review

These findings individually describe migration concerns.

Collectively, however, they begin to indicate broader migration requirements.

For example:

* Multiple high-priority assets may indicate elevated migration urgency.
* Coverage gaps may indicate insufficient long-term protection.
* Governance review requirements may delay migration execution.
* Readiness scores may influence migration sequencing.

## Decision Support Concept

To address this limitation, a Migration Decision Support Layer is proposed.

The purpose of this layer is to transform discovery and assessment outputs into explainable migration recommendations.

Potential decision outcomes include:

* Monitor Current State
* Continue Assessment
* Governance Review Required
* Activate Hybrid PQC Planning
* Initiate Migration Execution

This introduces a distinction between assessment and decision-making.

## Key Insight

Organizations do not migrate cryptographic assets solely because vulnerabilities or dependencies have been identified.

Organizations migrate because available evidence indicates that migration action is required.

As a result, migration systems may require a dedicated decision-support capability capable of interpreting assessment outputs and producing actionable recommendations.

## Implication for PQC Migration

A cryptographic asset may be:

* Discovered
* Classified
* Prioritized
* Governed
* Coverage Assessed

Yet migration decisions may still depend on additional interpretation.

Without a decision-support layer, migration planning may remain information-rich but action-poor.

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

Coverage Assessment

↓

Decision Support

↓

Migration Planning

This structure further shifts PQC migration away from cryptographic inventory management and toward governance-aware migration orchestration.

## Potential Contribution

This observation suggests that migration decision support may provide an important bridge between migration assessment and migration execution.

Decision-support capabilities could help organizations determine not only what cryptography exists and whether it remains adequate, but also what actions should be performed next.

## Future Work

Future prototype development will explore automated migration decision generation based on:

* Risk Levels
* Coverage Status
* Governance Conditions
* Readiness Scores
* Migration Priorities

Particular attention will be given to explainable decision generation, governance traceability, and adaptive migration recommendations for high-throughput financial systems.
