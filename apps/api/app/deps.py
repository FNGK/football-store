from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.session import get_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_session():
        yield session


def get_tenant_id(x_tenant_id: Annotated[str | None, Header()] = None) -> str:
    tenant = x_tenant_id or settings.default_tenant_id
    if not tenant or len(tenant) > 128:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Valid X-Tenant-Id header required",
        )
    return tenant


TenantId = Annotated[str, Depends(get_tenant_id)]
DbSession = Annotated[AsyncSession, Depends(get_db)]
