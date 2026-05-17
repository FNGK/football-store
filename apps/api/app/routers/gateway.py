from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.deps import TenantId

router = APIRouter(prefix="/v1/gateway", tags=["PII Gateway"])


class MaskIn(BaseModel):
    text: str = Field(min_length=1)


class MaskOut(BaseModel):
    masked_text: str
    token_count: int


@router.post("/mask", response_model=MaskOut, summary="Mask PII before LLM processing")
async def mask_pii(payload: MaskIn, tenant_id: TenantId) -> MaskOut:
    from amp_gateway import PiiGateway

    gw = PiiGateway.from_key()
    masked, mappings = gw.mask_text(tenant_id, payload.text)
    return MaskOut(masked_text=masked, token_count=len(mappings))
