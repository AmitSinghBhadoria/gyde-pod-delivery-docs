---
sidebar_position: 5
title: Architecture Sketch
---

# Architecture Sketch -- AI Support Copilot

**Engagement**: AI Support Copilot Pilot
**Owner**: Amit (POD Lead)
**Version**: 1.0
**Date**: 2026-05-01
**Framework ref**: Doc 03, Section 3.4; Doc 06, Section 6.1

---

## 1. System Overview

The AI Support Copilot is a **RAG-based (Retrieval-Augmented Generation) system** with a sequential pipeline architecture. It receives a support ticket as input, classifies it, retrieves relevant KB articles, reasons over the combined context to recommend an action, and drafts a grounded response -- all presented to a human agent for review and approval.

### Architecture Pattern: RAG + Chain-of-Thought Reasoning

Why RAG (not fine-tuning or pure agentic):
- **Grounded responses**: Every output traces back to KB articles -- no hallucination
- **No training data needed**: 36 tickets is too few for fine-tuning; RAG works with any KB size
- **KB updates without retraining**: Add a KB article, re-index, done
- **Auditable**: Every response cites its sources
- **Portable**: No custom model weights to manage during on-prem handover

---

## 2. System Architecture Diagram

```
                          ┌─────────────────────────────────────┐
                          │         FRONTEND (React)            │
                          │   Three-panel dashboard:            │
                          │   Ticket Queue │ Detail │ Copilot   │
                          └──────────────┬──────────────────────┘
                                         │ REST API
                                         ▼
┌──────────────┐          ┌─────────────────────────────────────┐
│  DATA LAYER  │          │      BACKEND (Express / Node.js)    │
│              │          │                                     │
│  MongoDB     │◄────────►│  ┌─────────────────────────────┐   │
│  - Tickets   │          │  │   LangChain.js Orchestrator  │   │
│  - Feedback  │          │  │                               │   │
│  - Sessions  │          │  │  1. Classify (Gemini)         │   │
│  - Audit Log │          │  │  2. Retrieve (ES hybrid)      │   │
│              │          │  │  3. Reason (Gemini)            │   │
│  Elastic-    │◄────────►│  │  4. Draft (Gemini)             │   │
│  search      │          │  │  5. Guardrails (post-process)  │   │
│  - KB Index  │          │  │                               │   │
│  - Vectors   │          │  └─────────────────────────────┘   │
│  - BM25      │          │                                     │
└──────────────┘          │  LLM Gateway (provider-agnostic)    │
                          │         │                           │
                          └─────────┼───────────────────────────┘
                                    │
                                    ▼
                          ┌─────────────────────┐
                          │   Google Vertex AI   │
                          │   - Gemini (LLM)     │
                          │   - text-embedding   │
                          │     -005             │
                          │   (via Service Acct) │
                          └─────────────────────┘
```

---

## 3. Component Architecture

### 3.1 Frontend -- React

| Component | Purpose |
|---|---|
| **TicketQueue** | Left panel: list of tickets from dataset, filterable by category/priority/status |
| **TicketDetail** | Center panel: full ticket view with metadata, description, SLA, response area |
| **CopilotSidebar** | Right panel: classification, KB matches, recommended action, draft response, confidence |
| **FeedbackWidget** | "Was this helpful?" + edit capability; posts corrections to backend |
| **ResponseEditor** | Rich text editor for agent to modify draft before accepting |

**State management**: React Context or Zustand (lightweight, no Redux overhead).
**API communication**: Axios or fetch to Express REST endpoints.

### 3.2 Backend -- Express (Node.js)

| Module | Responsibility | Key Endpoints |
|---|---|---|
| **API Router** | REST endpoints for frontend | `POST /api/copilot/process`, `GET /api/tickets`, `POST /api/feedback` |
| **LLM Gateway** | Provider-agnostic LLM abstraction | Wraps Vertex AI; swappable to OpenAI/Anthropic via config |
| **Pipeline Orchestrator** | LangChain.js sequential chain | Classify → Retrieve → Reason → Draft → Guardrails |
| **Data Service** | MongoDB CRUD operations | Tickets, feedback, audit logs |
| **Search Service** | Elasticsearch queries | Hybrid search (vector + BM25) |
| **Guardrails Service** | Post-processing safety checks | Profanity filter, confidence gating, hallucination check |
| **Audit Logger** | Logs every copilot decision | Input, output, confidence, sources, reasoning, timestamp |

### 3.3 AI Pipeline -- LangChain.js

