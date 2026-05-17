# Cursor plugins (AWS + CrewAI)

Project-local [Cursor plugins](https://cursor.com/docs/plugins) for this monorepo.

## Install in Cursor

1. Open **Settings → Plugins → Team Marketplaces → Import**
2. Paste this repository URL (or a fork)
3. Enable **aws** and **crewai** from the parsed marketplace ([`.cursor-plugin/marketplace.json`](../.cursor-plugin/marketplace.json))

**Or** install from the [Cursor Marketplace](https://cursor.com/marketplace): search **AWS** and use `npx skills add crewaiinc/skills` for official CrewAI skills.

## aws

- **MCP:** `aws-mcp` via [mcp-proxy-for-aws](https://github.com/aws/mcp-proxy-for-aws) → `https://aws-mcp.us-east-1.api.aws/mcp`
- **Rules:** Firecracker-first, least-privilege IAM
- **Skill:** `deploy-firecracker-sandbox`

Requires: `uv`, AWS CLI credentials (`aws configure` / SSO).

## crewai

- **MCP:** `crewai-docs` → `https://docs.crewai.com/mcp`
- **Skills:** `getting-started`, `design-agent`, `design-task`, `ask-docs`
- **Rules:** LangGraph vs CrewAI responsibilities in `packages/agents/`
