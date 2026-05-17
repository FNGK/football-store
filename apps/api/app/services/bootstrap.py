import re
import secrets

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.models import Tenant, User, UserRole
from app.security import hash_password


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug[:64] or "org"


async def bootstrap_admin(session: AsyncSession) -> None:
    if not settings.bootstrap_admin_email or not settings.bootstrap_admin_password:
        return
    email = settings.bootstrap_admin_email.lower()
    existing = await session.scalar(select(User).where(User.email == email))
    if existing is not None:
        return

    slug = slugify(settings.bootstrap_tenant_name)
    tenant = await session.scalar(select(Tenant).where(Tenant.slug == slug))
    if tenant is None:
        tenant = Tenant(slug=slug, name=settings.bootstrap_tenant_name)
        session.add(tenant)
        await session.flush()

    user = User(
        tenant_id=tenant.id,
        email=email,
        hashed_password=hash_password(settings.bootstrap_admin_password),
        role=UserRole.ADMIN,
    )
    session.add(user)
    await session.commit()


def generate_jwt_secret() -> str:
    return secrets.token_urlsafe(48)
