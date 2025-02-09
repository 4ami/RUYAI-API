"""user-migration

Revision ID: 6d5b3262f9bd
Revises: f72d4fce3e74
Create Date: 2025-02-08 09:16:13.265101

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d5b3262f9bd'
down_revision: Union[str, None] = 'f72d4fce3e74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'USER',
        sa.Column(name='_id', type_=sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(name='full_name', type_=sa.String(75), nullable=False),
        sa.Column(name='email', type_=sa.String(150), nullable=False, unique=True),
        sa.Column(name='password', type_=sa.String(64), nullable=False),
        sa.Column(name='salt', type_=sa.String(128), nullable=False),
        sa.Column(name='role', type_=sa.Integer(), nullable=True)
    )

    op.create_foreign_key(
        constraint_name=None,
        source_table='USER',
        referent_table='ROLE',
        local_cols=['role'],
        remote_cols=['_id'],
        ondelete='SET NULL',
        onupdate='CASCADE'
    )


def downgrade() -> None:
    op.drop_table('USER')
