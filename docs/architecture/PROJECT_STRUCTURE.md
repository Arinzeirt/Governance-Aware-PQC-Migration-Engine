# Enterprise Quantum Migration Platform (EQMP)

# Project Structure

---

## Document Identity

| Property | Value |
|----------|-------|
| Document | PROJECT_STRUCTURE.md |
| Role | Repository Structure Specification |
| Owner | EQMP Development |
| Audience | Developers, Researchers, Contributors |
| Scope | Project Organisation |
| Status | Active |
| Version | 1.0 |

---

# Purpose

This document defines how the Enterprise Quantum Migration Platform (EQMP) repository is organised.

Its purpose is to ensure that every file, directory and module has a clearly defined responsibility.

A well-structured repository enables maintainability, scalability and consistent development across the lifetime of the platform.

This document focuses on **where things belong**, while the platform architecture is defined in `ARCHITECTURE.md`.

---

# Repository Philosophy

EQMP follows a modular, enterprise-first repository architecture.

The repository is organised around responsibilities rather than technologies.

Each top-level directory owns a distinct responsibility and should remain independent wherever possible.

This separation enables the platform to evolve without creating unnecessary coupling between research, presentation, assessment and business logic.

---

# Repository Structure

```text
EQMP
│
├── app/
├── dashboard/
├── assets/
├── docs/
├── knowledge/
├── research-notes/
├── reports/
├── scans/
├── demo/
├── workspace/
├── archive/
└── backups/
```

---

# Directory Responsibilities

## app/

The application layer.

Contains the business logic that powers EQMP.

Examples include:

- Assessment Engine
- Risk Analysis
- Decision Services
- Reporting
- Inventory
- Roadmap Generation
- Recommendations
- Enterprise Scanning

No presentation logic should exist within this directory.

---

## dashboard/

The presentation layer.

Responsible for delivering the enterprise user experience.

Major responsibilities include:

- Landing Experience
- Enterprise Assessment
- Navigation
- Reporting Views
- Shared Components
- Design System
- Themes
- Layouts

The dashboard should never contain business rules or assessment logic.

---

## assets/

Contains all static resources used throughout the platform.

Examples include:

- Logos
- Illustrations
- Icons
- Research Graphics
- Images
- Branding Assets

---

## docs/

The official documentation of EQMP.

Documentation defines the platform's architecture, development approach, research direction and product vision.

The active documentation consists of:

- Architecture
- Project Structure
- Assessment Flow
- Development Blueprint
- Roadmap
- Research Framework
- Product Vision

---

## knowledge/

The shared enterprise knowledge base.

This directory stores reusable knowledge consumed throughout the platform.

Examples include:

- Governance Models
- Standards
- Industry Guidance
- PQC References
- Assessment Knowledge
- Regulatory Mapping

---

## research-notes/

The innovation engine of EQMP.

Research Notes transform academic research into practical platform capabilities.

Typical lifecycle:

Observation

↓

Research Question

↓

Literature Review

↓

Research Note

↓

Framework

↓

Assessment Methodology

↓

Platform Capability

↓

Enterprise Feature

---

## reports/

Stores generated reports and report templates.

Examples include:

- Executive Reports
- Technical Reports
- Compliance Reports
- Migration Roadmaps

---

## scans/

Stores assessment outputs and scan artefacts generated during enterprise assessments.

---

## demo/

Contains demonstration assets and proof-of-concept implementations used for presentations, workshops and stakeholder engagement.

---

## workspace/

A temporary working area for experiments, prototypes and active development.

Content in this directory should not be considered production-ready.

---

## archive/

Historical project material retained for reference.

Archived content does not form part of the active platform architecture.

---

## backups/

Backup copies created during major development milestones.

Backups exist for recovery purposes only.

---

# Engineering Principles

The repository follows these principles:

- One Responsibility Per Directory
- Modular Design
- Separation of Concerns
- Research Before Implementation
- Documentation Before Major Architecture Changes
- Enterprise Maintainability
- Long-Term Scalability

---

# Relationship to Other Documentation

This document defines **where** platform capabilities belong.

It should be read alongside:

- `ARCHITECTURE.md` — Defines the platform architecture.
- `ASSESSMENT_FLOW.md` — Defines the enterprise assessment methodology.
- `DEVELOPMENT_BLUEPRINT.md` — Defines implementation priorities.
- `ROADMAP.md` — Defines future platform evolution.
- `RESEARCH_FRAMEWORK.md` — Defines how research becomes capability.
- `PRODUCT_VISION.md` — Defines the commercial direction of EQMP.

Together, these documents form the official documentation of the Enterprise Quantum Migration Platform.
