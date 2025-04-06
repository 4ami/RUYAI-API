"""diagnose

Revision ID: 2f71e0d2ac83
Revises: 69286d982ada
Create Date: 2025-03-19 22:18:55.605609

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f71e0d2ac83'
down_revision: Union[str, None] = '69286d982ada'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'DIAGNOSE',
        sa.Column(name='_id', type_=sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column(name='glaucoma_diagnose', type_=sa.Enum('POSITIVE', 'NEGATIVE', name='glaucoma_diagnose'), nullable=False),
        sa.Column(name='severity', type_=sa.Enum('MILD', 'MODERATE', 'SEVERE', 'NEGATIVE', name='severity'), server_default='NEGATIVE', nullable=False),
    )


def downgrade() -> None:
    op.drop_column('DIAGNOSE')
    sa.Enum('POSITIVE', 'NEGATIVE', name='glaucoma_diagnose').drop(op.get_bind(), checkfirst=True)
    sa.Enum('MILD', 'MODERATE', 'SEVERE', 'NEGATIVE', name='severity').drop(op.get_bind(), checkfirst=True)
