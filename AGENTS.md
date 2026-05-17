# AGENTS.md — AI coding assistant guide

This monorepo builds a **multi-tenant agentic digital marketing platform**. Follow [`.cursorrules`](.cursorrules) for production guardrails.

## Cursor plugins (install first)

Import the team marketplace from [`.cursor-plugin/marketplace.json`](.cursor-plugin/marketplace.json):

1. **Cursor → Settings → Plugins → Team Marketplaces → Import** this repository URL, or install locally from `plugins/aws` and `plugins/crewai`.
2. Official marketplace alternatives: [AWS plugin](https://cursor.com/marketplace), CrewAI skills via `npx skills add crewaiinc/skills`.

| Plugin | Provides |
|--------|----------|
| `plugins/aws` | AWS MCP (IAM), Firecracker rules, deploy skill |
| `plugins/crewai` | CrewAI docs MCP, agent/task skills |

## Documentation

| Topic | URL |
|-------|-----|
| CrewAI (machine-readable) | https://docs.crewai.com/llms.txt |
| AWS MCP Server | https://docs.aws.amazon.com/agent-toolkit/latest/userguide/mcp-server.html |
| Research blueprint | Google Doc (see README) |

## Stack map

- **Orchestration:** LangGraph (`packages/agents/amp_agents/graph.py`)
- **Parallel creative:** CrewAI (`packages/agents/amp_agents/crew_build.py`)
- **API:** FastAPI `apps/api` — all routes need OpenAPI metadata + `X-Tenant-Id`
- **UI:** Next.js 15 `apps/web` — Interactive Plans, not chat approval
- **Sandbox:** Firecracker only (`infra/sandbox/`) — not Docker for agent code

## MCP servers (`.cursor/mcp.json`)

- `aws-mcp` — requires `uv` + `aws configure` or SSO login
- `crewai-docs` — remote docs MCP
- `postgres` — `${DATABASE_URL}` for schema reads

## Common commands

```bash
cd apps/web && pnpm dev
cd apps/api && uvicorn app.main:app --reload
docker compose up postgres -d
crewai run   # when using CLI-scaffolded crews
```
