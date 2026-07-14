# Enterprise Quantum Migration Platform (EQMP)

Version: RC1
Status: Active Development

---

# Purpose

This document defines the official software architecture for the Enterprise Quantum Migration Platform (EQMP).

The objective is to ensure every future feature follows a consistent structure and to prevent architectural drift as the platform grows.

---

# High-Level Architecture

Application

│

├── Controllers

├── Views

├── Components

├── Services (Future)

├── Engine (Future)

└── Documentation

---

# Directory Structure

dashboard/

controllers/

views/

components/

layouts/

assets/

design_system.py

app.py

---

# Controllers

Purpose

Route user navigation.

Controllers never render UI directly.

Responsibilities

• Route pages

• Handle navigation

• Select views

Example

controllers/navigation.py

---

# Views

Purpose

Compose complete application pages.

Views orchestrate components.

Views do not contain business logic.

Example

views/dashboard.py

views/assessment.py

views/reports.py

views/inventory.py

---

# Components

Purpose

Reusable interface elements.

Examples

Executive Summary

Executive KPIs

Quick Actions

Enterprise Findings

Migration Roadmap

Footer

Enterprise Header

Top Navigation

---

# Layouts

Purpose

Application shell.

Examples

workspace.py

shell.py

---

# Future Services

Purpose

Business logic.

Examples

Inventory Service

Governance Service

Reporting Service

Migration Service

Repository Service

---

# Future Engine

Purpose

Core EQMP intelligence.

Examples

Cryptographic Discovery Engine

Governance Decision Engine

Migration Orchestrator

Risk Engine

Repository Scanner

---

# Design Principles

1. Controllers never render UI.

2. Views compose pages.

3. Components are reusable.

4. Business logic belongs in Services.

5. Scanning belongs in Engine.

6. Styling belongs in the Design System.

7. Documentation evolves with the platform.

---

# Active Views

Dashboard

Assessment

Inventory

Repository Explorer

Reports

Research Centre

Migration

About

---

# Development Workflow

Review

↓

Architecture Decision

↓

Implementation

↓

Compile

↓

Run

↓

Review

↓

Freeze

---

# Long-Term Vision

EQMP evolves into an enterprise governance platform for post-quantum migration.

The dashboard becomes one workspace among many while all cryptographic intelligence is driven by the EQMP Engine and the Enterprise Quantum Migration Governance Framework (EQMGF).

