---
name: design-agent
description: Configure CrewAI agents — role, goal, backstory, tools, LLMs, memory. Use when editing SEO, Content, Web, or CMO agents.
---

# Design CrewAI agents

## AMP marketing agents

| Agent | Role focus |
|-------|------------|
| SEO | JSON-LD, AEO/GEO, Google Indexing API cold-start |
| Content | FTC/CMA compliant copy, channel variants |
| Web | Landing pages, SXO friction reduction |
| AI CMO | Cross-channel overlap, MAB, minimum liquidity |

## Instructions

1. Every agent `goal` and `backstory` must reference tenant isolation.
2. Attach MCP tools only after schema hash registration (rug-pull detection).
3. Do not grant financial write tools without idempotency key middleware.
4. Use `verbose=False` in production crews; log via control plane API.
5. Validate outputs with structured `expected_output` on each Task.
