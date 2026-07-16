# Research Notes Series 010

# From Readiness Scores to Governance-Driven Migration Roadmaps

---

## Building on Research Note 009

Research Note 009 introduced the concept of a **Post-Quantum Migration Readiness Score (PQMRS)** as a governance-aware measure of enterprise preparedness.

The readiness score provides executive visibility into an organization's migration capability by combining cryptographic discovery, governance maturity, regulatory exposure, business impact and migration status into a single measurable indicator.

However, measuring readiness introduces another practical challenge.

Once an organization understands its readiness posture, a new question immediately follows:

> **What should be migrated first?**

Knowing that an organization is only 62% ready is valuable, but it does not explain where migration should begin or how the migration should be executed.

This naturally leads to the next stage of the research.

---

# Research Observation

Current post-quantum migration guidance frequently recommends replacing vulnerable cryptographic algorithms according to technical severity.

In practice, enterprise migration rarely occurs this way.

Large organizations migrate business capabilities rather than individual algorithms.

Critical payment systems, identity platforms, customer services and regulatory systems often receive priority because of their operational importance, even when their cryptographic risk is similar to less critical assets.

This demonstrates that migration sequencing is fundamentally a governance decision rather than a purely technical activity.

---

# Research Problem

Existing migration approaches provide inventories and readiness assessments but rarely translate these outputs into an actionable migration roadmap.

As a result, organizations often struggle to answer important governance questions such as:

- Which business services should migrate first?
- Which assets can safely be postponed?
- How should migration phases be organized?
- Which systems introduce the greatest operational risk?
- How should migration budgets be prioritized?

Without an intelligent roadmap, migration planning becomes subjective and inconsistent.

---

# Proposed Contribution

This research proposes a **Governance-Driven Migration Roadmap Model (GDMRM).**

Instead of ranking cryptographic assets solely by algorithmic vulnerability, the roadmap prioritizes migration using multiple governance dimensions, including:

- Enterprise readiness
- Business criticality
- Regulatory obligations
- Operational dependencies
- Customer impact
- Migration complexity
- Governance ownership
- Compliance exposure

These dimensions enable migration to be organized into structured implementation waves rather than isolated technical projects.

---

# Practical Validation Through EQMP

The proposed roadmap model is currently being implemented within the **Enterprise Quantum Migration Platform (EQMP).**

The platform now generates governance-aware migration planning using:

- Migration priority
- Recommended migration deadlines
- Migration phases
- Asset ownership
- Governance responsibility
- Business criticality
- Compliance recommendations
- Executive readiness indicators

Rather than producing static assessment reports, EQMP transforms assessment results into practical migration guidance that organizations can use to plan implementation activities.

This implementation provides an experimental environment for evaluating governance-driven migration sequencing.

---

# Research Contribution

The primary contribution of this work is the transition from assessment to execution.

Instead of treating migration planning as a manual governance exercise, this research proposes that migration roadmaps can be systematically generated using enterprise governance intelligence.

This represents a shift from answering:

> "Which algorithms are vulnerable?"

towards answering:

> **"Which business capabilities should migrate first, and why?"**

---

# Key Insight

> **Assessment identifies readiness. Governance transforms readiness into execution.**

---

# Looking Ahead

Research Note Series 011 will investigate why **business criticality—not cryptographic severity alone—should become the primary driver of enterprise post-quantum migration priorities.**

---

**Arinze Research Notes Series 010**

*"The success of post-quantum migration will not be determined by discovering vulnerable algorithms, but by governing the order in which business-critical systems evolve."*

