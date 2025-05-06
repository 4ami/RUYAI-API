from .base_model import BaseModel
from sqlalchemy import BigInteger, String, ForeignKey, Boolean, DateTime, text, Enum
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime

class UserModel(BaseModel):
    __tablename__='USER'
    
    _id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(75), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    salt: Mapped[str] = mapped_column(String(128), nullable=False)
    role: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('ROLE._id', ondelete='SET NULL', onupdate='CASCADE'), nullable=True)
    account_status: Mapped[str] = mapped_column(Enum('PENDING', 'ACTIVE', 'DISABLED', name='account_status'), nullable=False, default='PENDING')
    locked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    locked_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=text("CONVERT_TZ(NOW(), 'UTC', 'Asia/Riyadh')"))