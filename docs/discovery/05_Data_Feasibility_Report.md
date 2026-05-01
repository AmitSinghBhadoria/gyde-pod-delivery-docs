# Data Feasibility Report: AI Support Copilot POC Dataset

**Document ID:** 05
**Phase:** Discovery
**Date:** 2026-04-30
**Prepared by:** Amit (POD Lead)
**Dataset:** `ai_support_copilot_poc_dataset.xlsx`

---

## 1. Dataset Overview

The dataset contains **5 sheets** (including a README) designed as a synthetic dataset for evaluating ticket classification, KB retrieval, action recommendation, and response drafting.

| Sheet | Records | Columns | Purpose |
|---|---|---|---|
| README | 5 | 2 | Dataset usage instructions |
| Tickets_Historical | 36 | 15 | Historical support tickets for training/grounding |
| KB_Articles | 12 | 6 | Knowledge base articles for retrieval |
| Escalation_Rules | 5 | 5 | Routing rules for escalation decisions |
| Evaluation_Set | 12 | 8 | Held-out blind test set |

---

## 2. Sheet-by-Sheet Analysis

### 2.1 Tickets_Historical (36 records, 15 columns)

**Columns:** `ticket_id`, `created_at`, `customer_name`, `channel`, `subject`, `description`, `category`, `priority`, `sentiment`, `assigned_agent`, `status`, `source_kb_id`, `expected_next_best_action`, `resolution_summary`, `target_sla_hours`

#### Completeness

| Column | Null Count | Percentage | Notes |
|---|---|---|---|
| source_kb_id | 3 | 8.3% | TKT-1006, TKT-1031, TKT-1035 (all Billing/invoice copy tickets) |
| All other columns | 0 | 0% | Fully populated |

**Finding:** The 3 null `source_kb_id` entries are Billing invoice-copy tickets. Their `resolution_summary` fields all reference "Resolved using KB-003," so the KB link exists in the resolution text but is missing from the structured field. This is a **data entry gap that should be corrected** -- `source_kb_id` should be `KB-003` for these three rows.

#### Distribution Analysis

**Category Distribution:**

| Category | Count | % |
|---|---|---|
| Data Import | 8 | 22.2% |
| Authentication | 6 | 16.7% |
| Integrations | 6 | 16.7% |
| Billing | 6 | 16.7% |
| Known Issue | 4 | 11.1% |
| Access Control | 3 | 8.3% |
| Compliance | 3 | 8.3% |
| **Reporting** | **0** | **0%** |

**Priority Distribution:**

| Priority | Count | % |
|---|---|---|
| Medium | 14 | 38.9% |
| High | 12 | 33.3% |
| Low | 7 | 19.4% |
| Critical | 3 | 8.3% |

**Channel Distribution:**

| Channel | Count | % |
|---|---|---|
| Portal | 14 | 38.9% |
| Email | 11 | 30.6% |
| Chat | 11 | 30.6% |

**Sentiment Distribution:**

| Sentiment | Count | % |
|---|---|---|
| Calm | 16 | 44.4% |
| Neutral | 11 | 30.6% |
| Frustrated | 9 | 25.0% |

**Expected Next Best Action:**

| Action | Count | % |
|---|---|---|
| Reply | 20 | 55.6% |
| Escalate | 12 | 33.3% |
| Ask for more info | 4 | 11.1% |

**Status Distribution:**

| Status | Count | % |
|---|---|---|
| Resolved | 24 | 66.7% |
| Escalated | 12 | 33.3% |

**SLA Distribution:**

| Target SLA | Count | % |
|---|---|---|
| 4 hours | 3 | 8.3% |
| 12 hours | 8 | 22.2% |
| 24 hours | 12 | 33.3% |
| 48 hours | 13 | 36.1% |

---

### 2.2 KB_Articles (12 records, 6 columns)

**Columns:** `kb_id`, `title`, `category`, `content`, `keywords`, `agent_note`

#### Completeness
All 12 records are **100% complete** -- no null or empty values in any column.

#### Distribution

**Category Distribution:**

