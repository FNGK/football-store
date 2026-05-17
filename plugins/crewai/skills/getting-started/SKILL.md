---
name: getting-started
description: Scaffold or extend CrewAI crews and flows in the AMP monorepo. Use when creating agents, tasks, crews, or wiring crewai run/deploy.
---

# CrewAI getting started (AMP)

## When to use

- Adding a new marketing build crew under `packages/agents/`
- Choosing between LangGraph workflow vs CrewAI parallel crew
- Running `crewai run` or integrating with FastAPI `POST /v1/agents/workflows/run`

## Project layout

| Path | Purpose |
|------|---------|
| `packages/agents/amp_agents/graph.py` | LangGraph intake |
| `packages/agents/amp_agents/crew_build.py` | Parallel SEO/Content/Web crew |
| `packages/agents/amp_agents/cmo_agent.py` | Budget / MAB logic |

## Instructions

1. Use **LangGraph** for cyclic orchestration and tenant checkpoint namespaces (`{tenant_id}:thread`).
2. Use **CrewAI** for parallel role-playing tasks with `Process.parallel`.
3. Install deps: `pip install crewai langgraph` in `apps/api` venv.
4. Query **crewai-docs** MCP for current API details before editing crew definitions.
5. Official skill pack: `npx skills add crewaiinc/skills` (optional, supplements this repo plugin).
