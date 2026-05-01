---
sidebar_position: 1
title: Deliverables Checklist
---

# POD Engagement Deliverables Checklist

**Purpose**: Master list of all artifacts and deliverables required across a POD engagement lifecycle. Use this as a tracking checklist for delivery and as a template for future engagements.

**Framework references**: Doc 01 (Charter), Doc 03 (Planning & Estimation), Doc 04 (Agile Delivery), Doc 05 (Client Communication), Doc 06 (SDLC), Doc 14 (Security), Doc 17 (QA & Testing), Doc 19 (Documentation)

---

## How to Use This Document

- **For the current engagement**: Track status of each artifact as the engagement progresses
- **For new engagements**: Copy this checklist, tailor the owner and timeline columns, mark items as Not Applicable where the framework allows tailoring
- **Non-negotiable items** are marked with **(NN)** -- these cannot be tailored away per Doc 01, Section 5.1

### Status Legend

| Status | Meaning |
|---|---|
| `---` | Not started |
| `In Progress` | Being drafted |
| `In Review` | Draft complete, under review |
| `Done` | Signed off / delivered |
| `N/A` | Not applicable for this engagement (document why in Tailoring Record) |

---

## Phase 0: Discovery

**Goal**: Shape the engagement, validate feasibility, produce the Discovery Output Pack (Doc 03, Section 3.4)

| # | Artifact | Owner | Framework Ref | Status |
|---|---|---|---|---|
| 1 | Discovery Call Answers | POD Lead | -- | Done |
| 2 | Use Case Canvas | POD Lead + PM | Doc 03, Sec 3.4 | Done |
| 3 | Data Feasibility Report | Data Engineer | Doc 03, Sec 3.4 | Done |
| 4 | POD Charter | PM + POD Lead | Doc 01, Sec 6 | In Review |
| 5 | Architecture Sketch | POD Lead | Doc 03, Sec 3.4 | Done |
| 6 | Evaluation Plan | POD Lead + QA | Doc 03, Sec 3.4 | Done |
| 7 | Risk Register (initial) | PM | Doc 03, Sec 6 | Done |
| 8 | Engagement Plan | PM | Doc 03, Sec 7 | Done |
| 9 | Sprint Plan | PM + POD Lead | Doc 04 | Done |
| 10 | Threat Model (initial) **(NN)** | Governance Engineer | Doc 14 | --- |
| 11 | Engagement Tailoring Record | POD Lead + PM | Doc 01, Sec 5.1 | --- |

**Discovery Exit Gate** (Doc 03, Section 3.5):
- [ ] All 7 Discovery Output Pack artifacts present and internally reviewed
- [ ] Client sponsor sign-off on success criteria and Evaluation Plan thresholds
- [ ] Architecture Sketch reviewed (no blocking concerns)
- [ ] Threat model in flight (initial threat surface identified)
- [ ] Sprint Zero / Sprint 1 readiness confirmed

---

## Phase 1: Sprint 1 -- Walking Skeleton + Eval Harness

**Goal**: End-to-end working slice (M1) and operational evaluation harness (M2)

### Engineering Deliverables

| # | Artifact | Owner | Framework Ref | Status |
|---|---|---|---|---|
| 12 | ADRs (Architecture Decision Records) | POD Lead | Doc 19 | --- |
| 13 | Data ingestion pipeline | Data Engineer | Doc 06 | --- |
| 14 | Vector store + retrieval module | Data Engineer + AI Engineer | Doc 06 | --- |
| 15 | Classification module | AI Engineer | Doc 06 | --- |
| 16 | Action recommendation module | AI Engineer | Doc 06 | --- |
| 17 | Response drafting module | AI Engineer | Doc 06 | --- |
| 18 | Confidence scoring | AI Engineer | Doc 06 | --- |
| 19 | UI (extension / sidebar / web app) | POD Lead | Doc 06 | --- |
| 20 | Eval harness **(NN)** | QA + POD Lead | Doc 17 | --- |
| 21 | Golden dataset (initial) **(NN)** | QA | Doc 17 | --- |

### Process Deliverables

| # | Artifact | Owner | Framework Ref | Status |
|---|---|---|---|---|
| 22 | Sprint 1 status report | PM | Doc 05 | --- |
| 23 | Sprint 1 demo | POD Lead + PM | Doc 04, Sec 8 | --- |

### Milestone Gates

**M1 -- Walking Skeleton**:
- [ ] One input → one classification → one retrieval → one output, deployed to dev
- [ ] Architecture ADRs documented

**M2 -- Eval Harness Operational**:
- [ ] Golden dataset committed (minimum 20 cases)
- [ ] Automated scoring running
- [ ] Baseline metrics published against Evaluation Plan thresholds

---

## Phase 2: Sprint 2 -- MVP + Hardening + Handover

**Goal**: Feature-complete MVP (M3), all eval gates passing, security reviewed, knowledge transfer ready

### Engineering Deliverables

| # | Artifact | Owner | Framework Ref | Status |
|---|---|---|---|---|
| 24 | Feedback loop (agent rates/edits, system learns) | AI Engineer | Doc 06 | --- |
| 25 | Guardrails (profanity, misuse prevention) | AI Engineer + Governance | Doc 14 | --- |
| 26 | UI polish + confidence indicators | POD Lead | Doc 06 | --- |
| 27 | Synthetic eval set (1000 questions) | QA + AI Engineer | Doc 17 | --- |

