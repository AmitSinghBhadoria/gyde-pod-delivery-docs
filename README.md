# Gyde POD Delivery Docs

Central documentation hub for Gyde AI POD engagements. Built with [Docusaurus](https://docusaurus.io/) and deployed to GitHub Pages.

## Current Engagement: AI Support Copilot Pilot

**Client**: Prasanna (CIO / Business Lead / Product Owner)
**Duration**: 4 weeks (2 sprints)
**Status**: Discovery phase

### POD Team

| Role | Person |
|---|---|
| POD Lead (AI Engineer Lead) | Amit |
| AI Engineer | Atharva |
| Data Engineer | Nancy |
| QA | Nishka |
| Governance Engineer | Shubham |
| Implementation Manager | Shivani |

### What we're building

An AI support copilot that helps agents: classify tickets, retrieve relevant KB articles, recommend next-best-action (reply / ask for more info / escalate), draft grounded responses with citations, and provide full traceability.

Phase 1: one support queue, one knowledge source (12 KB articles), one escalation mechanism, human-in-the-loop only.

## Docs Site

**Live site**: https://amitsinghbhadoria.github.io/gyde-pod-delivery-docs/

Auto-deploys on every push to `main` via GitHub Actions.

## Local Development

```bash
npm install
npm start
```

Opens at `http://localhost:3000/gyde-pod-delivery-docs/`

## Docs Structure

```
docs/
├── index.md                    # Landing page
├── discovery/                  # Discovery phase artifacts
│   ├── discovery-call-questions.md
│   ├── pm-discovery-questions.md
│   └── discovery-call-invite.md
├── team/                       # Team reference docs
│   └── product-overview.md
└── engagement/                 # Engagement artifacts (charter, arch, eval plan)
    └── placeholder.md
```

## Framework Reference

This engagement follows the Gyde POD Operation Framework (21 documents). The framework PDFs are stored separately in the `Gyde AI POD Framework/` directory, not in this repo. Key references:

- Doc 01: Framework Overview & Charter
- Doc 02: POD Structure & RACI Matrix
- Doc 03: Project Planning & Estimation Playbook
- Doc 04: Agile Delivery Framework
- Doc 05: Client Engagement & Communication Protocol
- Doc 06: SDLC for AI Systems
- Doc 08: AI/Agent Development Standards
- Doc 17: Quality Assurance & Testing Strategy