| Category | KB Articles | Article IDs |
|---|---|---|
| Authentication | 2 | KB-001, KB-002 |
| Billing | 2 | KB-003, KB-004 |
| Data Import | 2 | KB-005, KB-006 |
| Integrations | 2 | KB-007, KB-008 |
| Reporting | 1 | KB-009 |
| Access Control | 1 | KB-010 |
| Known Issue | 1 | KB-011 |
| Compliance | 1 | KB-012 |

**Content Length:**

| Metric | Characters | Words |
|---|---|---|
| Min | 199 | 31 |
| Max | 281 | 48 |
| Mean | 248 | 38.7 |
| Median | 254 | 39 |

All articles are short (199-281 characters, 31-48 words). 11 of 12 fall in the 200-281 character range; KB-010 (Access Control) is the shortest at 199 characters. There is **no significant length variation** -- articles are uniformly concise procedural snippets.

---

### 2.3 Escalation_Rules (5 records, 5 columns)

**Columns:** `rule_id`, `route_to_team`, `trigger_condition`, `severity`, `minimum_context_required`

#### Completeness
All 5 records are **100% complete**.

#### Coverage

| Rule | Route-to Team | Severity | Linked Categories |
|---|---|---|---|
| ER-001 | Engineering | High | Data Import (no KB match, multi-user workflow block) |
| ER-002 | Integrations Engineering | High | Integrations (sync/webhook/SSL failures) |
| ER-003 | Finance Operations | Medium | Billing (duplicate charge, pricing dispute) |
| ER-004 | Compliance | Critical | Compliance (PII, legal, subpoena) |
| ER-005 | Platform Operations | High | Authentication (MFA delivery, multi-user) |

---

### 2.4 Evaluation_Set (12 records, 8 columns)

**Columns:** `eval_id`, `short_label`, `ticket_text`, `expected_category`, `expected_priority`, `expected_primary_kb`, `expected_next_best_action`, `expected_reasoning_hint`

#### Completeness
All 12 records are **100% complete**.

#### Distribution

| Category | Eval Cases | Expected Actions |
|---|---|---|
| Authentication | 2 | Reply, Escalate |
| Billing | 2 | Reply, Escalate |
| Data Import | 2 | Reply, Ask for more info |
| Integrations | 2 | Reply, Escalate |
| Reporting | 1 | Reply |
| Access Control | 1 | Reply |
| Known Issue | 1 | Reply |
| Compliance | 1 | Escalate |

**Action Distribution:** Reply (6), Escalate (5), Ask for more info (1)
**Priority Distribution:** High (4), Medium (4), Low (3), Critical (1)

---

## 3. Quality Issues

### 3.1 CRITICAL: Massive Description Duplication

**Only 11 unique descriptions exist across 36 tickets.** Every ticket is an exact copy of one of 11 template descriptions. The duplicates differ only in metadata fields (customer name, channel, sentiment, agent, date).

| Unique Description (truncated) | Copies | Category |
|---|---|---|
| "Customer reports missing records after successful import..." | 4 | Data Import |
| "User reports no MFA code on registered number..." | 4 | Authentication |
| "Connector shows disconnected and no records synced..." | 4 | Integrations |
| "Customer reports duplicate notifications after editing..." | 4 | Known Issue |
| "User uploaded customer file and received validation error..." | 4 | Data Import |
| "Customer says renewal amount is above signed quote..." | 3 | Billing |
| "Billing admin requested invoice PDF..." | 3 | Billing |
| "Customer requests raw PII export..." | 3 | Compliance |
| "User says approvals module disappeared..." | 3 | Access Control |
| "Customer endpoint receiving repeated failures..." | 2 | Integrations |
| "Customer cannot access dashboard..." | 2 | Authentication |

**Impact:** A retrieval model trained on these tickets will see minimal lexical diversity per category. The dataset is effectively **11 unique scenarios**, not 36. This is acceptable for a POC proof-of-concept but would need significant expansion for production.

### 3.2 Category-Priority is Fully Deterministic (1:1 Mapping)

Every category maps to exactly one priority level:

| Category | Priority (Always) |
|---|---|
| Access Control | Low |
| Authentication | High |
| Billing | Medium |
| Compliance | Critical |
| Data Import | Medium |
| Integrations | High |
| Known Issue | Low |

