# Coverage Assessment as a Missing Layer in PQC Migration

Observation ID: 005

Date: 2026-06-15

Project: PQC Migration Engine

Case Study: Streple Backend

## Context

Previous observations established that effective post-quantum migration extends beyond cryptographic discovery.

Observation 001 demonstrated the limitations of keyword-based discovery.

Observation 002 highlighted the importance of cryptographic asset classification.

Observation 003 explored readiness assessment and migration prioritization.

Observation 004 introduced governance as a critical component of migration planning by connecting technical findings to ownership, approval processes, evidence requirements, and accountability structures.

While extending the prototype further, another limitation became apparent.

Even when cryptographic assets are discovered, classified, prioritized, and assigned governance responsibilities, an important question remains:

Does the identified cryptographic mechanism provide sufficient protection for the asset it is intended to protect?

## Observation

Most migration assessments focus on identifying cryptographic mechanisms and determining where migration effort should be directed.

However, the existence of a cryptographic mechanism does not automatically imply that it provides adequate protection for the required security objective.

For example:

* RSA-OAEP may be correctly identified as an encryption mechanism.
* Digital signatures may be correctly identified as authenticity controls.
* JWT authentication services may be correctly identified as authentication infrastructure.

Yet these findings alone do not determine whether protection remains sufficient against future quantum threats.

## Prototype Findings

The current prototype successfully performs:

* Cryptographic Discovery
* Asset Classification
* Risk Assessment
* Migration Recommendation
* Governance Assignment
* Readiness Evaluation

These capabilities improve visibility into cryptographic assets and their migration requirements.

However, testing revealed that migration decisions still depend on an additional assessment:

* Does the mechanism adequately protect confidentiality requirements?
* Does it adequately protect authenticity requirements?
* Is the protection horizon sufficient for the operational lifetime of the asset?
* Is migration immediately required, or can the mechanism continue operating under current assumptions?

These questions cannot be answered through discovery or classification alone.

## Coverage Assessment Concept

To address this limitation, a Coverage Assessment Layer is proposed.

The purpose of this layer is to evaluate whether a classified cryptographic mechanism provides sufficient protection coverage for its intended security objective.

Potential coverage outcomes include:

* Covers
* Horizon Short
* Protection Gap
* Not Yet Assessed
* Not Applicable

This creates a distinction between visibility and adequacy.

## Key Insight

Organizations do not migrate cryptographic mechanisms simply because they exist.

Organizations migrate because existing mechanisms may no longer provide sufficient protection coverage for required business, security, or regulatory objectives.

As a result, migration decisions may require both visibility into cryptographic assets and an assessment of whether those assets continue to satisfy required protection goals.

## Implication for PQC Migration

A cryptographic asset may be:

* Discovered
* Classified
* Governed
* Prioritized

Yet still lack sufficient protection coverage for long-term operation.

Without coverage assessment, migration planning may remain informed but incomplete.

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
Migration Planning

This structure further shifts PQC migration away from inventory management and toward a governance-aware migration decision framework.

## Potential Contribution

This observation suggests that coverage assessment may provide an important bridge between cryptographic visibility and migration execution.

Coverage evaluation could help organizations determine not only what cryptography exists, but whether that cryptography remains adequate for future operational requirements.

## Future Work

Future prototype development will explore methods for representing and evaluating coverage within the migration engine.

Particular attention will be given to protection horizons, security objectives, governance requirements, and migration decision support for high-throughput financial systems.
