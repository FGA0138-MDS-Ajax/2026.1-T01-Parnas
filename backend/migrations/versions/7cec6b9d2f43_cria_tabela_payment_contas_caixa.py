"""Cria tabela payment contas caixa

Revision ID: 7cec6b9d2f43
Revises: 72852b4102c3
Create Date: 2026-06-29 13:09:12.819182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7cec6b9d2f43'
down_revision = '72852b4102c3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('payment',
    sa.Column('payment_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.company_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('payment_id'),
    sa.UniqueConstraint('name', 'company_id', name='_payment_name_company_uc')
    )

    with op.batch_alter_table('bill', schema=None) as batch_op:
        batch_op.add_column(sa.Column('payment_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_bill_payment', 'payment', ['payment_id'], ['payment_id'], ondelete='RESTRICT')

    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('payment_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_transaction_payment', 'payment', ['payment_id'], ['payment_id'], ondelete='RESTRICT')


def downgrade():
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.drop_constraint('fk_transaction_payment', type_='foreignkey')
        batch_op.drop_column('payment_id')

    with op.batch_alter_table('bill', schema=None) as batch_op:
        batch_op.drop_constraint('fk_bill_payment', type_='foreignkey')
        batch_op.drop_column('payment_id')

    op.drop_table('payment')