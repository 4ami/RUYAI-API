"""diagnose_report

Revision ID: 73549fd8f722
Revises: 69286d982ada
Create Date: 2025-04-19 21:46:41.592672

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73549fd8f722'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'DIAGNOSE_REPORT',
        sa.Column(name='_id', type_=sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column(name='belongs_to', type_=sa.BigInteger, nullable=False),
        sa.Column(name='request_by', type_=sa.BigInteger, nullable=False),
        sa.Column(name='approval_status', type_=sa.Enum('PENDING', 'APPROVED', 'REJECTED', name='approval_status'), nullable=False, server_default='PENDING'),
        sa.Column(name='created_at', type_=sa.DATE, nullable=False, server_default=sa.text("CURRENT_TIMESTAMP"))
    )


def downgrade() -> None:
    op.drop_table('DIAGNOSE_REPORT')
    sa.Enum('PENDING', 'APPROVED', 'REJECTED', name='approval_status').drop(op.get_bind(), checkfirst=True)