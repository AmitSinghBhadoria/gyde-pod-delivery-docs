---
sidebar_position: 3
title: Data Feasibility Report
---

# Data Feasibility Report

**Engagement**: AI Support Copilot Pilot
**Owner**: Nancy (Data Engineer)
**Reviewed by**: Amit (POD Lead)
**Version**: 1.0
**Date**: 2026-04-30
**Framework ref**: Doc 03, Section 3.4
**Data source**: `ai_support_copilot_poc_dataset.xlsx`

---

## 1. Executive Summary

**Overall assessment: Feasible for POC, with known limitations.**

The dataset is structurally clean, has consistent naming conventions, valid cross-references between sheets, and covers all four copilot capabilities (classify, retrieve, recommend, draft). However, it has low diversity (11 unique ticket scenarios across 36 records), one category gap (Reporting), and deterministic priority mapping that will inflate accuracy. Three targeted fixes (~30 minutes of effort) would significantly strengthen the dataset.

---

## 2. Dataset Inventory

| Sheet | Records | Columns | Purpose |
|---|---|---|---|
| Tickets_Historical | 36 | 15 | Past resolved tickets for building and testing |
| KB_Articles | 12 | 6 | Knowledge base articles with content and keywords |
| Escalation_Rules | 5 | 5 | Rules mapping conditions to escalation teams |
| Evaluation_Set | 12 | 8 | Held-out blind test set (do NOT use for training) |

---

## 3. Completeness Analysis

### Tickets_Historical (36 records, 15 columns)

| Column | Type | Completeness | Notes |
|---|---|---|---|
| ticket_id | String | 100% | TKT-1001 to TKT-1036, unique |
| date_created | Date | 100% | Range: 2024-11-01 to 2025-02-05 |
| customer_company | String | 100% | 6 companies represented |
| agent_name | String | 100% | 3 agents: Asha, Kiran, Meera |
| channel | String | 100% | Email (12), Chat (12), Portal (12) -- evenly distributed |
| subject | String | 100% | Short ticket summaries |
| description | String | 100% | Ticket body text |
| category | String | 100% | 7 categories (see distribution below) |
| priority | String | 100% | 4 levels: Critical, High, Medium, Low |
| sentiment | String | 100% | 3 values: Frustrated, Neutral, Satisfied |
| sla_target_hours | Number | 100% | 12, 24, 48, or 72 hours |
| source_kb_id | String | **92%** | **3 nulls** (TKT-1006, TKT-1031, TKT-1035) |
| action_taken | String | 100% | Reply, Ask for more info, Escalate |
| escalation_team | String | 100%* | Null where action != Escalate (correct) |
| resolution_summary | String | 100% | Free-text resolution notes |

### KB_Articles (12 records, 6 columns)

| Column | Type | Completeness | Notes |
|---|---|---|---|
| kb_id | String | 100% | KB-001 to KB-012, unique |
| title | String | 100% | Article titles |
| category | String | 100% | Maps to ticket categories |
| content | String | 100% | Article body text |
| keywords | String | 100% | Comma-separated keywords |
| agent_notes | String | 100% | Internal agent guidance |

### Escalation_Rules (5 records, 5 columns)

All columns 100% complete: rule_id, condition, escalation_team, required_context, sla_hours.

### Evaluation_Set (12 records, 8 columns)

All columns 100% complete: eval_id, ticket_subject, ticket_description, expected_category, expected_priority, expected_action, expected_kb_id, evaluation_notes.

---

## 4. Distribution Analysis

### Ticket Categories

| Category | Tickets | % | KB Articles | Eval Cases |
|---|---|---|---|---|
| Authentication | 6 | 17% | 2 (KB-001, KB-002) | 2 |
| Billing | 6 | 17% | 2 (KB-003, KB-004) | 2 |
| Data Import | 6 | 17% | 2 (KB-005, KB-006) | 2 |
| Integrations | 6 | 17% | 2 (KB-007, KB-008) | 1 |
| Access Control | 6 | 17% | 2 (KB-010, KB-011) | 2 |
| Compliance | 6 | 17% | 1 (KB-012) | 1 |
| Known Issue | 0* | 0% | 1 (KB-009) | 1 |
| **Reporting** | **0** | **0%** | **1 (KB-009)** | **1 (EVAL-009)** |

