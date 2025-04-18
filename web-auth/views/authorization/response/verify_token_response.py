from pydantic import BaseModel, Field
from typing import Optional

class VerifyTokenResponse(BaseModel):
    code:int=Field(
        ...,
        title='Response Status Code'
    )
    message:str=Field(
        ...,
        title='Response message'
    )
    valid:bool=Field(
        ...,
        title='Token Validity'
    )
    id:Optional[int]=Field(
        default=None,
        title='User ID'
    )
    full_name:Optional[str]=Field(
        default=None,
        title='User Full Name'
    )
    role:Optional[int]=Field(
        default=None,
        title='User Role'
    )