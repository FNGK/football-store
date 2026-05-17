import os

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.deps import Auth, DbSession
from app.db.models import PiiTokenMapping

router = APIRouter(prefix="/v1/gateway", tags=["PII Gateway"])


class MaskIn(BaseModel):
    text: str = Field(min_length=1)


class MaskOut(BaseModel):
    masked_text: str
    token_count: int


@router.post("/mask", response_model=MaskOut, summary="Mask PII before LLM processing")
async def mask_pii(payload: MaskIn, auth: Auth, db: DbSession) -> MaskOut:
    from amp_gateway import PiiGateway

    key = os.environ.get("PII_FERNET_KEY", "").encode() or None
    gw = PiiGateway.from_key(key)
    masked, mappings = gw.mask_text(str(auth.tenant_id), payload.text)

    for token, ciphertext in mappings.items():
        db.add(
            PiiTokenMapping(
                tenant_id=auth.tenant_id,
                token=token,
                ciphertext=ciphertext,
            )
        )
    await db.flush()

    return MaskOut(masked_text=masked, token_count=len(mappings))
