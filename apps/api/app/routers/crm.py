from uuid import UUID

from fastapi import APIRouter, status
from pydantic import BaseModel, Field

from app.db.models import ConversionSource, FeedbackCategory
from app.deps import DbSession, TenantId

router = APIRouter(prefix="/v1/crm", tags=["Master CRM"])


class ConsentConversionIn(BaseModel):
    gclid: str | None = None
    fbclid: str | None = None
    consent_ad_storage: str = Field(examples=["granted"])
    consent_analytics_storage: str = Field(examples=["denied"])
    source: ConversionSource = ConversionSource.OBSERVED
    value_usd: float | None = None


class ConsentConversionOut(BaseModel):
    id: UUID
    source: ConversionSource
    tenant_id: str


@router.post(
    "/conversions",
    response_model=ConsentConversionOut,
    status_code=status.HTTP_201_CREATED,
    summary="Ingest conversion with Consent Mode v2 labeling",
)
async def ingest_conversion(
    payload: ConsentConversionIn,
    tenant_id: TenantId,
    db: DbSession,
) -> ConsentConversionOut:
    from app.db.models import ConversionEvent

    event = ConversionEvent(
        tenant_id=tenant_id,
        gclid=payload.gclid,
        fbclid=payload.fbclid,
        consent_ad_storage=payload.consent_ad_storage,
        consent_analytics_storage=payload.consent_analytics_storage,
        source=payload.source,
        value_usd=str(payload.value_usd) if payload.value_usd is not None else None,
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return ConsentConversionOut(id=event.id, source=event.source, tenant_id=tenant_id)
