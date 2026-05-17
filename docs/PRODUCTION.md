# Production deployment

## Prerequisites (you must provide)

| Secret | Description |
|--------|-------------|
| `POSTGRES_PASSWORD` | Strong database password |
| `JWT_SECRET_KEY` | Min 32 chars (`scripts/generate-env.sh` generates locally) |
| `BOOTSTRAP_ADMIN_PASSWORD` | Change default before go-live |
| `CORS_ORIGINS` | Your real dashboard URL(s), comma-separated |
| `ALLOWED_HOSTS` | API hostnames for TrustedHostMiddleware |
| `PUBLIC_API_URL` | Browser-reachable API URL for Next.js |

Optional: `OPENAI_API_KEY`, `SENTRY_DSN`, BigQuery credentials, AWS credentials for Firecracker hosts.

## Deploy with Docker Compose

```bash
./scripts/generate-env.sh apps/api/.env
# Edit apps/api/.env — set ENVIRONMENT=production, strong passwords, CORS, ALLOWED_HOSTS

export POSTGRES_PASSWORD='your-strong-password'
export PUBLIC_API_URL='https://api.yourdomain.com'

docker compose -f docker-compose.prod.yml up -d --build
```

## Default login (change immediately)

After first boot, if bootstrap env is set:

- Email: value of `BOOTSTRAP_ADMIN_EMAIL`
- Password: value of `BOOTSTRAP_ADMIN_PASSWORD`

## Health checks

- API: `GET /health` (includes database probe)
- Web: port 3000

## Not included in this release

Live Meta/Google Ads API warm-up, production Firecracker fleet, full T5 NER pipeline, and SOC2 audit require additional infrastructure work beyond this stack.