**Impact:** A model could learn to predict priority purely from category, without understanding ticket content. In real-world data, priority would vary within categories based on urgency context. This means **priority prediction accuracy may be artificially inflated** in POC evaluation.

### 3.3 Missing `source_kb_id` for 3 Billing Tickets

TKT-1006, TKT-1031, and TKT-1035 have `source_kb_id = null`, but their `resolution_summary` says "Resolved using KB-003." This is a data entry inconsistency -- the structured field should contain `KB-003`.

### 3.4 No Formatting or Encoding Issues

- All categorical fields are clean (no leading/trailing whitespace)
- No duplicate IDs in any sheet
- All non-null KB references in tickets resolve to valid KB IDs
- All eval KB references resolve to valid KB IDs
- Date range is consistent: Feb 1-19, 2026 (17 days)

---

## 4. Gap Analysis

### 4.1 Category Coverage Matrix

| Category | Tickets | KB Articles | Eval Set | Escalation Rule |
|---|---|---|---|---|
| Access Control | 3 | 1 (KB-010) | 1 (EVAL-008) | -- |
| Authentication | 6 | 2 (KB-001,002) | 2 (EVAL-001,002) | ER-005 |
| Billing | 6 | 2 (KB-003,004) | 2 (EVAL-003,004) | ER-003 |
| Compliance | 3 | 1 (KB-012) | 1 (EVAL-012) | ER-004 |
| Data Import | 8 | 2 (KB-005,006) | 2 (EVAL-005,006) | ER-001 |
| Integrations | 6 | 2 (KB-007,008) | 2 (EVAL-007,010) | ER-002 |
| Known Issue | 4 | 1 (KB-011) | 1 (EVAL-011) | -- |
| **Reporting** | **0** | **1 (KB-009)** | **1 (EVAL-009)** | **--** |

### 4.2 Critical Gap: "Reporting" Category Has Zero Training Tickets

KB-009 ("Report generation timeout") and EVAL-009 (quarterly revenue report timing out) both reference a **Reporting** category, but there are **zero historical tickets** in this category. The model will have no grounding examples for this category. This is a **blind spot** in the training data -- the eval set will test a scenario the model has never seen in the historical corpus.

**Recommendation:** Add 2-3 synthetic Reporting tickets to Tickets_Historical, or accept that Reporting classification will rely entirely on KB-009 content matching and zero-shot generalization.

### 4.3 Escalation Rule Reachability

| Rule | Reachable via Ticket Data? | Evidence |
|---|---|---|
| ER-001 (Engineering) | Yes | 4 Data Import tickets escalated |
| ER-002 (Integrations Eng) | Yes | 2 Integrations tickets escalated (webhook/SSL) |
| ER-003 (Finance Ops) | Yes | 3 Billing tickets escalated (renewal mismatch) |
| ER-004 (Compliance) | Yes | 3 Compliance tickets escalated (PII export) |
| ER-005 (Platform Ops) | Partially | MFA tickets exist (4) but none are escalated in historical data; all resolved via "Ask for more info". EVAL-002 expects escalation to ER-005. |

**Finding:** ER-005 is technically reachable (MFA multi-user scenario) but there is no historical ticket that was actually escalated through this rule. The eval set tests this path (EVAL-002), making it a **cold-start evaluation scenario**.

### 4.4 Categories with Insufficient Training Data

| Category | Ticket Count | Assessment |
|---|---|---|
| **Reporting** | 0 | **Critically insufficient** -- no training data at all |
| Access Control | 3 (1 unique scenario) | Low -- single scenario repeated |
| Compliance | 3 (1 unique scenario) | Low -- single scenario repeated |
| Known Issue | 4 (1 unique scenario) | Low -- single scenario repeated |

When accounting for description deduplication, most categories have only **1-2 truly unique scenarios**, which is thin even for a POC.

### 4.5 Unused KB Articles

| KB Article | Category | Referenced by Tickets? | In Eval? |
|---|---|---|---|
| KB-003 (Invoice copy and billing history) | Billing | No (despite being used in resolutions -- `source_kb_id` is null) | Yes (EVAL-003) |
| KB-009 (Report generation timeout) | Reporting | No (zero Reporting tickets) | Yes (EVAL-009) |

