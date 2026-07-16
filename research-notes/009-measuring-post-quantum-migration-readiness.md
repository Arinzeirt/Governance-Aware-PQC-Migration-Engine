# Research Notes Series 009

# Measuring What Matters: Why Post-Quantum Migration Needs a Readiness Score

---

## Building on Research Note 008

In **Research Note 008**, I argued that post-quantum migration decisions should be **explainable rather than opaque**. An explainable decision pipeline enables organizations to justify why one asset should be migrated before another by considering business context, governance, technical dependencies, and regulatory obligations instead of relying solely on cryptographic discovery.

While explainability improves confidence in migration decisions, it also exposes another important question:

> **How do organizations know whether they are actually ready to begin post-quantum migration?**

Decision support can recommend what to do next, but without a measurable indicator of organizational preparedness, executives still lack a way to understand their overall migration posture or track improvement over time.

This naturally leads to the next stage of the research.

---

# Research Observation

Most existing post-quantum migration initiatives focus on identifying cryptographic assets, vulnerable algorithms, or migration priorities. Although these activities are essential, they primarily answer operational questions such as:

- Where is cryptography used?
- Which algorithms require replacement?
- Which systems should be prioritized?

These are important technical outputs, but they do not answer the strategic question that executive leadership is more likely to ask:

> **How ready is our organization for post-quantum migration?**

Discovery provides visibility into the current environment, whereas readiness reflects an organization's overall capability to execute and sustain a successful migration programme.

---

# Research Problem

Current enterprise post-quantum initiatives provide inventories, risk reports and migration priorities, but they rarely provide a measurable indicator of organizational preparedness.

Without a governance-aware readiness metric, executive leadership cannot consistently answer:

- Are we ready to begin migration?
- Which business units are least prepared?
- Are we improving over time?
- Where should investment be prioritized?

The absence of a standardized readiness assessment creates a disconnect between technical discovery and executive decision making.

---

# Proposed Contribution

This work introduces the concept of a **Post-Quantum Migration Readiness Score (PQMRS).**

Rather than functioning as another technical metric, the readiness score translates cryptographic evidence into governance intelligence by evaluating multiple enterprise dimensions, including:

- Cryptographic visibility
- Asset classification maturity
- Business criticality
- Governance ownership
- Regulatory alignment
- Migration planning status
- Operational dependencies
- Migration priority

The resulting score provides executives with a measurable view of enterprise preparedness while supporting governance-led decision making.

---

# Practical Validation Through EQMP

The proposed readiness model is currently being implemented and evaluated through the **Enterprise Quantum Migration Platform (EQMP).**

The latest implementation extends beyond cryptographic discovery by incorporating governance-aware readiness assessment using:

- Asset criticality
- Business impact
- Regulatory exposure
- Migration priority
- Governance ownership
- Compliance recommendations
- Migration status
- Organizational readiness indicators

Rather than simply reporting vulnerable cryptographic assets, EQMP now generates an executive readiness assessment that supports governance reporting, migration planning and strategic decision making.

This implementation serves as an experimental validation environment for evaluating governance-aware readiness scoring in enterprise post-quantum migration.

---

# Research Contribution

The contribution of this work is not merely the introduction of another assessment metric.

It proposes that **Post-Quantum Migration Readiness** should become a measurable governance capability that integrates technical evidence, governance maturity, business priorities and regulatory obligations into a unified decision-support framework.

This shifts enterprise conversations away from asking:

> "How many vulnerable algorithms do we have?"

towards the more strategic question:

> **"How prepared are we to successfully execute and govern post-quantum migration?"**

---

# Key Insight

> **Discovery identifies what exists. Explainability justifies decisions. Readiness measures an organization's ability to execute those decisions successfully.**

---

# Looking Ahead

Research Note Series 010 will explore how enterprise readiness scores can be transformed into intelligent migration roadmaps that prioritize business-critical systems, governance objectives and regulatory deadlines through phased migration planning.

---

**Arinze Research Notes Series 009**

*"Enterprise post-quantum readiness should not be assumed—it should be measured, governed, and continuously improved."*

