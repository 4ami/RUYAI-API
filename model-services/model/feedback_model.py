from .base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Text, ForeignKey, NUMERIC, CheckConstraint, DATE, text
from datetime import date

class FeedbackModel(BaseModel):
    __tablename__='FEEDBACK'

    __table_args__=(
        CheckConstraint('rate >= 0 AND rate <= 10'),
    )
    
    _id:Mapped[int]=mapped_column(BigInteger, primary_key=True, autoincrement=True)
    rate:Mapped[float]=mapped_column(NUMERIC(precision=3, scale=1), nullable=False)
    comment:Mapped[str]=mapped_column(Text, nullable= False)
    report:Mapped[int]=mapped_column(BigInteger, ForeignKey('DIAGNOSE_REPORT._id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    submitted_at:Mapped[date]=mapped_column(DATE, nullable=False, server_default=text("CURRENT_DATE"))