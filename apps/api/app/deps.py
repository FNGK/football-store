from collections.abc import AsyncGenerator
from dataclasses import dataclass
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.models import Tenant, User, UserRole
from app.db.session import SessionLocal, current_tenant_id, get_session, set_tenant_context
from app.security import decode_token

bearer_scheme = HTTPBearer(auto_error=False)


@dataclass
class AuthContext:
    user_id: UUID
    tenant_id: UUID
    tenant_slug: str
    email: str
    role: UserRole


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_session():
        yield session


async def get_auth_context(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AuthContext:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = decode_token(credentials.credentials)
        if payload.get("type") != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        user_id = UUID(payload["sub"])
        tenant_id = UUID(payload["tenant_id"])
        tenant_slug = payload["tenant_slug"]
        email = payload["email"]
        role = UserRole(payload["role"])
    except (JWTError, KeyError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc

    user = await db.scalar(select(User).where(User.id == user_id, User.is_active.is_(True)))
    if user is None or user.tenant_id != tenant_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    tenant = await db.scalar(
        select(Tenant).where(Tenant.id == tenant_id, Tenant.is_active.is_(True))
    )
    if tenant is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tenant inactive")

    current_tenant_id.set(tenant_id)
    return AuthContext(
        user_id=user_id,
        tenant_id=tenant_id,
        tenant_slug=tenant_slug,
        email=email,
        role=role,
    )


async def require_admin(auth: Annotated[AuthContext, Depends(get_auth_context)]) -> AuthContext:
    if auth.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin required")
    return auth


DbSession = Annotated[AsyncSession, Depends(get_db)]
Auth = Annotated[AuthContext, Depends(get_auth_context)]
AdminAuth = Annotated[AuthContext, Depends(require_admin)]


async def check_idempotency(
    auth: Auth,
    db: DbSession,
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
) -> str | None:
    """Return cached response JSON if key exists; else return key for storage."""
    if idempotency_key is None:
        return None
    if len(idempotency_key) < 8 or len(idempotency_key) > 128:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Idempotency-Key")
    from app.db.models import IdempotencyRecord

    row = await db.scalar(
        select(IdempotencyRecord).where(
            IdempotencyRecord.tenant_id == auth.tenant_id,
            IdempotencyRecord.key == idempotency_key,
        )
    )
    if row is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Duplicate request",
            headers={"X-Idempotent-Replay": "true"},
        )
    return idempotency_key
