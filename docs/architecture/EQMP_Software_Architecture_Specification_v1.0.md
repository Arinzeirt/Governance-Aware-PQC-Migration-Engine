# EQMP Software Architecture Specification v1.0

**Platform:** EQMP – Enet Quantum Migration Platform

**Organisation:** Enet Technologies

**Status:** Technology Preview

**Version:** 1.0

---

# Purpose

The EQMP Software Architecture Specification defines the engineering principles, architectural layers, runtime lifecycle, module responsibilities, and design standards governing the development of the Enet Quantum Migration Platform.

This document serves as the primary architectural reference for the platform.

---

# Vision

EQMP is a governance-aware platform for enterprise post-quantum cryptographic migration.

The platform integrates:

* Cryptographic Discovery
* Asset Inventory
* Governance Assessment
* Migration Readiness
* Executive Decision Support
* Reporting

within one unified assessment lifecycle.

---

# Architectural Principles

## Principle 1

Single Source of Truth

AssessmentService owns all runtime state.

No UI component maintains independent assessment state.

---

## Principle 2

Presentation Layer

Responsible only for displaying information.

No business logic.

---

## Principle 3

Business Services

Responsible for implementing technical capabilities.

Examples include:

* Scanner
* Analytics
* Decision Engine
* Reporting Engine

Business services remain independent of the user interface.

---

## Principle 4

Layer Separation

Presentation Layer

↓

Runtime Layer

↓

Business Services

↓

Persistence Layer

---

# Runtime Lifecycle

Assessment Wizard

↓

AssessmentService.begin()

↓

Environment Validation

↓

Cryptographic Discovery

↓

Asset Classification

↓

Migration Readiness

↓

Governance Analysis

↓

Executive Decision

↓

Executive Workspace

↓

Reports

---

# Runtime State

AssessmentService owns:

* running
* progress
* current stage
* logs
* inventory
* analytics
* decision
* completion status

---

# Future Direction

Version 1.0

* Live assessment execution
* Runtime orchestration
* Executive Workspace
* Reporting

Version 2.0

* Multi-agent scanning
* Distributed assessment
* API integration
* Enterprise deployment

Version 3.0

* AI-assisted migration planning
* Autonomous governance recommendations
* Predictive migration optimisation

---

# Guiding Principle

Every feature introduced into EQMP shall strengthen transparency, explainability, governance awareness, and architectural modularity.
