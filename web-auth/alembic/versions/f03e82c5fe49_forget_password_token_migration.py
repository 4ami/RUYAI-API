"""forget_password_token_migration

Revision ID: f03e82c5fe49
Revises: 131421949404
Create Date: 2025-04-27 00:05:28.063733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f03e82c5fe49'
down_revision: Union[str, None] = '131421949404'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'FORGET_PASSWORD_TOKEN',
        sa.Column(name='_id', type_=sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column(name='email', type_=sa.String(255), nullable=False, index=True),
        sa.Column(name='token', type_=sa.String(255), unique=True, index=True),
        sa.Column(name='exp', type_=sa.DateTime, nullable=False),
        sa.Column(name='created_at', type_=sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'))
    )


def downgrade() -> None:
    op.drop_table('FORGET_PASSWORD_TOKEN')
