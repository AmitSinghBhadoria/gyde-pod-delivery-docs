---
sidebar_position: 14
title: UI Wireframes
---

# UI Wireframes -- AI Support Copilot

**Engagement**: AI Support Copilot Pilot
**Owner**: Amit (POD Lead)
**Version**: 1.0
**Date**: 2026-05-01
**Framework ref**: Doc 06 (SDLC for AI Systems)

---

## 1. Design Approach

The pilot UI is a **standalone web application** that simulates a support agent's workspace. It displays ticket data from the Excel dataset and integrates the AI copilot as a sidebar panel. This approach was chosen because the pilot does not integrate with Freshdesk -- the standalone app gives Prasanna a realistic demo without requiring API access to a live helpdesk system.

**Key design decisions**:
- Three-panel layout: Ticket Queue | Ticket Detail | Copilot Sidebar
- Copilot sidebar is always visible (no toggle) -- the entire point of the demo is showing the AI output
- All pipeline output is displayed: classification, recommended action, KB articles, draft response
- Confidence scores are shown per pipeline step to calibrate agent trust
- Accept / Edit / Override buttons enable the feedback loop

---

## 2. Main Screen: Agent Workspace

![UI Wireframe](../../client-docs/ui_wireframe.png)

### 2.1 Panel Layout

| Panel | Width | Content |
|---|---|---|
| **Ticket Queue** (left) | ~20% | Scrollable list of all 36 tickets from the dataset. Each ticket shows ID, subject line snippet, and status indicator |
| **Ticket Detail** (center) | ~45% | Full ticket view: subject, customer, channel, created date, description text, SLA countdown, and agent response text area |
| **Copilot Sidebar** (right) | ~35% | AI pipeline output: Classification, Recommended Action, Relevant KB Articles, Draft Response, and feedback controls |

### 2.2 Ticket Queue Panel

- Displays tickets as a vertical list with ticket ID and truncated subject
- Active ticket is highlighted
- Clicking a ticket loads it in the Ticket Detail panel and triggers the copilot pipeline
- Filter dropdown at bottom (by category, priority, status)
- Shows total ticket count

### 2.3 Ticket Detail Panel

| Section | Content |
|---|---|
| **Header** | Ticket ID, full subject line |
| **Metadata row** | Customer name, channel (Email/Chat/Phone), created date -- displayed as colored badges |
| **Description** | Full ticket text from the dataset |
| **SLA** | Time remaining countdown (hours + minutes), color-coded by urgency |
| **Agent Response** | Text area where the agent can type or paste the copilot's draft. Pre-populated with copilot draft when agent clicks "Accept" |
| **Send Reply** | Button to simulate sending the response |

### 2.4 Copilot Sidebar Panel

The copilot sidebar shows all 5 pipeline outputs in sequence:

| Section | Data Source | Display |
|---|---|---|
| **Classification** | Classify step output | Category tag, Priority badge (color-coded), Sentiment indicator, Confidence percentage |
| **Recommended Action** | Reason step output | Action type (Reply / Ask Clarification / Escalate) in a colored banner. For Escalate: shows escalation team and required context |
| **Relevant KB Articles** | Retrieve step output | Top 3 KB articles with ID, title, and relevance score (0-1). Clickable to expand full article content |
| **Draft Response** | Draft step output | Full generated response text. Includes [KB-XXX] citations that reference the KB articles above |
| **Controls** | Frontend | Accept (copies draft to Agent Response), Edit (opens draft in editable mode), Override (agent writes their own). Feedback row: "Was this helpful?" with Yes/No |

### 2.5 Header Bar

- **App title**: "AI Support Copilot"
- **Agent name**: Logged-in agent indicator (e.g., "Agent: Asha")
- **Version**: "Pilot v1.0"
- **Processing indicator**: Shows "Processing..." with spinner when pipeline is running

---

## 3. States and Interactions

### 3.1 Loading State

When the agent selects a ticket, the copilot sidebar shows a step-by-step progress indicator:
1. "Classifying ticket..." (Step 1)
2. "Searching knowledge base..." (Step 2)
3. "Analyzing and reasoning..." (Step 3)
4. "Drafting response..." (Step 4)
5. "Running guardrails..." (Step 5)

Each step shows a spinner while active and a checkmark when complete.

### 3.2 Error State

If the pipeline fails (LLM timeout, API error):
- Error banner at top of copilot sidebar (red background)
- Clear error message: "Pipeline failed: [reason]"
- "Retry" button to re-run the pipeline for the current ticket
- Agent can still manually type a response in the Agent Response area

### 3.3 Confidence Indicators (Sprint 2 Polish)

In Sprint 2 (S2-06), confidence scores get visual treatment:
- **Green** (>= 0.8): High confidence -- agent can trust the output
- **Yellow** (0.6 - 0.79): Medium confidence -- agent should verify
- **Red** (< 0.6): Low confidence -- agent should override

### 3.4 Guardrails Warnings (Sprint 2)

When guardrails flag an issue, a warning banner appears at the top of the copilot sidebar:
- **Critical** (red): Prompt injection detected, PII leakage found
- **Warning** (yellow): Low confidence, profanity detected, ungrounded claim

---

## 4. Component Mapping to Stories

| Component | Story | Sprint |
|---|---|---|
| Three-panel layout + ticket list + ticket detail | S1-10 | Sprint 1 |
| Copilot sidebar (basic: show pipeline output) | S1-10 | Sprint 1 |
| Accept / Edit / Override buttons | S1-10 | Sprint 1 |
| Feedback widget (Yes/No) | S1-10, S2-02 | Sprint 1 + 2 |
| Confidence score color-coding | S2-06 | Sprint 2 |
| KB article click-to-expand | S2-06 | Sprint 2 |
| Guardrails warning banners | S2-06 | Sprint 2 |
| Loading step-by-step progress | S2-06 | Sprint 2 |
| Error state with Retry button | S2-06 | Sprint 2 |
| Escalation callout box | S2-06 | Sprint 2 |

---

## 5. Technology

| Concern | Choice | Rationale |
|---|---|---|
| Framework | React 18 | Team familiarity; component model fits panel layout |
| State management | Zustand | Lightweight; simpler than Redux for a pilot |
| HTTP client | Axios | Promise-based; interceptors for error handling |
| Styling | Tailwind CSS | Utility-first; rapid prototyping without custom CSS files |
| Build tool | Vite | Fast dev server; React template out of the box |

---

## 6. Responsive Considerations

The pilot targets **desktop browsers only** (1280px+ viewport). Support agents use desktop workstations. No mobile or tablet layouts are planned for the pilot.

Production consideration: If the copilot moves to a Freshdesk sidebar widget, the layout would be a single-panel copilot (right sidebar only), since the ticket queue and detail are handled by Freshdesk.

---

## Change Log

| Date | Change | By |
|---|---|---|
| 2026-05-01 | Initial UI wireframes document created | Amit |
