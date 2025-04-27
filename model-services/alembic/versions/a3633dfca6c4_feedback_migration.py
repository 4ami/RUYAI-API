"""feedback_migration

Revision ID: a3633dfca6c4
Revises: 940052a1ae71
Create Date: 2025-04-25 20:00:28.740264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3633dfca6c4'
down_revision: Union[str, None] = '940052a1ae71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'FEEDBACK',
        sa.Column(name='_id', type_=sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column(name='rate', type_=sa.NUMERIC(precision=3, scale=1), nullable=False),
        sa.Column(name='comment', type_=sa.Text, nullable=False),
        sa.Column(name='report', type_=sa.BigInteger, nullable=False),
        sa.Column(name='submitted_at', type_=sa.DATE, nullable=False, server_default=sa.text("CURRENT_DATE"))
    )

    op.create_check_constraint(
        constraint_name=None,
        table_name='FEEDBACK',
        condition='rate >= 0 AND rate <= 10'
    )


    op.create_foreign_key(
        constraint_name=None,
        source_table='FEEDBACK',
        referent_table='DIAGNOSE_REPORT',
        local_cols=['report'],
        remote_cols=['_id'],
        ondelete='CASCADE',
        onupdate='CASCADE'
    )


def downgrade() -> None:
    op.drop_table('FEEDBACK')
