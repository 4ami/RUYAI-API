from .base_model import BaseModel
from sqlalchemy import Integer, String, ForeignKey, Boolean, DateTime, text
from sqlalchemy.orm import mapped_column, Mapped

class UserModel(BaseModel):
    __tablename__='USER'
    
    _id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(75), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    salt: Mapped[str] = mapped_column(String(128), nullable=False)
    role: Mapped[int | None] = mapped_column(Integer, ForeignKey('ROLE._id', ondelete='SET NULL', onupdate='CASCADE'), nullable=True)
    locked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    locked_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, server_default=text("timezone('Asia/Riyadh', now())"))