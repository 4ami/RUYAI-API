from pydantic import BaseModel, Field
from typing import Optional


class Role(BaseModel):
    id:int
    role:str

class AvailableRoles(BaseModel):
    code:int=Field(
        ...,
        title='Response Status Code',
        description='Protocol status code associated with response',
        strict=True
    )
    message:str=Field(
        ...,
        title='Response Message',
        description='Illustration meesage for the response state.',
        strict=True
    )
    roles:Optional[list[Role]]=Field(
        default= None,
        title='Allowed Roles',
        description='Roles to be used in register form'
    )