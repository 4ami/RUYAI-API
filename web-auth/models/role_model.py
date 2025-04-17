from .base_model import BaseModel
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import mapped_column, Mapped


class RoleModel(BaseModel):
    __tablename__='ROLE'
    _id:Mapped[int]=mapped_column(BigInteger, primary_key=True, autoincrement=True)
    role:Mapped[str]=mapped_column(String(35), nullable=False, unique=True)