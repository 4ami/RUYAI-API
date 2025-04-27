from .base_model import BaseModel
from sqlalchemy import BigInteger, UUID, String, Enum, NUMERIC, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from enum import Enum as en

class ImageSetModel(BaseModel):
    __tablename__='IMAGE_SET'
    _id:Mapped[int]=mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name:Mapped[UUID]=mapped_column(UUID, nullable=False, unique=True)
    path:Mapped[str]=mapped_column(String, nullable=False)
    extension:Mapped[str]=mapped_column(String(3), nullable=False)
    glaucoma_diagnose:Mapped[str]=mapped_column(Enum('POSITIVE', 'NEGATIVE', name='glaucoma_diagnose'), nullable=False)
    glaucoma_confidence:Mapped[float]=mapped_column(NUMERIC(precision=11, scale=10), nullable=False)
    severity:Mapped[str]=mapped_column(Enum('MILD', 'MODERATE', 'SEVERE', 'NORMAL', name='severity'), nullable=False)
    report_id:Mapped[int]=mapped_column(BigInteger, ForeignKey('DIAGNOSE_REPORT._id', ondelete='SET NULL', onupdate='CASCADE'), nullable=True)

class GlaucomaDiagnose(str, en):
    POSITIVE='POSITIVE'
    NEGATIVE='NEGATIVE'

class SevirityDiagnose(str, en):
    S0='NORMAL'
    S1='MILD'
    S2='MODERATE'
    S3='SEVERE'