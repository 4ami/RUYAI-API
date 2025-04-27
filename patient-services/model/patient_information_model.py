from .base import BaseModel
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BigInteger, Enum, String, DateTime, JSON
from datetime import datetime


class PatientInformationModel(BaseModel):
    __tablename__='PATIENT_INFORMATION'

    _id:Mapped[int]=mapped_column(BigInteger, primary_key=True, autoincrement=True)
    first_name:Mapped[str]=mapped_column(String, nullable=False)
    middle_name:Mapped[str]=mapped_column(String, nullable=False)
    last_name:Mapped[str]=mapped_column(String, nullable=False)
    birth_date:Mapped[datetime]=mapped_column(DateTime, nullable=False)
    gender:Mapped[str]=mapped_column(Enum('MALE','FEMALE', name='patient_gender_enum'), nullable=False)
    medical_history:Mapped[dict]=mapped_column(JSON, nullable=True)
    medical_staff_id:Mapped[int]=mapped_column(BigInteger, nullable=False)