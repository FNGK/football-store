import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ConversionSource(str, enum.Enum):
    OBSERVED = "observed"
    MODELED = "modeled"


class FeedbackCategory(str, enum.Enum):
    BUG = "bug"
    FEATURE = "feature"
    STRATEGIC = "strategic"


class TenantScopedMixin:
    tenant_id: Mapped[str] = mapped_column(String(128), index=True, nullable=False)


class ConversionEvent(Base, TenantScopedMixin):
    __tablename__ = "conversion_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gclid: Mapped[str | None] = mapped_column(String(256))
    fbclid: Mapped[str | None] = mapped_column(String(256))
    consent_ad_storage: Mapped[str | None] = mapped_column(String(32))
    consent_analytics_storage: Mapped[str | None] = mapped_column(String(32))
    source: Mapped[ConversionSource] = mapped_column(
        Enum(ConversionSource), default=ConversionSource.OBSERVED
    )
    value_usd: Mapped[str | None] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class FeedbackTicket(Base, TenantScopedMixin):
    __tablename__ = "feedback_tickets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category: Mapped[FeedbackCategory] = mapped_column(Enum(FeedbackCategory))
    subject: Mapped[str] = mapped_column(String(512))
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class PiiTokenMapping(Base, TenantScopedMixin):
    __tablename__ = "pii_token_mappings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    ciphertext: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
