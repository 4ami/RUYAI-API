from .base_model import BaseModel
from sqlalchemy import BigInteger, String, Boolean
from sqlalchemy.orm import mapped_column, Mapped

class PrivilegeModel(BaseModel):
    __tablename__='PRIVILEGES'
    _id:Mapped[int]=mapped_column(BigInteger, primary_key=True, autoincrement=True)
    service:Mapped[str]=mapped_column(String(35), nullable=False)
    access:Mapped[bool]=mapped_column(Boolean, nullable=False, default=False)
    read:Mapped[bool]=mapped_column(Boolean, nullable=False, default=False)
    write:Mapped[bool]=mapped_column(Boolean, nullable=False, default=False)