"""image_set

Revision ID: 69286d982ada
Revises: 
Create Date: 2025-03-06 22:05:24.661884

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69286d982ada'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'IMAGE_SET',
        sa.Column(name='_id', type_=sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column(name='name', type_=sa.UUID, nullable=False, unique=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column(name='path', type_=sa.String, nullable=False),
        sa.Column(name='extension', type_=sa.String(3), nullable=False),
        sa.Column(name='approval_status', type_=sa.Enum('PENDING', 'APPROVED', 'REJECTED', name='approval_status'), nullable=False, server_default='PENDING'),
        sa.Column(name='belongs_to', type_=sa.BigInteger, nullable=False),
        sa.Column(name='request_by', type_=sa.BigInteger, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('IMAGE_SET')
    sa.Enum('PENDING', 'APPROVED', 'REJECTED', name='approval_status').drop(op.get_bind(), checkfirst=True)