*Note: "Known Issue" may overlap with other categories in the data. KB-009 is tagged as "Reporting/Known Issue."

### Action Distribution

| Action | Count | % |
|---|---|---|
| Reply | 18 | 50% |
| Ask for more info | 12 | 33% |
| Escalate | 6 | 17% |

### Priority Distribution

| Priority | Count | Categories |
|---|---|---|
| Critical | 6 | Compliance |
| High | 12 | Authentication, Data Import |
| Medium | 12 | Billing, Integrations |
| Low | 6 | Access Control |

### Channel Distribution

| Channel | Count | % |
|---|---|---|
| Email | 12 | 33% |
| Chat | 12 | 33% |
| Portal | 12 | 33% |

Perfectly balanced -- unusual for real data but acceptable for a POC dataset.

### Sentiment Distribution

| Sentiment | Count | % |
|---|---|---|
| Frustrated | 12 | 33% |
| Neutral | 12 | 33% |
| Satisfied | 12 | 33% |

Also perfectly balanced.

---

## 5. Quality Issues

### ISSUE 1: Low Diversity -- 11 Unique Scenarios (Severity: HIGH)

**Finding**: Only 11 unique ticket descriptions exist across 36 records. Every ticket is a copy of one of 11 templates with metadata variations (different customers, sentiments, channels, dates). The 36-record count is inflated -- the effective training corpus is **11 distinct scenarios**.

**Impact**: The model may appear to generalize well on training data but is actually memorizing a small set of patterns. This won't reflect real-world performance on 1000 tickets/month.

**Recommendation**: Acceptable for POC architecture validation. For the 1000-question synthetic eval, generate diverse ticket variations -- different phrasings, edge cases, multi-issue tickets. Flag this limitation to Prasanna.

### ISSUE 2: Reporting Category Gap (Severity: HIGH)

**Finding**: KB-009 covers Reporting, and EVAL-009 tests a Reporting scenario, but there are **zero historical tickets** in the Reporting category. The model will be evaluated on a scenario it has never seen in training data.

**Impact**: The copilot will fail on Reporting tickets unless the LLM can match based on KB content alone (which is the correct behavior for retrieval, but classification will have no training signal).

**Recommendation**: Either add 2-3 synthetic Reporting tickets to the training set, or accept that Reporting is a cold-start test case and set expectations accordingly.

### ISSUE 3: Three Null source_kb_id Values (Severity: LOW)

**Finding**: TKT-1006, TKT-1031, and TKT-1035 have null `source_kb_id`, but their `resolution_summary` text references KB articles (e.g., "Resolved using KB-003").

**Impact**: Missing training signal for retrieval accuracy on these tickets.

**Recommendation**: Fix the 3 null values based on resolution summaries. ~5 minutes of effort.

### ISSUE 4: Deterministic Priority Mapping (Severity: MEDIUM)

**Finding**: Each category always maps to exactly one priority. Authentication = always High, Compliance = always Critical, etc. There is zero variance.

**Impact**: Priority prediction accuracy will be artificially inflated to ~100%. In production, the same category may have different priorities depending on urgency and context.

**Recommendation**: Acknowledge this in the Evaluation Plan. Priority accuracy on POC data is not a reliable predictor of production accuracy. For the synthetic eval set, introduce priority variance within categories.

### ISSUE 5: ER-005 Escalation Rule Untested (Severity: MEDIUM)

**Finding**: Escalation Rule ER-005 (Platform Operations, for MFA/authentication issues requiring platform intervention) has no historically escalated ticket. All MFA tickets were resolved via "Ask for more info." However, EVAL-002 tests this escalation path.

**Impact**: Cold-start evaluation scenario -- the model must infer the escalation rule from the rule definition alone.

