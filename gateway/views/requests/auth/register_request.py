from pydantic import Field, EmailStr
from ..base_request import BaseRequest

class AuthRegisterRequest(BaseRequest):
    full_name:str=Field(
        ...,
        title='User Full Name',
        description='User full name to be registered in the system. It will be used to represent user in the client side.',
        examples=['John Doe'],
        strict=True
    )
    email:EmailStr=Field(
        ...,
        title="User Email",
        description="User's valid email address for registration and communication.",
        examples=["user@example.com"],
        strict=True,
    )
    password:str=Field(
        ...,
        title='User Password',
        description='Secret phrase used by user to access his account later on the system.',
        examples=['Secr3t_Pa$sw0rD'],
        strict=True
    )
    role:int=Field(
        ...,
        title='Required Role',
        description='Wanted role to use the system',
        strict=True
    )