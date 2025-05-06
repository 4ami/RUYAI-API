from .base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, DateTime, String, text
from datetime import datetime
from pytz import timezone

class ForgetPasswordTokenModel(BaseModel):
    __tablename__="FORGET_PASSWORD_TOKEN"

    _id:Mapped[int]=mapped_column(BigInteger, primary_key=True, autoincrement=True)
    email:Mapped[str]=mapped_column(String, nullable=False, index=True)
    token:Mapped[str]=mapped_column(String, unique=True, index=True)
    exp:Mapped[datetime]=mapped_column(DateTime, nullable=False)
    created_at:Mapped[datetime]=mapped_column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    def is_expired(self):
        return self.exp < datetime.now()