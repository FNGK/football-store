import app.bootstrap  # noqa: F401 — monorepo path setup

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import agents, crm, feedback, gateway, support


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Agentic Marketing Platform API",
    description="Master CRM and multi-tenant agent control plane",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crm.router)
app.include_router(support.router)
app.include_router(feedback.router)
app.include_router(agents.router)
app.include_router(gateway.router)


@app.get("/health", tags=["Health"], summary="Health check")
async def health() -> dict[str, str]:
    return {"status": "ok"}
