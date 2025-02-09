from .base_model import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class PrivilegeModel(BaseModel):
    __tablename__='PRIVILEGES'
    _id=Column(Integer, primary_key=True, autoincrement=True)
    service=Column(String(35), nullable=False)
    access=Column(Boolean, nullable=False, default=False)
    read=Column(Boolean, nullable=False, default=False)
    write=Column(Boolean, nullable=False, default=False)
    role=Column(Integer, ForeignKey('ROLE._id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)