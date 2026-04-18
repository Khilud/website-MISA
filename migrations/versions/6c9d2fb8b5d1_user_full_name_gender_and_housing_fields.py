"""Add full name, gender, and housing fields

Revision ID: 6c9d2fb8b5d1
Revises: e6b1d47f9a21
Create Date: 2026-04-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c9d2fb8b5d1'
down_revision = 'e6b1d47f9a21'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('full_name', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('gender', sa.String(length=30), nullable=True))

    conn = op.get_bind()
    user_table = sa.table(
        'user',
        sa.column('id', sa.Integer),
        sa.column('username', sa.String(length=64)),
        sa.column('first_name', sa.String(length=64)),
        sa.column('surname', sa.String(length=64)),
        sa.column('email', sa.String(length=120)),
        sa.column('full_name', sa.String(length=120)),
    )

    rows = conn.execute(
        sa.select(
            user_table.c.id,
            user_table.c.username,
            user_table.c.first_name,
            user_table.c.surname,
            user_table.c.email,
        )
    ).fetchall()

    for row in rows:
        first = (row.first_name or '').strip()
        last = (row.surname or '').strip()
        full_name = f'{first} {last}'.strip() or row.email or row.username or f'User {row.id}'
        conn.execute(
            user_table.update().where(user_table.c.id == row.id).values(full_name=full_name)
        )

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('full_name', existing_type=sa.String(length=120), nullable=False)
        batch_op.drop_column('surname')
        batch_op.drop_column('first_name')

    with op.batch_alter_table('service_request', schema=None) as batch_op:
        batch_op.add_column(sa.Column('housing_room_type', sa.String(length=60), nullable=True))
        batch_op.add_column(sa.Column('housing_budget', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('housing_preferred_location', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('housing_duration', sa.String(length=80), nullable=True))


def downgrade():
    with op.batch_alter_table('service_request', schema=None) as batch_op:
        batch_op.drop_column('housing_duration')
        batch_op.drop_column('housing_preferred_location')
        batch_op.drop_column('housing_budget')
        batch_op.drop_column('housing_room_type')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('surname', sa.String(length=64), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('gender')
        batch_op.drop_column('full_name')