```
Input: ticket_text (string)
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 1: CLASSIFY                                         │
│ Model: Gemini via Vertex AI                              │
│ Prompt: System prompt + ticket text → structured JSON    │
│ Output: { category, priority, sentiment, confidence }    │
│ Technique: Structured output with JSON schema            │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 2: RETRIEVE                                         │
│ Engine: Elasticsearch hybrid search                      │
│ Method: Vector similarity (cosine) + BM25 keyword match  │
│ Embedding: Vertex AI text-embedding-005 (768 dimensions) │
│ Input: ticket_text embedded → kNN search + BM25 query    │
│ Fusion: Reciprocal Rank Fusion (RRF) to merge results    │
│ Output: top-K KB articles with relevance scores          │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 3: REASON                                           │
│ Model: Gemini via Vertex AI                              │
│ Input: ticket + retrieved KB articles + escalation rules │
│ Prompt: Chain-of-thought reasoning prompt                │
│ Output: { action, reasoning, escalation_team?,           │
│           required_context?, confidence }                │
│ Logic:                                                   │
│   - If KB match + resolution exists → Reply              │
│   - If insufficient info to resolve → Ask for more info  │
│   - If escalation rule triggers → Escalate + team + ctx  │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 4: DRAFT                                            │
│ Model: Gemini via Vertex AI                              │
│ Input: ticket + KB articles + action + reasoning         │
│ Prompt: Generate response grounded in KB with citations  │
│ Output: { draft_response, cited_kb_ids, tone }           │
│ Constraints: Must cite sources, match customer sentiment │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 5: GUARDRAILS (Post-processing)                     │
│ Checks: Profanity filter, PII leak check, confidence     │
│         threshold, hallucination check (all claims must   │
│         trace to KB), misuse pattern detection            │
│ If any check fails: flag to agent with warning, do not   │
│ suppress — show draft with disclaimer                    │
│ Output: { all pipeline outputs + guardrail_status }      │
└─────────────────────────────────────────────────────────┘
```

### 3.4 Data Layer

#### MongoDB Collections

| Collection | Purpose | Key Fields |
|---|---|---|
| `tickets` | Ingested ticket data | ticket_id, subject, description, category, priority, channel, status |
| `feedback` | Agent corrections and ratings | ticket_id, helpful (bool), original_draft, edited_draft, timestamp |
| `sessions` | Agent session tracking | agent_id, session_start, tickets_processed |
| `audit_log` | Complete copilot decision trail | ticket_id, pipeline_output (full), latency_ms, model_version, timestamp |

#### Elasticsearch Indices

| Index | Purpose | Fields | Configuration |
|---|---|---|---|
| `kb_articles` | KB article storage + search | kb_id, title, content, keywords, agent_notes, category | Standard analyzer for BM25 |
| `kb_vectors` | KB article embeddings | kb_id, embedding (dense_vector, 768 dims) | HNSW index, cosine similarity |

**Hybrid search implementation**: Single query combines kNN on `kb_vectors` with BM25 on `kb_articles`, results merged via Reciprocal Rank Fusion (RRF). Elasticsearch 8.x supports this natively with the `_search` API's `knn` + `query` combination.

### 3.5 LLM Gateway

```javascript
// Provider-agnostic interface
interface LLMProvider {
  generateStructured(prompt, schema, options) → JSON
  generateText(prompt, options) → string
  embed(text) → number[]
}

// Implementations
class VertexAIProvider implements LLMProvider { ... }  // Default
class OpenAIProvider implements LLMProvider { ... }    // Fallback
class AnthropicProvider implements LLMProvider { ... } // Fallback

// Configuration-driven selection
const provider = createProvider(config.LLM_PROVIDER) // "vertex-ai" | "openai" | "anthropic"
```

Provider selected via environment variable. Swap with zero code changes.

### 3.6 Feedback Loop

```
Agent accepts/edits draft
        │
        ▼
POST /api/feedback
  {
    ticket_id,
    helpful: true/false,
    original_draft,     // copilot's version
    edited_draft,       // agent's version (if edited)
    action_override     // if agent changed the recommended action
  }
        │
        ▼
Stored in MongoDB `feedback` collection
        │
        ▼
Future: Use accumulated feedback as few-shot examples
        in prompts or for fine-tuning
```

---

## 4. Technology Decisions

| Decision | Choice | Rationale | Alternatives Considered |
|---|---|---|---|
| Architecture pattern | RAG | Grounded responses, no training data needed, auditable | Fine-tuning (insufficient data), Pure agentic (over-complex) |
| LLM | Gemini via Vertex AI | Single GCP service account, native integration, strong structured output | GPT-4o, Claude (kept as fallbacks via LLM Gateway) |
| Embeddings | Vertex AI text-embedding-005 | Same service account, 768 dims, good multilingual base | OpenAI ada-002, Cohere, BGE |
| Retrieval | Elasticsearch hybrid (vector + BM25) | Native hybrid search, self-hostable, production-proven | ChromaDB (no BM25), pgvector (no native BM25), Qdrant (no BM25) |
| Operational DB | MongoDB | Flexible schema for tickets + feedback, team familiarity | PostgreSQL (viable but less flexible for pilot iteration) |
| Backend | Express (Node.js) | Team expertise (Amit + Atharva), fast iteration | FastAPI/Python (viable but slower team velocity) |
| Frontend | React | Standard, team familiarity, component model fits three-panel layout | Next.js (SSR not needed for internal tool) |
| Orchestration | LangChain.js | Provider abstraction, structured output parsing, ES + MongoDB integrations | Custom pipeline (more boilerplate), LlamaIndex (Python-focused) |
| Search fusion | Reciprocal Rank Fusion | Balanced merge of vector + keyword results, no tuning needed | Weighted average (requires tuning), Cohere reranker (extra cost) |

