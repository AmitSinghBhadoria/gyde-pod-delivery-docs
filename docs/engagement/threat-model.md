---
sidebar_position: 10
title: Threat Model
---

# Threat Model (Initial) -- AI Support Copilot

**Engagement**: AI Support Copilot Pilot
**Owner**: Shubham (Governance Engineer)
**Version**: 1.0
**Date**: 2026-05-01
**Framework ref**: Doc 14 (Enterprise Security Framework)
**Non-negotiable**: Yes -- Doc 01, Section 5.1, Item 1 (Threat modeling and secrets management)

> This is the **initial threat model** produced during Discovery. It identifies the threat surface and top threats. A full threat model with validated mitigations is due by Sprint 1 demo (May 10). The threat model is a living document updated as the system evolves.

---

## 1. System Scope

### Components in Scope

| Component | Technology | Trust Level |
|---|---|---|
| Frontend | React (browser) | Untrusted (client-side) |
| Backend API | Express (Node.js) | Trusted (server-side) |
| Pipeline Orchestrator | LangChain.js | Trusted (server-side) |
| LLM Gateway | Custom abstraction layer | Trusted (server-side) |
| Operational DB | MongoDB | Trusted (data store) |
| Search Index | Elasticsearch | Trusted (data store) |
| LLM Service | Vertex AI (Gemini) | External trusted (Google-managed) |
| Embedding Service | Vertex AI text-embedding-005 | External trusted (Google-managed) |

### Components Out of Scope (Pilot)

- Freshdesk API integration (not built in pilot)
- Production infrastructure / load balancing
- Customer-facing endpoints (agent-facing only)
- Network-level security (firewall, VPN) -- deferred to production

---

## 2. Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                     TRUST BOUNDARY: Browser                      │
│                                                                  │
│  ┌──────────┐                                                   │
│  │  React   │ ──── (1) HTTP/REST ────┐                          │
│  │ Frontend │ ◄── (8) JSON response ─┤                          │
│  └──────────┘                        │                          │
└──────────────────────────────────────┼──────────────────────────┘
                                       │
