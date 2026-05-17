import json

from fastapi import APIRouter, Header, HTTPException, Response, status
from pydantic import BaseModel, Field

from app.config import settings
from app.deps import Auth, DbSession
from app.services.idempotency import get_cached, store

router = APIRouter(prefix="/v1/agents", tags=["Agents"])


class GuardrailsIn(BaseModel):
    max_input_tokens: int = Field(default=100_000, ge=1000)
    max_output_tokens: int = Field(default=50_000, ge=1000)
    max_tool_calls: int = Field(default=50, ge=1)


class GuardrailsOut(BaseModel):
    tenant_id: str
    mode: str
    thread_id: str


class RunWorkflowIn(BaseModel):
    message: str = Field(min_length=1)


class RunWorkflowOut(BaseModel):
    brief: str
    guardrails: dict


@router.get("/status", summary="Agent workflow status for tenant")
async def agent_status(auth: Auth) -> dict:
    return {
        "tenant_id": str(auth.tenant_id),
        "tenant_slug": auth.tenant_slug,
        "orchestrator": "langgraph",
        "creative_crew": "crewai",
        "mode": "normal",
        "agents_enabled": settings.agents_enabled,
    }


@router.post(
    "/guardrails",
    response_model=GuardrailsOut,
    summary="Configure MVG guardrails for tenant session",
)
async def configure_guardrails(payload: GuardrailsIn, auth: Auth) -> GuardrailsOut:
    from amp_agents.graph import checkpoint_thread_id

    thread = checkpoint_thread_id(str(auth.tenant_id), "default")
    return GuardrailsOut(
        tenant_id=str(auth.tenant_id),
        mode="normal",
        thread_id=thread,
    )


@router.post(
    "/workflows/run",
    response_model=RunWorkflowOut,
    summary="Run intake LangGraph workflow",
)
async def run_workflow(
    payload: RunWorkflowIn,
    auth: Auth,
    db: DbSession,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> Response:
    if not idempotency_key or len(idempotency_key) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Idempotency-Key header required (min 8 chars)",
        )

    cached = await get_cached(db, auth.tenant_id, idempotency_key)
    if cached is not None:
        status_code, body = cached
        return Response(
            content=json.dumps(body),
            media_type="application/json",
            status_code=status_code,
            headers={"X-Idempotent-Replay": "true"},
        )

    if not settings.agents_enabled:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Agents disabled",
        )

    try:
        from amp_agents.graph import compile_orchestrator

        graph = compile_orchestrator()
        result = graph.invoke(
            {
                "tenant_id": str(auth.tenant_id),
                "messages": [{"role": "user", "content": payload.message}],
                "brief": "",
                "safe_mode": False,
                "guardrails": {},
            }
        )
        out = RunWorkflowOut(
            brief=result.get("brief", ""),
            guardrails=result.get("guardrails", {}),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Workflow execution failed",
        ) from exc

    body = out.model_dump()
    await store(db, auth.tenant_id, idempotency_key, 200, body)
    return Response(content=json.dumps(body), media_type="application/json", status_code=200)
