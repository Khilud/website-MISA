"""Add employer worker requests table

Revision ID: f3b8a2c9d114
Revises: e6b1d47f9a21
Create Date: 2026-04-11 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3b8a2c9d114'
down_revision = 'a1c9d61bde44'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'employer_worker_request',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employer_name', sa.String(length=140), nullable=False),
        sa.Column('work_category', sa.String(length=120), nullable=False),
        sa.Column('work_type', sa.String(length=20), nullable=False),
        sa.Column('short_term_days', sa.Integer(), nullable=True),
        sa.Column('preferred_start_date', sa.Date(), nullable=True),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('phone_number', sa.String(length=30), nullable=False),
        sa.Column('address', sa.String(length=255), nullable=False),
        sa.Column('details', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('request_date', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_employer_worker_request_email'), 'employer_worker_request', ['email'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_employer_worker_request_email'), table_name='employer_worker_request')
    op.drop_table('employer_worker_request')