┌──────────────────────────────────────┼──────────────────────────┐
│                TRUST BOUNDARY: Server (GCP VM)                   │
│                                      ▼                          │
│  ┌──────────────────────────────────────┐                       │
│  │         Express API Server           │                       │
│  │  (2) Validate + route request        │                       │
│  └──────────┬───────────────────────────┘                       │
│             │                                                    │
│             ▼                                                    │
│  ┌──────────────────────────────────────┐                       │
│  │     LangChain.js Pipeline            │                       │
│  │  (3) Classify ─► (4) Retrieve        │                       │
│  │  (5) Reason ──► (6) Draft            │                       │
│  │  (7) Guardrails                      │                       │
│  └──┬────────┬──────────────────────────┘                       │
│     │        │                                                   │
│     ▼        ▼                                                   │
│  ┌───────┐ ┌──────────────┐                                     │
│  │MongoDB│ │Elasticsearch │                                     │
│  │tickets│ │ kb_articles  │                                     │
│  │feedbk │ │ kb_vectors   │                                     │
│  │audit  │ │              │                                     │
│  └───────┘ └──────────────┘                                     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
                     │
                     │ (3,5,6) LLM API calls
                     │ (4) Embedding API call
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│           TRUST BOUNDARY: Google Cloud (External)                │
│                                                                  │
│  ┌─────────────────────────────────────┐                        │
│  │         Vertex AI                    │                        │
│  │  - Gemini (LLM)                     │                        │
│  │  - text-embedding-005               │                        │
│  │  (via Service Account auth)         │                        │
│  └─────────────────────────────────────┘                        │
└──────────────────────────────────────────────────────────────────┘
```

### Data Flow Legend

| # | Flow | Data | Protocol |
|---|---|---|---|
| 1 | Browser → API | Ticket ID, feedback payload | HTTPS (REST) |
| 2 | API → Pipeline | Ticket text, metadata | Internal function call |
| 3 | Pipeline → Vertex AI | Ticket text + prompt | HTTPS (gRPC via SDK) |
| 4 | Pipeline → Elasticsearch | Query embedding + search query | HTTP (internal) |
| 5 | Pipeline → Vertex AI | Ticket + KB context + prompt | HTTPS (gRPC via SDK) |
| 6 | Pipeline → Vertex AI | Ticket + KB + reasoning + prompt | HTTPS (gRPC via SDK) |
| 7 | Pipeline → Pipeline | All outputs → guardrail checks | Internal function call |
| 8 | API → Browser | Full pipeline output (JSON) | HTTPS (REST) |

---

## 3. STRIDE Analysis

### 3.1 Spoofing

| # | Threat | Component | Severity | Pilot Exposure | Mitigation |
|---|---|---|---|---|---|
| T-01 | **Unauthorized API access** -- attacker calls backend API directly without authentication | Express API | Medium | Low (internal network) | Pilot: CORS restriction to frontend origin. Production: add JWT auth, API keys |
| T-02 | **GCP Service Account key theft** -- leaked key grants Vertex AI access | LLM Gateway | High | Medium | Store key as env var or GCP Secret Manager; never commit to Git; rotate on suspicion |
| T-03 | **Agent impersonation** -- one agent submits feedback as another | Feedback API | Low | Low (pilot is internal team) | Pilot: accept risk (internal users). Production: tie feedback to authenticated session |

### 3.2 Tampering

| # | Threat | Component | Severity | Pilot Exposure | Mitigation |
|---|---|---|---|---|---|
| T-04 | **Prompt injection via ticket text** -- malicious ticket content manipulates LLM behavior | Pipeline (all LLM steps) | High | Medium | System prompt / user prompt separation; guardrails layer detects common injection patterns; LLM instructed to treat ticket as data, not instructions |
| T-05 | **KB article tampering** -- modified KB content causes incorrect responses | Elasticsearch | Medium | Low (static dataset) | Pilot: KB is read-only after ingestion. Production: access controls on KB update API; audit log on changes |
| T-06 | **Audit log tampering** -- modifying decision trail to hide bad outputs | MongoDB (audit_log) | Medium | Low | Pilot: append-only writes; no delete API exposed. Production: immutable audit store |

### 3.3 Repudiation

| # | Threat | Component | Severity | Pilot Exposure | Mitigation |
|---|---|---|---|---|---|
| T-07 | **Agent denies seeing copilot output** -- no proof of what was shown | Audit trail | Low | Low | Every pipeline run logged with full output, timestamp, ticket_id. Audit log is the proof. |
| T-08 | **Feedback without attribution** -- cannot trace who approved/rejected a response | Feedback system | Low | Low | Pilot: single-user environment. Production: require agent_id in feedback payload |

### 3.4 Information Disclosure

| # | Threat | Component | Severity | Pilot Exposure | Mitigation |
|---|---|---|---|---|---|
| T-09 | **PII leakage in draft response** -- copilot echoes customer PII from ticket into response unnecessarily | Draft pipeline step | High | Medium | Guardrails layer checks draft for PII patterns (SSN, email, phone); prompt instructs model not to echo PII unless relevant to resolution |
| T-10 | **Ticket data exposed to LLM provider** -- customer ticket content sent to Google | Vertex AI API calls | Medium | Medium | Accepted risk for pilot (Google Cloud ToS covers data handling). Production: evaluate data processing agreements; consider on-prem LLM |
| T-11 | **API returns excessive data** -- pipeline output includes internal metadata in response | Express API | Low | Low | API response schema defined; strip internal fields before returning to frontend |
| T-12 | **Secrets in logs or error messages** -- stack traces expose env vars or API keys | Express API | Medium | Medium | Error handling middleware returns generic error messages; structured logging excludes sensitive fields |

### 3.5 Denial of Service

| # | Threat | Component | Severity | Pilot Exposure | Mitigation |
|---|---|---|---|---|---|
| T-13 | **LLM rate limiting** -- excessive pipeline calls exhaust Vertex AI quota | Vertex AI | Medium | Low (low pilot volume) | Monitor API usage; implement request queuing; set per-minute rate limit on copilot endpoint |
| T-14 | **Large ticket text causes timeout** -- excessively long ticket overwhelms pipeline | Pipeline | Low | Low | Truncate ticket text to max token limit before sending to LLM; set pipeline timeout (15s hard limit) |
| T-15 | **Elasticsearch resource exhaustion** -- expensive queries consume all memory | Elasticsearch | Low | Low (small dataset) | Set query timeout; limit kNN candidates; monitor ES health |

### 3.6 Elevation of Privilege

| # | Threat | Component | Severity | Pilot Exposure | Mitigation |
|---|---|---|---|---|---|
| T-16 | **Prompt injection escalates to system-level actions** -- injected prompt causes LLM to call unauthorized tools or APIs | Pipeline | Medium | Low (no tool-use configured) | Pipeline uses structured output only; no function-calling / tool-use enabled; LLM cannot execute code or make external calls |
| T-17 | **MongoDB injection** -- malicious input in ticket text used to construct MongoDB query | Data Service | Medium | Medium | Use parameterized queries (Mongoose ODM); never interpolate user input into query strings |
| T-18 | **Frontend XSS** -- draft response contains script content rendered unsanitized in the browser | React Frontend | Medium | Medium | React auto-escapes JSX content by default; avoid using raw HTML injection; sanitize any rich content with a library like DOMPurify; set CSP headers |

---

## 4. Top Threats (Ranked)

| Rank | ID | Threat | Severity | Likelihood | Priority | Owner |
|---|---|---|---|---|---|---|
| 1 | T-04 | **Prompt injection via ticket text** | High | Medium | **Critical** | Atharva + Shubham |
| 2 | T-09 | **PII leakage in draft response** | High | Medium | **Critical** | Atharva + Shubham |
| 3 | T-02 | **GCP Service Account key theft** | High | Low | **High** | Amit |
| 4 | T-18 | **Frontend XSS via draft response** | Medium | Medium | **High** | Amit |
| 5 | T-17 | **MongoDB injection** | Medium | Medium | **High** | Amit + Nancy |
| 6 | T-10 | **Ticket data exposed to LLM provider** | Medium | High (by design) | **Medium** | Shubham |
| 7 | T-12 | **Secrets in logs/errors** | Medium | Medium | **Medium** | Amit |

---

## 5. Secrets Management

### Inventory

| Secret | Storage | Access Method | Rotation |
|---|---|---|---|
| GCP Service Account key (JSON) | GCP Secret Manager or env var | `GOOGLE_APPLICATION_CREDENTIALS` env var | On suspicion of compromise |
| MongoDB connection string | `.env` file (local) / env var (deployed) | `MONGODB_URI` env var | On credential change |
| Elasticsearch credentials | `.env` file (local) / env var (deployed) | `ES_URL` env var | On credential change |
| LLM provider API keys (fallback) | `.env` file (local) / env var (deployed) | `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` env vars | Quarterly |

### Rules

- **No secrets in code**: `.env` is in `.gitignore`; `.env.example` contains placeholder values only
- **No secrets in logs**: Logging middleware strips sensitive fields
- **No secrets in error responses**: Error handler returns generic messages
- **Service Account key never committed**: Key file path set via env var, file excluded from Git
- **`.env.example` documents all required vars** without actual values

---

## 6. Guardrails Mapping

Each guardrail addresses one or more threats:

| Guardrail | Threats Mitigated | Implementation |
|---|---|---|
| **Profanity filter** | -- (content quality, not security) | Word list + regex matching on draft output |
| **PII check** | T-09 (PII leakage) | Regex patterns for SSN, email, phone, credit card in draft output; flag if found |
| **Prompt injection detection** | T-04 (prompt injection) | Pattern matching for common injection phrases ("ignore previous", "system prompt", etc.) in ticket text |
| **Confidence gating** | T-04 (indirect -- low confidence may indicate manipulation) | Flag if any step confidence < 0.5 |
| **Hallucination check** | -- (accuracy, not security) | LLM-judge verifies all claims trace to cited KB articles |
| **Input length limit** | T-14 (DoS via large input) | Truncate ticket text > 4,000 tokens |

---

## 7. Compliance Considerations

| Area | Pilot Status | Production Requirement |
|---|---|---|
| **Data residency** | Data on GCP (Gyde account, region TBD) | Client's on-prem infrastructure; data never leaves their network |
| **Data processing agreement** | Vertex AI processes ticket text per Google Cloud ToS | Evaluate DPA with Google; or switch to on-prem LLM |
| **PII handling** | Excel dataset may contain simulated PII | Production: PII policy required; data minimization; retention limits |
| **Audit trail** | All copilot decisions logged | Production: define retention period; access controls on audit data |
| **Access control** | Single-user pilot; no auth | Production: role-based access; SSO integration |
| **Data retention** | No policy for pilot | Production: define retention and deletion policies per client requirements |

---

## 8. Action Items

| # | Action | Owner | Due | Status |
|---|---|---|---|---|
| 1 | Implement prompt injection guardrail (T-04) | Shubham + Atharva | Sprint 2 (May 11-13) | Pending |
| 2 | Implement PII check guardrail (T-09) | Shubham + Atharva | Sprint 2 (May 11-13) | Pending |
| 3 | Verify GCP Service Account key is not in Git (T-02) | Amit | Sprint 1 Day 1 (May 1) | Pending |
| 4 | Implement input sanitization / XSS prevention (T-18) | Amit | Sprint 1 (S1-10) | Pending |
| 5 | Use parameterized queries in MongoDB (T-17) | Amit + Nancy | Sprint 1 (S1-02, S1-09) | Pending |
| 6 | Configure structured logging without secrets (T-12) | Amit | Sprint 1 (S1-01) | Pending |
| 7 | Document data handling in Vertex AI calls (T-10) | Shubham | Sprint 1 | Pending |
| 8 | Build adversarial test cases for injection + PII (T-04, T-09) | Nishka + Shubham | Sprint 2 (S2-03) | Pending |
| 9 | Full security review and sign-off | Shubham | Sprint 2 (S2-10, May 14-15) | Pending |

---

## 9. Review Schedule

| Activity | When | Participants |
|---|---|---|
| Initial threat model review | May 1 (this document) | Shubham + Amit |
| Threat model update (post-M1) | May 10 (Sprint 1 demo) | Shubham |
| Security review (pre-delivery) | May 14-15 | Shubham + Amit |
| Security sign-off | May 15 | Shubham |

---

## Change Log

| Date | Change | By |
|---|---|---|
| 2026-05-01 | Initial threat model created with 18 threats across STRIDE categories | Shubham + Amit |

---

*Threat modeling is a non-negotiable framework requirement (Doc 01, Section 5.1). This initial model identifies the threat surface; full validation occurs during the security review in Sprint 2.*
