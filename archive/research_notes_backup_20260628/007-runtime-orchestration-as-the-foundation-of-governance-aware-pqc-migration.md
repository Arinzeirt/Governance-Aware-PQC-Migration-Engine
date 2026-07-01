# Runtime Orchestration as the Foundation of Governance-Aware PQC Migration

Observation ID: 007

Date: 2026-06-28

Project: PQC Migration Engine

Case Study: EQMP (Enet Quantum Migration Platform)

## Context

Previous observations established that effective post-quantum migration extends beyond cryptographic discovery.

Observation 001 demonstrated the limitations of keyword-based discovery.

Observation 002 introduced cryptographic asset classification as an essential capability for understanding the role of identified cryptographic mechanisms.

Observation 003 proposed migration readiness assessment to support migration prioritisation.

Observation 004 established governance as an essential component of migration planning.

Observation 005 introduced coverage assessment to determine whether existing cryptographic protections remain sufficient for future operational requirements.

Observation 006 proposed a migration decision-support layer capable of transforming multiple assessment outputs into actionable migration recommendations.

Together, these observations significantly expanded the capabilities of the prototype beyond cryptographic inventory generation.

However, while integrating these capabilities into a unified enterprise platform, another architectural limitation became apparent.

## Observation

The prototype now contains multiple specialised assessment components including:

* Cryptographic Discovery
* Asset Classification
* Migration Readiness Assessment
* Governance Assessment
* Coverage Assessment
* Decision Support

Each capability successfully performs its intended function.

However, these capabilities currently operate as individual processing stages.

The platform itself lacks a dedicated mechanism responsible for coordinating the complete assessment lifecycle.

As additional assessment capabilities were introduced, maintaining a coherent execution sequence became increasingly difficult.

This raised an important architectural question:

**Who coordinates the migration assessment?**

## Prototype Findings

During development of the Executive Workspace, it became evident that several independent components required access to the same assessment information.

Examples included:

* Assessment Wizard
* Progress Workspace
* Executive Workspace
* Enterprise Intelligence
* Decision Engine
* Reporting Components

Initially, each component attempted to obtain information independently.

This created several architectural challenges.

For example:

* Multiple components attempted to derive assessment state independently.
* Dashboard components recalculated information already generated elsewhere.
* Progress reporting became disconnected from assessment execution.
* Decision generation became difficult to synchronise with assessment completion.

Although individual modules functioned correctly, the platform itself lacked a unified assessment lifecycle.

## Runtime Orchestration Concept

To address this limitation, a Runtime Orchestration Layer is proposed.

The purpose of this layer is to coordinate the complete assessment lifecycle while maintaining a single authoritative assessment state.

Rather than allowing individual components to execute assessment activities independently, a dedicated orchestration service becomes responsible for coordinating:

* Assessment Initialisation
* Environment Validation
* Cryptographic Discovery
* Asset Classification
* Migration Readiness Analysis
* Governance Evaluation
* Decision Generation
* Executive Reporting

This transforms the platform from a collection of assessment modules into an integrated migration system.

## Key Insight

Building additional assessment capabilities does not automatically produce an integrated migration platform.

A governance-aware migration platform requires an orchestration mechanism capable of coordinating assessment activities throughout their entire lifecycle.

Runtime orchestration therefore represents an architectural capability rather than an additional assessment feature.

## Implication for PQC Migration

Future enterprise migration platforms are likely to require dedicated runtime coordination capable of managing assessment execution across multiple independent services.

Without runtime orchestration:

* assessment components become increasingly disconnected,
* execution order becomes difficult to maintain,
* assessment progress becomes difficult to explain,
* executive dashboards cannot accurately represent assessment state.

Runtime orchestration therefore becomes an enabling capability for governance-aware migration management.

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

Runtime Orchestration

↓

Migration Planning

↓

Executive Reporting

This further evolves the prototype from a cryptographic assessment tool into an enterprise migration platform capable of coordinating governance-aware migration activities.

## Potential Contribution

This observation suggests that Runtime Orchestration may represent an important architectural layer within enterprise post-quantum migration systems.

Rather than focusing exclusively on cryptographic analysis, future migration platforms may benefit from treating assessment execution itself as a managed lifecycle coordinated through a dedicated orchestration service.

Such an approach may improve assessment transparency, execution consistency, governance traceability, and future extensibility.

## Future Work

Future prototype development will investigate runtime orchestration through the introduction of a dedicated Assessment Service responsible for:

* Assessment lifecycle management
* Runtime state management
* Progress coordination
* Executive dashboard synchronisation
* Decision workflow integration
* Automatic report generation

Particular attention will be given to state management, explainable execution, event-driven assessment workflows, and support for future distributed assessment environments.
