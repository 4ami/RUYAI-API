from .base_model import BaseModel
from sqlalchemy import BigInteger, Enum
from sqlalchemy.orm import mapped_column, Mapped

class DiagnoseModel(BaseModel):
    __tablename__='DIAGNOSE'
    _id:Mapped[int]=mapped_column(BigInteger, primary_key=True, autoincrement=True)
    glaucoma_diagnose:Mapped[str]=mapped_column(Enum('POSITIVE', 'NEGATIVE', name='glaucoma_diagnose'), nullable=False)
    severity:Mapped[str]=mapped_column(Enum('MILD', 'MODERATE', 'SEVERE', 'NEGATIVE', name='severity'), nullable=False, server_default='NEGATIVE')