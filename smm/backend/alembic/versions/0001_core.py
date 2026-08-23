"""SINERGY SMM core schema
Revision ID: 0001_core
"""
from alembic import op
from app.database import Base
from app.domain import models

revision="0001_core"
down_revision=None
branch_labels=None
depends_on=None

def upgrade():
    Base.metadata.create_all(bind=op.get_bind())

def downgrade():
    Base.metadata.drop_all(bind=op.get_bind())
