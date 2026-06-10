"""fix(migrations): unifica heads divergentes para reconciliar histórico paralelo

Revision ID: 2cdc0e42feac
Revises: 3c766b060c61, d7a779e5f5b4
Create Date: 2026-06-10 19:55:28.387571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cdc0e42feac'
down_revision = ('3c766b060c61', 'd7a779e5f5b4')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
