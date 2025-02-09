"""privileges-migration

Revision ID: f72d4fce3e74
Revises: 391ad3a0685e
Create Date: 2025-02-08 09:16:11.312427

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f72d4fce3e74'
down_revision: Union[str, None] = '391ad3a0685e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'PRIVILEGES',
        sa.Column(name='_id', type_=sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(name='service', type_=sa.String(35), nullable=False),
        sa.Column(name='access', type_=sa.Boolean(), default=False, nullable=False),
        sa.Column(name='read', type_=sa.Boolean(), default=False, nullable=False),
        sa.Column(name='write', type_=sa.Boolean(), default=False, nullable=False),
        sa.Column(name='role', type_=sa.Integer(), nullable=False)
    )

    op.create_foreign_key(
        constraint_name=None,
        source_table='PRIVILEGES',
        referent_table='ROLE',
        local_cols=['role'],
        remote_cols=['_id'],
        ondelete='CASCADE',
        onupdate='CASCADE'
    )


def downgrade() -> None:
    op.drop_table('PRIVILEGES')
