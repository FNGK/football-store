---
name: design-task
description: Write CrewAI tasks with dependencies, structured output, and human review hooks. Use when defining SEO/Content/Web tasks.
---

# Design CrewAI tasks

## Patterns

- Prefix descriptions with `[{tenant_id}]` for traceability.
- Use `expected_output` to enforce JSON-LD blocks, HTML outlines, or copy variants.
- Chain SEO → Content → Web only when sequential dependency is required; default to **parallel** in `crew_build.py`.
- For Consent Mode or CRM data tasks, label `observed` vs `modeled` in output schema.

## Human review

Interactive Plans in `apps/web` replace chat-based HITL — crew outputs should map to plan sections, not free-form chat approvals.
