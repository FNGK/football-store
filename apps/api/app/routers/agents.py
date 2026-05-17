from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel, Field

from app.deps import TenantId

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
async def agent_status(tenant_id: TenantId) -> dict:
    return {
        "tenant_id": tenant_id,
        "orchestrator": "langgraph",
        "creative_crew": "crewai",
        "mode": "normal",
    }


@router.post(
    "/guardrails",
    response_model=GuardrailsOut,
    summary="Configure MVG guardrails for tenant session",
)
async def configure_guardrails(
    payload: GuardrailsIn,
    tenant_id: TenantId,
) -> GuardrailsOut:
    from amp_agents.graph import checkpoint_thread_id

    thread = checkpoint_thread_id(tenant_id, "default")
    return GuardrailsOut(tenant_id=tenant_id, mode="normal", thread_id=thread)


@router.post(
    "/workflows/run",
    response_model=RunWorkflowOut,
    summary="Run intake LangGraph workflow",
)
async def run_workflow(
    payload: RunWorkflowIn,
    tenant_id: TenantId,
    idempotency_key: str | None = Header(default=None),
) -> RunWorkflowOut:
    if not idempotency_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Idempotency-Key header required for agent runs",
        )
    from amp_agents.graph import compile_orchestrator

    graph = compile_orchestrator()
    result = graph.invoke(
        {
            "tenant_id": tenant_id,
            "messages": [{"role": "user", "content": payload.message}],
            "brief": "",
            "safe_mode": False,
            "guardrails": {},
        }
    )
    return RunWorkflowOut(brief=result.get("brief", ""), guardrails=result.get("guardrails", {}))
