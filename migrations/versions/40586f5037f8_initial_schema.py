"""Reset and combine migrations

Revision ID: 40586f5037f8
Create Date: 2025-08-25
"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# Required Alembic identifiers
revision = '40586f5037f8'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create service table with all fields from templates
    op.create_table('service',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(64), index=True),
        sa.Column('description', sa.Text()),
        sa.Column('category', sa.String(50), server_default='general', nullable=False),
        sa.Column('subcategory', sa.String(50), nullable=True),
        sa.Column('price', sa.Float()),
        sa.Column('is_available', sa.Boolean(), server_default='1'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create index on service name
    op.create_index('ix_service_name', 'service', ['name'])

    # Create service_request table with all fields from templates
    op.create_table('service_request',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('service_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(20), server_default='pending'),
        sa.Column('request_date', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('completion_date', sa.DateTime(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['service_id'], ['service.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    # Drop tables in correct order due to foreign key constraints
    op.drop_table('service_request')
    op.drop_index('ix_service_name', 'service')
    op.drop_table('service')