"""patients_information

Revision ID: b07e68b53995
Revises: 
Create Date: 2025-03-18 01:11:47.655109

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b07e68b53995'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# TODO: add relation with hospital id
def upgrade() -> None:
    op.create_table(
        'PATIENT_INFORMATION',
        sa.Column(name='_id', type_=sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column(name='first_name', type_=sa.String, nullable=False),
        sa.Column(name='middle_name', type_=sa.String, nullable=False),
        sa.Column(name='last_name', type_=sa.String, nullable=False),
        sa.Column(name='birth_date', type_=sa.DateTime, nullable=False),
        sa.Column(name='gender', type_=sa.Enum('MALE','FEMALE', name='patient_gender_enum'), nullable=False),
        sa.Column(name='medical_history', type_=sa.JSON, nullable=True),
        sa.Column(name='medical_staff_id', type_=sa.BigInteger, nullable=False)
    )


def downgrade() -> None:
    op.drop_table('PATIENT_INFORMATION')
    sa.Enum('MALE','FEMALE', name='patient_gender_enum').drop(op.get_bind(),checkfirst=True)
