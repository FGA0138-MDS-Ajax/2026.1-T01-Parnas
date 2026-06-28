"""fix: adiciona campo is_active no model User

Revision ID: 72852b4102c3
Revises: 716cacea4b34
Create Date: 2026-06-25 21:21:17.690852

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72852b4102c3'
down_revision = '716cacea4b34'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()))


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('is_active')