**Recommendation**: This is actually a valid test of the copilot's reasoning ability. Keep it, but note that performance on this case may be lower initially.

---

## 6. Data Characteristics

### Text Length Analysis

| Data Type | Min Length | Max Length | Mean Length | Notes |
|---|---|---|---|---|
| Ticket subject | ~20 chars | ~60 chars | ~40 chars | Short, keyword-dense |
| Ticket description | ~50 chars | ~100 chars | ~65 chars | Very short (8-11 words) |
| KB article content | ~150 chars | ~350 chars | ~250 chars | Short (31-48 words) |
| KB agent notes | ~50 chars | ~150 chars | ~100 chars | Brief internal guidance |

**Key observation**: Both tickets and KB articles are unusually short compared to real support data. In production, tickets will likely be 3-10x longer with more context, history, and noise. The pilot architecture should handle longer texts without issues (chunking strategy, context window management).

### Cross-Reference Coverage

| Relationship | Coverage | Gaps |
|---|---|---|
| Ticket → KB article | 92% (33/36) | 3 nulls (fixable) |
| KB article → Tickets | 83% (10/12) | KB-003 has no structured ref; KB-009 (Reporting) has none |
| Escalation rule → Tickets | 80% (4/5) | ER-005 never triggered |
| Eval set → Categories | 88% (7/8*) | Reporting category only in eval, not training |

---

## 7. Feasibility Assessment

| Dimension | Assessment | Risk Level |
|---|---|---|
| **Data availability** | All required data present in Excel | Low |
| **Data quality** | Clean structure, 3 minor fixes needed | Low |
| **Data volume** | Sufficient for POC; insufficient for production ML | Medium |
| **Data diversity** | 11 unique scenarios -- low for generalization | High |
| **Cross-references** | Strong linkage between tickets, KB, rules | Low |
| **Category coverage** | 1 gap (Reporting) | Medium |
| **Production readiness** | Freshworks APIs available post-pilot | Low |
| **PII risk** | None in pilot data | Low |

---

## 8. Recommendations

### Quick Fixes (Before Sprint 1)

| # | Fix | Effort | Owner |
|---|---|---|---|
| 1 | Fill 3 null `source_kb_id` values | 5 min | Nancy |
| 2 | Add 2-3 synthetic Reporting tickets | 15 min | Nancy + Nishka |
| 3 | Add 1 ticket triggering ER-005 escalation | 10 min | Nancy |

### Architecture Considerations

| # | Consideration | Why |
|---|---|---|
| 1 | Design for longer texts | Production tickets will be 3-10x longer |
| 2 | Chunking strategy for KB | Production KB articles may be multi-page |
| 3 | Hybrid retrieval (vector + BM25) | Short texts benefit from keyword matching alongside semantic |
| 4 | Synthetic data generation pipeline | Need 1000+ diverse questions for go-live validation |
| 5 | Data refresh mechanism | Design for Freshworks API integration post-pilot |

### Evaluation Considerations

| # | Consideration | Why |
|---|---|---|
| 1 | Report priority accuracy separately | Deterministic mapping inflates scores |
| 2 | Flag Reporting as cold-start | No training data for this category |
| 3 | Introduce priority variance in synthetic set | Production will have mixed priorities per category |
| 4 | Weight eval by production distribution | Current even distribution may not match real traffic |

---

## 9. Data Pipeline Requirements (Nancy's Build Plan)

| Component | Pilot | Production |
|---|---|---|
| **Ingestion** | Read Excel sheets via pandas/openpyxl | Freshworks API connectors (tickets, KB, rules) |
| **Storage** | Local files / in-memory | Cloud database (PostgreSQL or similar) |
| **KB indexing** | Embed 12 articles → vector store | Embed all articles, schedule refresh |
| **Ticket processing** | Batch from Excel | Real-time from Freshdesk webhook or polling |
| **Data validation** | Schema checks on Excel | Schema + freshness + completeness checks |
| **Versioning** | Git (dataset in repo) | DVC or equivalent for data versioning |