---

## 5. Integration Points

| Integration | Pilot | Production |
|---|---|---|
| **Ticket source** | Excel → MongoDB (one-time ingestion script) | Freshworks Ticket API → MongoDB (webhook or polling) |
| **KB source** | Excel → Elasticsearch (one-time indexing script) | Freshworks KB API → Elasticsearch (scheduled refresh) |
| **Escalation rules** | JSON config file loaded at startup | Freshworks or config service |
| **LLM** | Vertex AI (Gemini) via Google Service Account | Same, or swap via LLM Gateway config |
| **Agent interface** | Standalone React web app | Chrome extension calling same backend API |

---

## 6. GCP Service Account Permissions

| Permission / Role | Service | Why |
|---|---|---|
| `roles/aiplatform.user` | Vertex AI | LLM (Gemini) and embedding API calls |
| `roles/serviceusage.serviceUsageConsumer` | Service Usage | Enable required APIs |
| Vertex AI API enabled (`aiplatform.googleapis.com`) | -- | Required for Gemini and embeddings |

MongoDB and Elasticsearch run on the VM -- no additional GCP IAM needed. Firewall rules for internal access only.

---

## 7. Non-Functional Requirements

| Requirement | Target | How |
|---|---|---|
| **Latency** | < 10 seconds per ticket (full pipeline) | Parallel where possible (classify + retrieve can run concurrently) |
| **Portability** | Full on-prem handover post-pilot | All components self-hostable; no managed-only services |
| **LLM agnostic** | Swap provider with zero code changes | LLM Gateway abstraction; provider selected via env config |
| **Auditability** | Every decision traceable | Audit log with full pipeline output per ticket |
| **Security** | No secrets in code | GCP Service Account for auth; env vars for config |
| **Versioning** | All prompts and data in Git | Prompts as template files; dataset versioned in repo |

---

## 8. Walking Skeleton (Sprint 1 Target)

The thinnest end-to-end slice proving the architecture works:

1. **Input**: One hardcoded ticket from the dataset
2. **Classify**: Gemini returns category + priority (structured JSON)
3. **Retrieve**: Elasticsearch returns top-1 KB article (hybrid search)
4. **Reason**: Gemini returns action recommendation
5. **Draft**: Gemini returns grounded response with citation
6. **Present**: React UI shows the full copilot output in the sidebar

When this works end-to-end, the architecture is validated. Everything after is iteration and expansion.

---

## 9. Directory Structure (Proposed)

```
ai-support-copilot/
├── client/                     # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── TicketQueue/
│   │   │   ├── TicketDetail/
│   │   │   ├── CopilotSidebar/
│   │   │   └── FeedbackWidget/
│   │   ├── services/           # API client
│   │   └── App.jsx
│   └── package.json
├── server/                     # Express backend
│   ├── src/
│   │   ├── routes/             # API endpoints
│   │   ├── pipeline/           # LangChain.js pipeline
│   │   │   ├── classify.js
│   │   │   ├── retrieve.js
│   │   │   ├── reason.js
│   │   │   ├── draft.js
│   │   │   └── guardrails.js
│   │   ├── providers/          # LLM Gateway
│   │   │   ├── base.js         # Interface
│   │   │   ├── vertex-ai.js
│   │   │   ├── openai.js
│   │   │   └── index.js        # Factory
│   │   ├── services/           # MongoDB, Elasticsearch
│   │   ├── middleware/         # Auth, logging, error handling
│   │   └── config/            # Environment config
│   └── package.json
├── data/                       # Dataset and ingestion scripts
│   ├── ingest.js              # Excel → MongoDB + Elasticsearch
│   └── dataset/               # Raw Excel file
├── prompts/                    # Versioned prompt templates
│   ├── classify.txt
│   ├── reason.txt
│   └── draft.txt
├── eval/                       # Evaluation harness
│   ├── golden-set/            # Test cases (JSON)
│   ├── scorers/               # Scoring functions
│   └── run-eval.js            # Eval runner
├── docs/                       # Architecture docs, ADRs
├── .env.example               # Environment template (no secrets)
└── docker-compose.yml         # MongoDB + Elasticsearch for local dev
```
