"""role-privilage-relationship

Revision ID: 131421949404
Revises: 6d5b3262f9bd
Create Date: 2025-02-10 10:34:04.600231

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


import os
import json
from dotenv import load_dotenv
load_dotenv()


# revision identifiers, used by Alembic.
revision: str = '131421949404'
down_revision: Union[str, None] = '6d5b3262f9bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'ROLE_PRIVILEGES',
        sa.Column(name='role', type_=sa.Integer(), nullable=False, primary_key=True),
        sa.Column(name='privilege', type_=sa.Integer(), nullable=False, primary_key=True)
    )
    # ROLE <-> ROLE_PRIVILEGES
    op.create_foreign_key(
        constraint_name=None,
        source_table='ROLE_PRIVILEGES',
        referent_table='ROLE',
        local_cols=['role'],
        remote_cols=['_id'],
        ondelete='CASCADE',
        onupdate='CASCADE'
    )

    # PRIVILEGES <-> ROLE_PRIVILEGES
    op.create_foreign_key(
        constraint_name=None,
        source_table='ROLE_PRIVILEGES',
        referent_table='PRIVILEGES',
        local_cols=['privilege'],
        remote_cols=['_id'],
        ondelete='CASCADE',
        onupdate='CASCADE'
    )

    cols:list[sa.Column]=[
        sa.Column(name='role', type_=sa.Integer(), nullable=False, primary_key=True),
        sa.Column(name='privilege', type_=sa.Integer(), nullable=False, primary_key=True)
    ]

    if os.getenv('ENV').lower() == 'development':
        with open('alembic/seeder/role-privileges.json', 'r') as seed:
            seeder=json.load(seed)
        roles=sa.Table('ROLE_PRIVILEGES', sa.MetaData(),*cols)
        op.bulk_insert(table=roles, rows=seeder)


def downgrade() -> None:
    op.drop_table('ROLE_PRIVILEGES')
