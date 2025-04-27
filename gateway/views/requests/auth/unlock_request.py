from ..base_request import BaseRequest
from pydantic import Field, EmailStr, model_validator

class UnLockRequest(BaseRequest):
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

    @model_validator(mode='before')
    def at_least_one(cls, values):
        email, account_id=values.get('email'), values.get('account_id')
        if not email and not account_id:
            raise ValueError("Either 'email' or 'account_id' must be provided.")
        return values