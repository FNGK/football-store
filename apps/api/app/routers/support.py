from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.deps import TenantId

router = APIRouter(prefix="/v1", tags=["Support"])

DOCS_SNIPPETS = {
    "monitor": "Monitor LangGraph workflows via GET /v1/agents/status. Safe Mode activates on MVG breach.",
    "budget": "Configure minimum liquidity and token caps via POST /v1/agents/guardrails.",
    "plan": "Edit Interactive Plans in the dashboard; use Undo before Approve.",
}

REDIRECT_KEYWORDS = ("bug", "feature", "strategic", "roadmap", "partnership", "broken")


class SupportChatIn(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class SupportChatOut(BaseModel):
    reply: str = ""
    redirect_to_feedback: bool = False


@router.post(
    "/support/chat",
    response_model=SupportChatOut,
    summary="Documentation-only support agent",
)
async def support_chat(payload: SupportChatIn, tenant_id: TenantId) -> SupportChatOut:
    lower = payload.message.lower()
    if any(k in lower for k in REDIRECT_KEYWORDS):
        return SupportChatOut(redirect_to_feedback=True)

    for key, snippet in DOCS_SNIPPETS.items():
        if key in lower:
            return SupportChatOut(reply=snippet)

    return SupportChatOut(
        reply=(
            f"Tenant {tenant_id}: I can help with monitoring agents, budget parameters, "
            "and control surfaces. Try asking about 'monitor', 'budget', or 'plan'."
        )
    )
