from ..base_request import BaseRequest
from pydantic import Field, EmailStr

class AuthLockRequest(BaseRequest):
    email:EmailStr=Field(
        None,
        title='User email',
        description='Registered user email',
        examples=['email@example.com'],
        strict=True
    )
    account_id:int=Field(
        None,
        title='Account Identifier',
        description='Identifier generated when user registered and it used to identify user',
        examples=['12135', '22351'],
        strict=True
    )