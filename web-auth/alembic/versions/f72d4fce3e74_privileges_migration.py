"""privileges-migration

Revision ID: f72d4fce3e74
Revises: 391ad3a0685e
Create Date: 2025-02-08 09:16:11.312427

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


import os
import json
from dotenv import load_dotenv
load_dotenv()

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
    )

    cols:list[sa.Column]=[
        sa.Column(name='_id', type_=sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(name='service', type_=sa.String(35), nullable=False),
        sa.Column(name='access', type_=sa.Boolean(), default=False, nullable=False),
        sa.Column(name='read', type_=sa.Boolean(), default=False, nullable=False),
        sa.Column(name='write', type_=sa.Boolean(), default=False, nullable=False),
    ]

    if os.getenv('ENV').lower() == 'development':
        with open('alembic/seeder/privileges.json', 'r') as seed:
            seeder=json.load(seed)
        roles=sa.Table('PRIVILEGES', sa.MetaData(),*cols)
        op.bulk_insert(table=roles, rows=seeder)


def downgrade() -> None:
    op.drop_table('PRIVILEGES')
