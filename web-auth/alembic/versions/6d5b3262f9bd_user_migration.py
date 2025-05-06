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
        sa.Column(name='_id', type_=sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(name='full_name', type_=sa.String(75), nullable=False),
        sa.Column(name='email', type_=sa.String(150), nullable=False, unique=True),
        sa.Column(name='password', type_=sa.String(64), nullable=False),
        sa.Column(name='salt', type_=sa.String(128), nullable=False),
        sa.Column(name='role', type_=sa.BigInteger(), nullable=True),
        sa.Column(name='account_status', type_=sa.Enum('PENDING', 'ACTIVE', 'DISABLED', name='account_status'), nullable=False, default='PENDING'),
        sa.Column(name='locked', type_=sa.Boolean(), nullable=False, default=False),
        sa.Column(name='locked_at', type_=sa.DateTime(), nullable=True),
        sa.Column(name='created_at', type_=sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP"))
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

    op.execute("""
    CREATE TRIGGER set_locked_at
    BEFORE UPDATE ON `USER`
    FOR EACH ROW
    BEGIN
        IF NEW.locked = TRUE AND OLD.locked = FALSE THEN
            SET NEW.locked_at = CURRENT_TIMESTAMP;
        END IF;
    END
    """)


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS set_locked_at;")
    op.drop_table('USER')
