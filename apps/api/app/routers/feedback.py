import logging
from uuid import UUID

from fastapi import APIRouter, status
from pydantic import BaseModel, Field

from app.db.models import FeedbackCategory, FeedbackTicket
from app.deps import DbSession, TenantId

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1", tags=["Feedback"])


class FeedbackIn(BaseModel):
    category: str = Field(examples=["feature"])
    subject: str = Field(min_length=1, max_length=512)
    body: str = Field(min_length=1)


class FeedbackOut(BaseModel):
    id: UUID
    tenant_id: str
    alert_sent: bool = True


@router.post(
    "/feedback",
    response_model=FeedbackOut,
    status_code=status.HTTP_201_CREATED,
    summary="Log feedback to Master CRM and alert administrators",
)
async def submit_feedback(
    payload: FeedbackIn,
    tenant_id: TenantId,
    db: DbSession,
) -> FeedbackOut:
    category = FeedbackCategory(payload.category)
    ticket = FeedbackTicket(
        tenant_id=tenant_id,
        category=category,
        subject=payload.subject,
        body=payload.body,
    )
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    logger.warning(
        "ADMIN_ALERT tenant=%s category=%s subject=%s id=%s",
        tenant_id,
        category.value,
        payload.subject,
        ticket.id,
    )
    return FeedbackOut(id=ticket.id, tenant_id=tenant_id)
