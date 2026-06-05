"""cria tabela simulacao

Revision ID: 3c7b1d9a2f4e
Revises: a9d874f8a711
Create Date: 2026-06-05 20:55:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c7b1d9a2f4e'
down_revision = 'a9d874f8a711'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'simulation',
        sa.Column('id_simulacao', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('id_empresa', sa.Integer(), nullable=False),
        sa.Column('id_usuario', sa.Integer(), nullable=False),
        sa.Column('valor_solicitado', sa.Numeric(precision=14, scale=2), nullable=False),
        sa.Column('prazo_meses', sa.Integer(), nullable=False),
        sa.Column('modalidade', sa.String(length=10), nullable=False),
        sa.Column('taxa_juros', sa.Numeric(precision=8, scale=4), nullable=False),
        sa.Column('valor_parcela', sa.Numeric(precision=14, scale=2), nullable=False),
        sa.Column('valor_total', sa.Numeric(precision=14, scale=2), nullable=False),
        sa.Column('total_juros', sa.Numeric(precision=14, scale=2), nullable=False),
        sa.Column('data_simulacao', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['id_empresa'], ['company.company_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['id_usuario'], ['user.user_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id_simulacao')
    )


def downgrade():
    op.drop_table('simulation')
