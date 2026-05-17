import json
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import IdempotencyRecord


async def get_cached(
    db: AsyncSession, tenant_id: UUID, key: str
) -> tuple[int, dict] | None:
    row = await db.scalar(
        select(IdempotencyRecord).where(
            IdempotencyRecord.tenant_id == tenant_id,
            IdempotencyRecord.key == key,
        )
    )
    if row is None:
        return None
    return row.response_status, json.loads(row.response_body)


async def store(
    db: AsyncSession,
    tenant_id: UUID,
    key: str,
    status: int,
    body: dict,
) -> None:
    record = IdempotencyRecord(
        tenant_id=tenant_id,
        key=key,
        response_status=status,
        response_body=json.dumps(body),
    )
    db.add(record)
    await db.flush()
