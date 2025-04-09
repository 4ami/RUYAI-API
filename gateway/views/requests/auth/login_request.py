from ..base_request import BaseRequest
from pydantic import Field, EmailStr

class AuthLoginRequest(BaseRequest):
    email:EmailStr=Field(
        ...,
        title='User email',
        description='Registered user email',
        examples=['email@example.com'],
        strict=True
    )
    password:str=Field(
        ...,
        title='User Account Password',
        description='Password of user account made during registeration.',
        examples=['Secr3t_Pa$sw0rD'],
        strict=True
    )