# Agentic Digital Marketing Platform

Production-grade, multi-tenant agentic digital marketing platform with an integrated Master CRM backend.

## Repository setup

This project was initialized as a **greenfield replacement** of the legacy `football-store` scaffold. The GitHub integration token cannot create new repositories; to use a dedicated remote:

1. Create `agentic-marketing-platform` on GitHub (org or user).
2. Update the remote:
   ```bash
   git remote set-url origin https://github.com/YOUR_ORG/agentic-marketing-platform.git
   git push -u origin main
   ```

Alternatively, rename the existing `football-store` repository in GitHub Settings → General.

## Architecture

| Layer | Stack |
|-------|--------|
| Frontend | Next.js 15, Tailwind, shadcn/ui, assistant-ui |
| API | FastAPI, OpenAPI, SQLAlchemy |
| Agents | LangGraph (orchestration), CrewAI (parallel creative) |
| Sandbox | AWS Firecracker microVMs (not Docker for agent code) |
| Data | PostgreSQL (tenant RLS), BigQuery Zero-ETL adapter |
| Edge | Server-side GTM click-ID persistence |

## Monorepo layout

```
apps/web          Next.js dashboard (Generative UI)
apps/api          FastAPI Master CRM + agent control plane
packages/agents   LangGraph/CrewAI swarm
packages/crm      CRM domain models & repositories
packages/gateway  PII NER tokenization gateway
packages/shared   Types, guardrails, MCP rug-pull detection
services/sgtm     Click ID persistence (gclid/fbclid cookies)
infra/sandbox     Firecracker runner interface
```

## Cursor plugins (AWS + CrewAI)

This repo ships project plugins under [`plugins/aws`](plugins/aws) and [`plugins/crewai`](plugins/crewai), registered in [`.cursor-plugin/marketplace.json`](.cursor-plugin/marketplace.json).

| Plugin | MCP / capabilities |
|--------|-------------------|
| **aws** | AWS MCP Server via `uvx mcp-proxy-for-aws` (IAM SigV4) |
| **crewai** | CrewAI docs MCP + skills (`getting-started`, `design-agent`, `design-task`, `ask-docs`) |

**Setup**

1. Import the repo as a team marketplace in **Cursor → Settings → Plugins**, or install each plugin from `plugins/*`.
2. Configure AWS: `aws configure` or `aws sso login`; set `AWS_REGION` in `.env`.
3. Optional: `./scripts/install-cursor-plugins.sh` for official `crewaiinc/skills` via npx.
4. See [`AGENTS.md`](AGENTS.md) for assistant conventions.

VS Code / Cursor also recommends the **AWS Toolkit** extension via [`.vscode/extensions.json`](.vscode/extensions.json).

## Quick start

```bash
./scripts/generate-env.sh apps/api/.env   # once — creates JWT secret
docker compose up postgres -d
./scripts/dev-up.sh

# Login at http://localhost:3000/login
# Default: admin@example.com / ChangeMeNow123!  (change in apps/api/.env)
```

Production deploy: see [docs/PRODUCTION.md](docs/PRODUCTION.md).

## Phases (blueprint)

1. **Environment** — `.cursorrules`, MCP, stack, Firecracker config
2. **Data & CRM** — Zero-ETL, sGTM, Consent Mode v2, PII gateway
3. **Agent swarm** — Intake, Build, AI CMO, MAB/SBL, GeoLift MMM
4. **Security** — MVG guardrails, circuit breakers, IPI defense, compliance
5. **UI/UX** — Interactive Plans, onboarding, support bot, CRM feedback routing

See the research blueprint (Google Doc) for API warm-up timelines (Meta 15-day, Google Ads token review).
