"""Initial schema with RLS

Revision ID: 001
Revises:
Create Date: 2026-05-17

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE TYPE userrole AS ENUM ('admin', 'member')")
    op.execute("CREATE TYPE conversionsource AS ENUM ('observed', 'modeled')")
    op.execute("CREATE TYPE feedbackcategory AS ENUM ('bug', 'feature', 'strategic')")

    op.create_table(
        "tenants",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("slug", sa.String(64), nullable=False, unique=True),
        sa.Column("name", sa.String(256), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id", ondelete="CASCADE")),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("hashed_password", sa.String(256), nullable=False),
        sa.Column(
            "role",
            postgresql.ENUM("admin", "member", name="userrole", create_type=False),
            nullable=False,
        ),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("tenant_id", "email", name="uq_user_tenant_email"),
    )
    op.create_index("ix_users_tenant_id", "users", ["tenant_id"])
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "idempotency_keys",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id")),
        sa.Column("key", sa.String(128), nullable=False),
        sa.Column("response_status", sa.Integer(), nullable=False),
        sa.Column("response_body", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("tenant_id", "key", name="uq_idempotency_tenant_key"),
    )

    conversion_source = postgresql.ENUM(
        "observed", "modeled", name="conversionsource", create_type=False
    )
    feedback_category = postgresql.ENUM(
        "bug", "feature", "strategic", name="feedbackcategory", create_type=False
    )
    op.create_table(
        "conversion_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id")),
        sa.Column("gclid", sa.String(256)),
        sa.Column("fbclid", sa.String(256)),
        sa.Column("consent_ad_storage", sa.String(32)),
        sa.Column("consent_analytics_storage", sa.String(32)),
        sa.Column("source", conversion_source, server_default="observed"),
        sa.Column("value_usd", sa.String(32)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_conversion_events_tenant_id", "conversion_events", ["tenant_id"])

    op.create_table(
        "feedback_tickets",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("category", feedback_category, nullable=False),
        sa.Column("subject", sa.String(512), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_feedback_tickets_tenant_id", "feedback_tickets", ["tenant_id"])

    op.create_table(
        "pii_token_mappings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id")),
        sa.Column("token", sa.String(128), nullable=False, unique=True),
        sa.Column("ciphertext", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_pii_token_mappings_tenant_id", "pii_token_mappings", ["tenant_id"])

    for table in ("conversion_events", "feedback_tickets", "pii_token_mappings", "idempotency_keys"):
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
        op.execute(f"""
            CREATE POLICY tenant_isolation_{table} ON {table}
            USING (tenant_id::text = current_setting('app.current_tenant_id', true))
            WITH CHECK (tenant_id::text = current_setting('app.current_tenant_id', true))
        """)


def downgrade() -> None:
    for table in ("conversion_events", "feedback_tickets", "pii_token_mappings", "idempotency_keys"):
        op.execute(f"DROP POLICY IF EXISTS tenant_isolation_{table} ON {table}")
    op.drop_table("pii_token_mappings")
    op.drop_table("feedback_tickets")
    op.drop_table("conversion_events")
    op.drop_table("idempotency_keys")
    op.drop_table("users")
    op.drop_table("tenants")
    op.execute("DROP TYPE IF EXISTS feedbackcategory")
    op.execute("DROP TYPE IF EXISTS conversionsource")
    op.execute("DROP TYPE IF EXISTS userrole")
