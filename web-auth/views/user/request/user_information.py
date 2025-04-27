from pydantic import BaseModel, Field
from typing import Optional

class UserInformationBase(BaseModel):
    full_name:Optional[str] = Field(
        default=None
    )

class AdminUseOfUserInformation(UserInformationBase):
    role:Optional[int] = Field(
        default=None
    )
    account_status:str

class UserUseOfUserInformation(UserInformationBase):
    email:Optional[str] = Field(
        default=None
    )
    password:Optional[str] = Field(
        default=None
    )