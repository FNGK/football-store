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

## Quick start

```bash
# API
cd apps/api && python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
uvicorn app.main:app --reload

# Web
cd apps/web && pnpm install && pnpm dev
```

## Phases (blueprint)

1. **Environment** — `.cursorrules`, MCP, stack, Firecracker config
2. **Data & CRM** — Zero-ETL, sGTM, Consent Mode v2, PII gateway
3. **Agent swarm** — Intake, Build, AI CMO, MAB/SBL, GeoLift MMM
4. **Security** — MVG guardrails, circuit breakers, IPI defense, compliance
5. **UI/UX** — Interactive Plans, onboarding, support bot, CRM feedback routing

See the research blueprint (Google Doc) for API warm-up timelines (Meta 15-day, Google Ads token review).