---

## 5. Data Characteristics

### 5.1 Text Length Profile

| Metric | Ticket Descriptions | KB Article Content |
|---|---|---|
| Min length (chars) | 51 | 199 |
| Max length (chars) | 84 | 281 |
| Mean length (chars) | 65 | 248 |
| Median length (chars) | 61 | 254 |
| Min words | 8 | 31 |
| Max words | 11 | 48 |
| Mean words | 8.9 | 38.7 |
| KB-to-Ticket ratio | -- | 3.8x longer |

**Finding:** Ticket descriptions are uniformly short (8-11 words each). KB articles are uniformly 31-48 words. Both are unusually compact -- real-world tickets and KB articles would be significantly longer and more variable. This means the POC will test retrieval on **short, low-ambiguity text** which may overstate accuracy relative to production conditions.

### 5.2 Ticket-to-KB Mapping

- **No ticket maps to multiple KB articles.** The `source_kb_id` field is always a single value (or null). In real-world scenarios, a ticket could require information from multiple KB sources.
- **KB-003 and KB-009 have zero ticket mappings** (though KB-003 is referenced in resolution text).
- KB articles are referenced between 2-4 times each (excluding unused ones), indicating reasonable distribution.

### 5.3 Customer Distribution

| Customer | Tickets |
|---|---|
| Northbridge Finance | 8 (22.2%) |
| Acme Capital | 6 (16.7%) |
| ZenShop | 5 (13.9%) |
| UrbanLend | 5 (13.9%) |
| FinEdge | 5 (13.9%) |
| CredAxis | 4 (11.1%) |
| PrimeLeaf Health | 2 (5.6%) |
| BluePeak Retail | 1 (2.8%) |

8 unique customers across 36 tickets. Distribution is somewhat skewed toward Northbridge Finance.

---

## 6. Summary of Findings

### Strengths
1. **Clean structure** -- no encoding issues, consistent naming, valid cross-references
2. **Full category coverage** in KB and Eval sets (all 8 categories represented)
3. **All 5 escalation rules are logically reachable** from the data scenarios
4. **Eval set is well-designed** -- covers all categories, all action types, and all priority levels
5. **Clear separation** of training data (Tickets_Historical) from test data (Evaluation_Set)

### Weaknesses and Risks

| # | Issue | Severity | Recommendation |
|---|---|---|---|
| 1 | **Only 11 unique ticket descriptions** across 36 records | High | Accept for POC; flag that production needs 200+ unique tickets |
| 2 | **Reporting category has 0 training tickets** | High | Add 2-3 synthetic Reporting tickets, or document as known blind spot |
| 3 | **Category-to-Priority is deterministic 1:1** | Medium | Accept for POC; note that priority prediction metrics will be inflated |
| 4 | **3 tickets missing `source_kb_id`** (should be KB-003) | Low | Fix data: set `source_kb_id = KB-003` for TKT-1006, TKT-1031, TKT-1035 |
| 5 | **ER-005 has no historically escalated ticket** | Medium | Add 1 ticket that was escalated via ER-005, or accept cold-start eval |
| 6 | **Very short text lengths** (8-11 word tickets, 31-48 word KB) | Medium | Accept for POC; note real-world text will be longer and noisier |
| 7 | **No multi-KB ticket mappings** | Low | Accept for POC; real-world tickets may need multi-article retrieval |
| 8 | **KB-003 and KB-009 unused in structured ticket refs** | Low | Fix KB-003 (see #4); KB-009 has no tickets (see #2) |

### Overall Feasibility Assessment

**The dataset is feasible for a POC** with the above caveats. It provides enough structure to demonstrate all four copilot capabilities (classification, retrieval, action recommendation, response drafting). The main risks are around low diversity (11 unique scenarios) and the Reporting category gap. These should be flagged to the client as known limitations that would be addressed in a production dataset.

**Recommended pre-POC fixes (effort: ~30 minutes):**
1. Set `source_kb_id = KB-003` for tickets TKT-1006, TKT-1031, TKT-1035
2. Add 2-3 Reporting category tickets to Tickets_Historical
3. Add 1 Authentication ticket that escalates via ER-005 (multi-user MFA outage)
