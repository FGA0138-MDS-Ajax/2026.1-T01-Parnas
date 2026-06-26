"""chore: unifica historico de migrations da develop

Revision ID: 0d1cc55554da
Revises: 3c766b060c61, bfe04d60b618, d7a779e5f5b4
Create Date: 2026-06-25 20:30:33.441022

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d1cc55554da'
down_revision = ('3c766b060c61', 'bfe04d60b618', 'd7a779e5f5b4')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
