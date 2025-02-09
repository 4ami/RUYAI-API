from .base_model import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey

class UserModel(BaseModel):
    __tablename__='USER'
    _id=Column(Integer, primary_key=True, autoincrement=True)
    full_name=Column(String(75), nullable=False)
    email=Column(String(150), nullable=False, unique=True)
    password=Column(String(64), nullable=False)
    salt=Column(String(128), nullable=False)
    role=Column(Integer, ForeignKey('ROLE._id', ondelete='SET NULL', onupdate='CASCADE'), nullable=True)