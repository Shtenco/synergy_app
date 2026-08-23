"""SINERGY SMM v1.2 functional core
Revision ID: 0002_v12
Revises: 0001_core
"""
from alembic import op
import sqlalchemy as sa
revision="0002_v12"; down_revision="0001_core"; branch_labels=None; depends_on=None

def upgrade():
    op.add_column("messages",sa.Column("external_message_id",sa.String(length=255),nullable=False,server_default=""))
    op.add_column("messages",sa.Column("ai_draft",sa.Text(),nullable=False,server_default=""))
    op.create_unique_constraint("uq_messages_conversation_external","messages",["conversation_id","external_message_id"])
    op.create_table("publication_deliveries",
        sa.Column("id",sa.String(length=36),primary_key=True),
        sa.Column("content_id",sa.String(length=36),sa.ForeignKey("content_items.id"),nullable=False),
        sa.Column("social_account_id",sa.String(length=36),sa.ForeignKey("social_accounts.id"),nullable=False),
        sa.Column("idempotency_key",sa.String(length=180),nullable=False,unique=True),
        sa.Column("status",sa.String(length=32),nullable=False,server_default="queued"),
        sa.Column("attempts",sa.Integer(),nullable=False,server_default="0"),
        sa.Column("external_post_id",sa.String(length=255),nullable=False,server_default=""),
        sa.Column("last_error",sa.Text(),nullable=False,server_default=""),
        sa.Column("created_at",sa.DateTime(),nullable=False,server_default=sa.func.now()),
        sa.Column("updated_at",sa.DateTime(),nullable=False,server_default=sa.func.now()))
    op.create_index("ix_publication_deliveries_content_id","publication_deliveries",["content_id"])
    op.create_index("ix_publication_deliveries_social_account_id","publication_deliveries",["social_account_id"])
    op.create_index("ix_publication_deliveries_idempotency_key","publication_deliveries",["idempotency_key"],unique=True)
    op.create_index("ix_publication_deliveries_status","publication_deliveries",["status"])

def downgrade():
    op.drop_index("ix_publication_deliveries_status",table_name="publication_deliveries")
    op.drop_index("ix_publication_deliveries_idempotency_key",table_name="publication_deliveries")
    op.drop_index("ix_publication_deliveries_social_account_id",table_name="publication_deliveries")
    op.drop_index("ix_publication_deliveries_content_id",table_name="publication_deliveries")
    op.drop_table("publication_deliveries")
    op.drop_constraint("uq_messages_conversation_external","messages",type_="unique")
    op.drop_column("messages","ai_draft"); op.drop_column("messages","external_message_id")
