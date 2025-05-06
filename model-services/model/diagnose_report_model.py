from .base_model import BaseModel
from sqlalchemy import BigInteger, Enum, DATE, text
from sqlalchemy.orm import mapped_column, Mapped
from datetime import date

class DiagnoseReportModel(BaseModel):
    __tablename__='DIAGNOSE_REPORT'
    _id:Mapped[int]=mapped_column(BigInteger, primary_key=True, autoincrement=True)
    belongs_to:Mapped[int]=mapped_column(BigInteger, nullable=False)
    request_by:Mapped[int]=mapped_column(BigInteger, nullable=False)
    approval_status:Mapped[str]=mapped_column(Enum('PENDING', 'APPROVED', 'REJECTED', name='approval_status'), nullable=False, server_default='PENDING')
    created_at:Mapped[date]=mapped_column(DATE, nullable=False, server_default=text("CURRENT_TIMESTAMP"))