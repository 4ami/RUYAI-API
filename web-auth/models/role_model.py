from .base_model import BaseModel
from sqlalchemy import Column, Integer, String

class RoleModel(BaseModel):
    __tablename__='ROLE'
    _id=Column(Integer, primary_key=True, autoincrement=True)
    role=Column(String(35), nullable=False, unique=True)