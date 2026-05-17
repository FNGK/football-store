import logging
import os
import subprocess
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import app.bootstrap  # noqa: F401

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from sqlalchemy import text
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.config import settings
from app.db.session import SessionLocal, engine
from app.routers import agents, auth, crm, feedback, gateway, support
from app.services.bootstrap import bootstrap_admin

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("amp.api")

limiter = Limiter(key_func=get_remote_address, default_limits=[f"{settings.rate_limit_per_minute}/minute"])


def run_migrations() -> None:
    api_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=api_root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        logger.error("Migration failed: %s", result.stderr)
        if settings.is_production:
            raise RuntimeError("Database migration failed")
    else:
        logger.info("Migrations applied")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("SKIP_APP_LIFESPAN") != "1":
        run_migrations()
        async with SessionLocal() as session:
            await bootstrap_admin(session)
    yield
    if os.getenv("SKIP_APP_LIFESPAN") != "1":
        await engine.dispose()


app = FastAPI(
    title="Agentic Marketing Platform API",
    description="Master CRM and multi-tenant agent control plane",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

if settings.is_production:
    hosts = [h.strip() for h in settings.allowed_hosts.split(",") if h.strip()]
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=hosts)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(crm.router)
app.include_router(support.router)
app.include_router(feedback.router)
app.include_router(agents.router)
app.include_router(gateway.router)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    if settings.is_production:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


@app.get("/health", tags=["Health"], summary="Health check with dependency probes")
@limiter.limit("60/minute")
async def health(request: Request) -> JSONResponse:
    checks: dict[str, str] = {"api": "ok"}
    status_code = 200
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception as exc:
        checks["database"] = f"error: {exc}"
        status_code = 503
    return JSONResponse(content={"status": "ok" if status_code == 200 else "degraded", "checks": checks}, status_code=status_code)
