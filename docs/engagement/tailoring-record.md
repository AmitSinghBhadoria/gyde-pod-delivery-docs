---
sidebar_position: 11
title: Engagement Tailoring Record
---

# Engagement Tailoring Record -- AI Support Copilot

**Engagement**: AI Support Copilot Pilot
**Owner**: Amit (POD Lead) + Shivani (PM)
**Version**: 1.0
**Date**: 2026-05-01
**Framework ref**: Doc 01, Section 5.1

> The Gyde POD Operation Framework is designed to be tailored per engagement. This document records every deviation from the default framework practices, with rationale. **Non-negotiable items (Doc 01, Section 5.1) cannot be tailored away** without Engineering Leadership approval.

---

## 1. Non-Negotiable Compliance

All five non-negotiables are upheld in this engagement. None have been waived.

| # | Non-Negotiable | Status | How Fulfilled |
|---|---|---|---|
| 1 | Threat modeling and secrets management | **Compliant** | Threat Model (#10) produced; secrets via env vars / GCP Secret Manager |
| 2 | Evaluation before production | **Compliant** | Evaluation Plan (#6), Eval Harness (#20), Golden Dataset (#21), 1,000-question synthetic eval |
| 3 | Versioned data and prompts | **Compliant** | All prompts, datasets, configs in Git; every change tracked |
| 4 | Audit trail for AI decisions | **Compliant** | Every copilot decision logged to MongoDB audit_log with full pipeline output |
| 5 | Incident response readiness | **Compliant** | Runbooks included in Knowledge Transfer Package (#34) |

---

## 2. Tailoring Decisions

### 2.1 Engagement Lifecycle (Doc 03, Section 2)

| Default | Tailored To | Rationale | Impact |
|---|---|---|---|
| 5 phases: Discovery → Sprint Zero → Build → Hardening → Handover | 3 phases: Discovery → Sprint 1 (Build) → Sprint 2 (Build + Hardening + Handover) | 16-day pilot timeline; Sprint Zero activities absorbed into Discovery and Sprint 1 Day 1; Hardening and Handover compressed into Sprint 2 | Higher risk; mitigated by pre-approved scope cuts in Risk Register |
| M0 through M6 milestones | M0 through M3 only | Pilot scope; M4-M6 (production deployment, stable operation, engagement close) are out of scope | Client understands pilot != production |
| Discovery: 1-3 weeks | Discovery: 1 day (May 1) | Internal simulation; team already aligned; Discovery call answers captured same day | Acceptable for simulation; real client engagement would take longer |

### 2.2 Sprint Cadence (Doc 04, Section 2)

| Default | Tailored To | Rationale | Impact |
|---|---|---|---|
| 2-week (10-day) sprints | Sprint 1: 10 days, Sprint 2: 6 days | Hard deadline May 16; Sprint 2 is compressed but covers only hardening + handover scope | Sprint 2 has less buffer; contingency plan addresses this |
| Backlog refinement on Day 9 | Sprint 1 only; Sprint 2 too short for separate refinement | Sprint 2 backlog is fully planned during Discovery; no refinement ceremony needed | Acceptable -- Sprint 2 scope is fixed |
| WIP limit: 1 in-progress story per member | Relaxed to 2 for Sprint 1 | Parallel tracks (infra + data + pipeline) require some members to context-switch | Monitor in retro; revert if quality suffers |

### 2.3 QA Practices (Doc 04, Section 6)

| Default | Tailored To | Rationale | Impact |
|---|---|---|---|
| QA buddy assigned per story; rotates each sprint | QA buddy assigned per story; limited rotation due to 2-sprint engagement | Only 2 sprints; full rotation not achievable; buddy assignments prioritize domain knowledge | Acceptable for pilot; some members won't QA-buddy every part of the system |
| Adversarial eval run every 2 sprints | Run once in Sprint 2 | Only 2 sprints total; adversarial set created and run in Sprint 2 | Compliant -- adversarial eval happens before delivery |

### 2.4 Security (Doc 14)

| Default | Tailored To | Rationale | Impact |
|---|---|---|---|
| Full authentication and authorization | No authentication in pilot | Internal pilot with simulated data; single-user access | Production must add JWT auth / SSO; documented in productionization note |
| Data processing agreements for LLM providers | Deferred to production | Pilot uses simulated data; no real customer PII | Production must evaluate DPA with Google or switch to on-prem LLM |
| Network-level security review | Deferred to production | Pilot runs on internal GCP VM; no external traffic in pilot | Production requires firewall rules, VPN, TLS |

### 2.5 Documentation (Doc 19)

| Default | Tailored To | Rationale | Impact |
|---|---|---|---|
| Separate Architecture Sketch + final Architecture Document | Architecture Sketch (#5) serves as architecture doc; updated to final during Sprint 2 (#31) | Pilot is short; maintaining two documents for same content is overhead | Single document evolves from sketch to final |
| Monthly steering committee pack | Not applicable | Engagement is 16 days; no monthly cadence exists | Replaced by weekly status email + sprint demos |

### 2.6 Operations (Doc 18)

| Default | Tailored To | Rationale | Impact |
|---|---|---|---|
| Monitoring dashboards | Not built in pilot | No production traffic; monitoring adds overhead without value | Documented as production requirement in productionization note |
| On-call rotation | Not applicable | No production deployment; pilot is demo-only | Documented in KT package as production requirement |
| Rollback plan | Not applicable | No production deployment | Documented in KT package |

### 2.7 MLOps (Doc 12)

| Default | Tailored To | Rationale | Impact |
|---|---|---|---|
| Model version registry | Prompt versions tracked in Git | No model training / fine-tuning; RAG architecture uses foundation model as-is | Adequate for pilot; production may need formal registry if fine-tuning is added |
| Drift detection | Not applicable | No production traffic to detect drift against | Documented as production requirement |
| A/B testing framework | Not applicable | Single pipeline variant; no traffic to split | Could be useful in production for prompt iteration |

---

## 3. Items Explicitly NOT Tailored

These framework practices are followed as-is, without modification:

| Practice | Framework Ref | Why Kept |
|---|---|---|
| Threat modeling | Doc 14 | Non-negotiable; initial model produced at Discovery, full review at Sprint 2 |
| Evaluation harness with golden dataset | Doc 17 | Non-negotiable; eval gates every release |
| Versioned prompts and data | Doc 10 | Non-negotiable; all prompts in Git as template files |
| Audit logging | Doc 01 | Non-negotiable; every copilot decision logged |
| Sprint demos to client | Doc 04 | Essential for client alignment; both demos happening |
| Sprint retro | Doc 04 | Essential for team improvement; both retros happening |
| Risk register (living) | Doc 03 | Updated weekly; visible to client |
| Definition of Done | Doc 04 | Full DoD applied to every story including QA buddy verification |
| Change request process | Doc 03 | Active for any scope/schedule changes |
| Decision logging (ADRs) | Doc 19 | Key decisions documented as they occur |

---

## 4. Approval

| Role | Name | Approval | Date |
|---|---|---|---|
| POD Lead | Amit | __________ | __________ |
| Implementation Manager | Shivani | __________ | __________ |

**Note**: No Engineering Leadership approval required because all five non-negotiables are upheld. Tailoring decisions affect only engagement-specific practices, not framework principles.

---

## Change Log

| Date | Change | By |
|---|---|---|
| 2026-05-01 | Initial tailoring record created | Amit + Shivani |

---

*This record ensures transparency about what we changed and why. Future engagements can reference this as a precedent for similar pilot-scoped tailoring.*
