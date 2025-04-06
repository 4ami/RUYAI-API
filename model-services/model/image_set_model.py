from .base_model import BaseModel
from sqlalchemy import BigInteger, UUID, String, Enum, text
from sqlalchemy.orm import mapped_column, Mapped

class ImageSetModel(BaseModel):
    __tablename__='IMAGE_SET'
    _id:Mapped[int]=mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name:Mapped[UUID]=mapped_column(UUID, nullable=False, unique=True, server_default=text('gen_random_uuid()'))
    path:Mapped[str]=mapped_column(String, nullable=False)
    extension:Mapped[str]=mapped_column(String(3), nullable=False)
    approval_status:Mapped[str]=mapped_column(Enum('PENDING', 'APPROVED', 'REJECTED', name='approval_status'), nullable=False, server_default='PENDING')
    belongs_to:Mapped[int]=mapped_column(BigInteger, nullable=False)
    request_by:Mapped[int]=mapped_column(BigInteger, nullable=False)