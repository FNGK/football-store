#!/usr/bin/env bash
# Start web + API dev servers (run from repo root).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [ ! -f "$ROOT/apps/api/.env" ]; then
  "$ROOT/scripts/generate-env.sh" "$ROOT/apps/api/.env"
fi

start_web() {
  if curl -sf http://127.0.0.1:3000/ >/dev/null 2>&1; then
    echo "Web already running on http://localhost:3000"
    return
  fi
  echo "Starting Next.js on port 3000..."
  cd "$ROOT/apps/web"
  [ -f .env ] || cp .env.example .env
  [ -d node_modules ] || pnpm install
  nohup pnpm dev --hostname 0.0.0.0 > /tmp/amp-web.log 2>&1 &
  echo $! > /tmp/amp-web.pid
}

start_api() {
  if curl -sf http://127.0.0.1:8000/health >/dev/null 2>&1; then
    echo "API already running on http://localhost:8000"
    return
  fi
  echo "Starting API on port 8000..."
  cd "$ROOT/apps/api"
  [ -f .env ] || cp .env.example .env
  nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/amp-api.log 2>&1 &
  echo $! > /tmp/amp-api.pid
}

start_web
sleep 2
start_api
sleep 2

echo ""
echo "=== Servers ==="
curl -sf http://127.0.0.1:3000/ >/dev/null && echo "  Web:  http://localhost:3000  (OK)" || echo "  Web:  FAILED — see /tmp/amp-web.log"
curl -sf http://127.0.0.1:8000/health >/dev/null && echo "  API:  http://localhost:8000  (OK)" || echo "  API:  FAILED — see /tmp/amp-api.log"
echo ""
echo "In Cursor: open the PORTS panel and click the globe/link next to port 3000."
