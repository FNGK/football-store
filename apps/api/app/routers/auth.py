from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select

from app.db.models import Tenant, User
from app.deps import Auth, DbSession
from app.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)

router = APIRouter(prefix="/v1/auth", tags=["Authentication"])


class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    tenant_id: UUID
    tenant_slug: str


class RefreshIn(BaseModel):
    refresh_token: str


class MeOut(BaseModel):
    user_id: UUID
    email: str
    tenant_id: UUID
    tenant_slug: str
    role: str


@router.post("/login", response_model=TokenOut, summary="Authenticate and receive JWT tokens")
async def login(payload: LoginIn, db: DbSession) -> TokenOut:
    user = await db.scalar(
        select(User).where(User.email == payload.email.lower(), User.is_active.is_(True))
    )
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    tenant = await db.scalar(select(Tenant).where(Tenant.id == user.tenant_id, Tenant.is_active.is_(True)))
    if tenant is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tenant inactive")

    access = create_access_token(
        user_id=user.id,
        tenant_id=tenant.id,
        tenant_slug=tenant.slug,
        role=user.role.value,
        email=user.email,
    )
    refresh = create_refresh_token(user_id=user.id, tenant_id=tenant.id)
    return TokenOut(
        access_token=access,
        refresh_token=refresh,
        tenant_id=tenant.id,
        tenant_slug=tenant.slug,
    )


@router.post("/refresh", response_model=TokenOut, summary="Refresh access token")
async def refresh(payload: RefreshIn, db: DbSession) -> TokenOut:
    try:
        data = decode_token(payload.refresh_token)
        if data.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user_id = UUID(data["sub"])
        tenant_id = UUID(data["tenant_id"])
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token") from exc

    user = await db.scalar(select(User).where(User.id == user_id, User.is_active.is_(True)))
    tenant = await db.scalar(select(Tenant).where(Tenant.id == tenant_id, Tenant.is_active.is_(True)))
    if user is None or tenant is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access = create_access_token(
        user_id=user.id,
        tenant_id=tenant.id,
        tenant_slug=tenant.slug,
        role=user.role.value,
        email=user.email,
    )
    new_refresh = create_refresh_token(user_id=user.id, tenant_id=tenant.id)
    return TokenOut(
        access_token=access,
        refresh_token=new_refresh,
        tenant_id=tenant.id,
        tenant_slug=tenant.slug,
    )


@router.get("/me", response_model=MeOut, summary="Current authenticated user")
async def me(auth: Auth) -> MeOut:
    return MeOut(
        user_id=auth.user_id,
        email=auth.email,
        tenant_id=auth.tenant_id,
        tenant_slug=auth.tenant_slug,
        role=auth.role.value,
    )
