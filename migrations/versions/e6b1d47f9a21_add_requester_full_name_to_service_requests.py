"""Add requester_full_name to service requests

Revision ID: e6b1d47f9a21
Revises: bb8765a3f3c4
Create Date: 2026-04-07 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6b1d47f9a21'
down_revision = 'bb8765a3f3c4'
branch_labels = None
depends_on = None


def _build_full_name(first_name, surname, email):
    first = (first_name or '').strip()
    last = (surname or '').strip()
    full = f'{first} {last}'.strip()
    return full or email


def upgrade():
    with op.batch_alter_table('service_request', schema=None) as batch_op:
        batch_op.add_column(sa.Column('requester_full_name', sa.String(length=140), nullable=True))

    # Backfill existing records so DB exports show readable requester names.
    conn = op.get_bind()
    service_request = sa.table(
        'service_request',
        sa.column('id', sa.Integer),
        sa.column('user_id', sa.Integer),
        sa.column('requester_full_name', sa.String(length=140)),
    )
    user = sa.table(
        'user',
        sa.column('id', sa.Integer),
        sa.column('first_name', sa.String(length=64)),
        sa.column('surname', sa.String(length=64)),
        sa.column('email', sa.String(length=120)),
    )

    rows = conn.execute(
        sa.select(
            service_request.c.id,
            user.c.first_name,
            user.c.surname,
            user.c.email,
        ).select_from(
            service_request.join(user, service_request.c.user_id == user.c.id)
        )
    ).fetchall()

    for row in rows:
        conn.execute(
            service_request.update().where(service_request.c.id == row.id).values(
                requester_full_name=_build_full_name(row.first_name, row.surname, row.email)
            )
        )


def downgrade():
    with op.batch_alter_table('service_request', schema=None) as batch_op:
        batch_op.drop_column('requester_full_name')
