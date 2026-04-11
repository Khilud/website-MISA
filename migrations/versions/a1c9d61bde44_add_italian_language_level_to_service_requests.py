"""Add italian_language_level to service requests

Revision ID: a1c9d61bde44
Revises: e6b1d47f9a21
Create Date: 2026-04-07 00:00:01.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1c9d61bde44'
down_revision = 'e6b1d47f9a21'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('service_request', schema=None) as batch_op:
        batch_op.add_column(sa.Column('italian_language_level', sa.String(length=20), nullable=True))


def downgrade():
    with op.batch_alter_table('service_request', schema=None) as batch_op:
        batch_op.drop_column('italian_language_level')
