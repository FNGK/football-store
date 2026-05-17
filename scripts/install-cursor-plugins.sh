#!/usr/bin/env bash
# Install optional official CrewAI skills pack (supplements repo plugins/crewai).
set -euo pipefail

echo "==> CrewAI official skills (crewaiinc/skills)"
if command -v npx >/dev/null 2>&1; then
  npx --yes skills add crewaiinc/skills || echo "WARN: skills CLI failed — use Cursor marketplace or plugins/crewai instead"
else
  echo "WARN: npx not found; skip or install Node.js 20+"
fi

echo "==> AWS MCP prerequisites"
if ! command -v uvx >/dev/null 2>&1; then
  echo "Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
fi
if ! command -v aws >/dev/null 2>&1; then
  echo "Install AWS CLI v2 and run: aws configure  (or aws sso login)"
fi

echo "Done. Enable plugins/aws and plugins/crewai via Cursor Settings → Plugins,"
echo "or import .cursor-plugin/marketplace.json as a team marketplace."
