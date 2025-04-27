from pydantic import BaseModel, Field
from typing import Optional

class UserInformationForAdmin(BaseModel):
    full_name:Optional[str] = Field(
        default=None
    )
    role:Optional[int] = Field(
        default=None
    )
    account_status:str
