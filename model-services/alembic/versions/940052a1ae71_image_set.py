"""image_set

Revision ID: 940052a1ae71
Revises: 73549fd8f722
Create Date: 2025-04-19 22:19:46.492596

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '940052a1ae71'
down_revision: Union[str, None] = '73549fd8f722'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'IMAGE_SET',
        sa.Column(name='_id', type_=sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column(name='name', type_=sa.UUID, nullable=False, unique=True),
        sa.Column(name='path', type_=sa.String(255), nullable=False),
        sa.Column(name='extension', type_=sa.String(5), nullable=False),
        sa.Column(name='glaucoma_diagnose', type_=sa.Enum('POSITIVE', 'NEGATIVE', name='glaucoma_diagnose'), nullable=False),
        sa.Column(name='glaucoma_confidence', type_=sa.NUMERIC(precision=11, scale=10), nullable=False),
        sa.Column(name='severity', type_=sa.Enum('MILD', 'MODERATE', 'SEVERE', 'NORMAL', name='severity'), nullable=False),
        sa.Column(name='report_id', type_=sa.BigInteger, nullable=True)
    )

    op.create_foreign_key(
        constraint_name=None,
        source_table='IMAGE_SET',
        referent_table='DIAGNOSE_REPORT',
        local_cols=['report_id'],
        remote_cols=['_id'],
        ondelete='SET NULL',
        onupdate='CASCADE'
    )


def downgrade() -> None:
    op.drop_table('IMAGE_SET')
    sa.Enum('POSITIVE', 'NEGATIVE', name='glaucoma_diagnose').drop(op.get_bind(), checkfirst=True)
    sa.Enum('MILD', 'MODERATE', 'SEVERE', 'NORMAL', name='severity').drop(op.get_bind(), checkfirst=True)