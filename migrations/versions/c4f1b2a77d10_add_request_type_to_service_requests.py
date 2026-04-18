"""Add request_type to service requests

Revision ID: c4f1b2a77d10
Revises: 9a7c2d8e1f4b
Create Date: 2026-04-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4f1b2a77d10'
down_revision = '9a7c2d8e1f4b'
branch_labels = None
depends_on = None


def _map_category_to_type(category):
    mapping = {
        'Documentation': 'documentation',
        'Language': 'language',
        'Housing': 'housing',
        'Career': 'career',
        'Group Tour': 'tour',
    }
    return mapping.get((category or '').strip(), 'other')


def upgrade():
    with op.batch_alter_table('service_request', schema=None) as batch_op:
        batch_op.add_column(sa.Column('request_type', sa.String(length=20), nullable=True))

    conn = op.get_bind()
    service_request = sa.table(
        'service_request',
        sa.column('id', sa.Integer),
        sa.column('service_id', sa.Integer),
        sa.column('request_type', sa.String(length=20)),
    )
    service = sa.table(
        'service',
        sa.column('id', sa.Integer),
        sa.column('category', sa.String(length=50)),
    )

    rows = conn.execute(
        sa.select(
            service_request.c.id,
            service.c.category,
        ).select_from(
            service_request.outerjoin(service, service_request.c.service_id == service.c.id)
        )
    ).fetchall()

    for row in rows:
        conn.execute(
            service_request.update().where(service_request.c.id == row.id).values(
                request_type=_map_category_to_type(row.category)
            )
        )

    with op.batch_alter_table('service_request', schema=None) as batch_op:
        batch_op.alter_column('request_type', existing_type=sa.String(length=20), nullable=False)
        batch_op.create_index(batch_op.f('ix_service_request_request_type'), ['request_type'], unique=False)


def downgrade():
    with op.batch_alter_table('service_request', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_service_request_request_type'))
        batch_op.drop_column('request_type')
