from collections.abc import AsyncGenerator
from contextvars import ContextVar
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings

current_tenant_id: ContextVar[UUID | None] = ContextVar("current_tenant_id", default=None)

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    pool_pre_ping=True,
)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def set_tenant_context(session: AsyncSession, tenant_id: UUID) -> None:
    """Set Postgres session variable for RLS policies."""
    await session.execute(
        text("SELECT set_config('app.current_tenant_id', :tid, true)"),
        {"tid": str(tenant_id)},
    )


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        tid = current_tenant_id.get()
        if tid is not None:
            await set_tenant_context(session, tid)
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
