"""Add category and subcategory to services

Revision ID: d13324638238
Revises: 40586f5037f8
Create Date: 2025-09-16 02:14:20.884174

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd13324638238'
down_revision = '40586f5037f8'
branch_labels = None
depends_on = None


def upgrade():
    # Add category and subcategory columns to service table
    with op.batch_alter_table('service', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category', sa.String(length=50), nullable=False, server_default='Documentation'))
        batch_op.add_column(sa.Column('subcategory', sa.String(length=50), nullable=True))


def downgrade():
    # Remove category and subcategory columns from service table
    with op.batch_alter_table('service', schema=None) as batch_op:
        batch_op.drop_column('subcategory')
        batch_op.drop_column('category')