### Evaluation & Quality Deliverables

| # | Artifact | Owner | Framework Ref | Status |
|---|---|---|---|---|
| 28 | Final eval results **(NN)** | QA | Doc 17 | --- |
| 29 | Sample outputs (10-12 across categories) | QA | Doc 03 | --- |
| 30 | Security review sign-off **(NN)** | Governance Engineer | Doc 14 | --- |

### Documentation Deliverables

| # | Artifact | Owner | Framework Ref | Status |
|---|---|---|---|---|
| 31 | Architecture document (final) | POD Lead | Doc 19 | --- |
| 32 | Productionization note | POD Lead | Client brief | --- |
| 33 | Model card | AI Engineer + POD Lead | Doc 19 | --- |
| 34 | Knowledge transfer package | POD Lead + PM | Doc 19 | --- |

### Process Deliverables

| # | Artifact | Owner | Framework Ref | Status |
|---|---|---|---|---|
| 35 | Sprint 2 status report | PM | Doc 05 | --- |
| 36 | Final demo + walkthrough | POD Lead + PM | Doc 04 | --- |
| 37 | Engagement summary | POD Lead + PM | Doc 19 | --- |

### Milestone Gates

**M3 -- MVP Feature-Complete**:
- [ ] All MVP scope implemented and integrated
- [ ] Eval metrics at or above target thresholds
- [ ] Security review completed, no blocking findings
- [ ] Adversarial eval cases run

**Delivery Gate**:
- [ ] All documentation delivered
- [ ] Knowledge transfer complete
- [ ] Client walkthrough conducted
- [ ] Codebase ready for handover

---

## Recurring Artifacts (Every Sprint)

These are produced every sprint, not just once.

| Artifact | Owner | Cadence | Framework Ref |
|---|---|---|---|
| Weekly status email | PM | Weekly | Doc 05 |
| Weekly call (Google Meet) | PM + POD Lead | Weekly | Doc 05 |
| Sprint demo | POD Lead + PM | Per sprint | Doc 04, Sec 8 |
| Eval results delta | QA | Per sprint | Doc 17 |
| Updated risk register | PM | Per sprint | Doc 03 |
| Decision log entries | POD Lead + PM | As needed | Doc 19 |
| Updated ADRs | POD Lead | As needed | Doc 19 |
| Sprint retro outcomes | POD Lead | Per sprint | Doc 04 |

---

## Non-Negotiable Artifacts (Never Tailored Away)

Per Doc 01, Section 5.1 -- these are required in every engagement regardless of size, timeline, or client preferences:

| # | Non-Negotiable | Artifacts That Fulfill It |
|---|---|---|
| 1 | Threat modeling and secrets management | Threat Model (#10), Security Review (#30) |
| 2 | Evaluation before production | Evaluation Plan (#6), Eval Harness (#20), Golden Dataset (#21), Final Eval Results (#28) |
| 3 | Versioned data and prompts | All prompts, data, and configs in version control |
| 4 | Audit trail for AI decisions | Logging in the application, Decision Log |
| 5 | Incident response readiness | Runbooks (in Knowledge Transfer Package #34) |

---

## Ownership Summary by Role

### POD Lead (Amit)
Primary: #1, #5, #12, #19, #26, #31, #32
Contributing: #2, #4, #6, #9, #23, #33, #34, #36, #37

### AI Engineer (Atharva)
Primary: #14, #15, #16, #17, #18, #24, #25
Contributing: #27, #33

### Data Engineer (Nancy)
Primary: #3, #13
Contributing: #14

### QA (Nishka)
Primary: #20, #21, #27, #28, #29
Contributing: #6

### Governance Engineer (Shubham)
Primary: #10, #25, #30
Contributing: #6

### Implementation Manager (Shivani)
Primary: #4, #7, #8, #9, #11, #22, #35
Contributing: #2, #23, #34, #36, #37

---

## Adapting This Checklist for New Engagements

When starting a new client engagement:

1. **Copy this document** as the starting point
2. **Fill in the Owner column** with actual team member names
3. **Review each item** against the engagement scope:
   - If the engagement is shorter (e.g., 2-week spike), mark non-critical items as N/A
   - If longer (e.g., 12-week build), add items from the extended framework inventory (Doc 12: MLOps, Doc 18: Operations)
4. **Never mark Non-Negotiable (NN) items as N/A** -- these require Engineering Leadership approval to waive (Doc 01, Section 5.1)
5. **Record all tailoring decisions** in the Engagement Tailoring Record (#11)
6. **Add engagement-specific deliverables** requested by the client that aren't in this template

### Common Additions by Engagement Type

| Engagement Type | Typical Additional Artifacts |
|---|---|
| Production deployment | Runbooks, on-call rotation, rollback plan, monitoring dashboards, cost projection |
| Regulated industry | Compliance mapping, responsible AI checklist, governance log, audit trail design |
| Multi-team | Cross-team interface contracts, shared API specs, integration test suite |
| Data-heavy | Data lineage docs, PII handling policy, data quality reports, refresh schedules |
| Long-running (12+ weeks) | Monthly steering committee pack, model version registry, drift detection setup |
