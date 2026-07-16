# Research Notes Series 011

# Why Business Criticality Should Drive Post-Quantum Migration

---

## Building on Research Note 010

Research Note 010 introduced the concept of a **Governance-Driven Migration Roadmap Model (GDMRM)**, demonstrating that enterprise migration should be planned through structured governance rather than isolated technical activities.

The proposed roadmap transformed enterprise readiness into phased migration plans by considering governance responsibilities, migration ownership, operational dependencies and regulatory obligations.

However, another important question emerges.

When several systems appear equally vulnerable, **which one should migrate first?**

Traditional migration approaches often answer this question using cryptographic severity alone.

This research argues that enterprise migration requires a different perspective.

---

# Research Observation

Current post-quantum migration guidance generally prioritizes systems based on technical characteristics such as:

- Vulnerable algorithms
- Cryptographic key sizes
- Legacy implementations
- Exposure to quantum attacks

Although technically valid, these criteria rarely reflect how organizations actually make investment and operational decisions.

In practice, executives prioritize:

- Revenue-generating services
- Payment infrastructure
- Customer-facing platforms
- Regulatory systems
- Critical operational services

The systems that matter most to the business are not always the systems with the greatest cryptographic exposure.

---

# Research Problem

Many migration frameworks implicitly assume that cryptographic risk should determine migration priority.

This assumption creates several governance challenges.

Organizations may:

- Allocate resources to technically vulnerable but operationally insignificant systems.
- Delay migration of business-critical services because their technical scores appear lower.
- Ignore regulatory obligations attached to high-value business functions.
- Produce migration plans that satisfy engineering teams but fail executive governance objectives.

As a result, technical optimization does not necessarily produce enterprise resilience.

---

# Proposed Contribution

This research proposes that **Business Criticality** should become the primary decision variable for enterprise post-quantum migration.

Rather than asking:

> "Which algorithm is most vulnerable?"

Organizations should first ask:

> **"Which business capability creates the greatest operational, financial and regulatory impact if compromised?"**

Business criticality should be evaluated using governance-aware indicators such as:

- Revenue dependency
- Customer impact
- Service availability
- Regulatory exposure
- Operational resilience
- Mission-critical functions
- Recovery requirements
- Executive ownership

Cryptographic vulnerability remains important, but it becomes one factor within a broader governance decision framework.

---

# Practical Validation Through EQMP

The proposed model is currently being implemented within the **Enterprise Quantum Migration Platform (EQMP).**

The platform evaluates business criticality using enterprise governance information including:

- Business zone
- Asset criticality
- Throughput classification
- Latency sensitivity
- Governance ownership
- Migration priority
- Regulatory exposure
- Compliance recommendations

These indicators influence migration sequencing, ensuring that business-critical systems receive higher priority even when multiple assets exhibit similar cryptographic risk.

This implementation provides an experimental environment for validating governance-aware migration prioritization.

---

# Research Contribution

The contribution of this work is a shift from **technology-first migration** to **business-first migration.**

Instead of allowing cryptographic algorithms alone to determine migration priorities, this research proposes that enterprise governance should integrate technical risk with business value.

This changes the primary migration question from:

> "Which cryptographic implementation is weakest?"

to

> **"Which business capability cannot afford to fail during the post-quantum transition?"**

---

# Key Insight

> **Organizations do not migrate algorithms—they migrate business operations protected by cryptography.**

---

# Looking Ahead

Research Note Series 012 will examine how **regulatory obligations and compliance intelligence should actively influence enterprise post-quantum migration decisions rather than serving only as audit evidence.**

---

**Arinze Research Notes Series 011**

*"The future of post-quantum migration will be determined not by which algorithms are weakest, but by which business capabilities matter most."*

