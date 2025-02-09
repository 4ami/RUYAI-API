"""role-migration

Revision ID: 391ad3a0685e
Revises: 
Create Date: 2025-02-08 09:15:47.499695

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import os
import json
from dotenv import load_dotenv
load_dotenv()


# revision identifiers, used by Alembic.
revision: str = '391ad3a0685e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    cols:list[sa.Column]=[
        sa.Column(name='_id', type_=sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(name='role', type_=sa.String(35), nullable=False, unique=True)
    ]

    op.create_table(
        'ROLE',
        sa.Column(name='_id', type_=sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(name='role', type_=sa.String(35), nullable=False, unique=True)
    )

    if os.getenv('ENV').lower() == 'development':
        with open('alembic/seeder/roles.json', 'r') as seed:
            seeder=json.load(seed)
        roles=sa.Table('ROLE', sa.MetaData(),*cols)
        op.bulk_insert(table=roles, rows=seeder)


def downgrade() -> None:
    op.drop_table('ROLE')
