from pydantic import Field, EmailStr, BaseModel, model_validator
import json

class LockRequest(BaseModel):
    email:EmailStr|None=Field(
        None,
        title='User email',
        description='Registered user email',
        examples=['email@example.com'],
        strict=True
    )
    account_id:int|None=Field(
        None,
        title='Account Identifier',
        description='Identifier generated when user registered and it used to identify user',
        examples=['12135', '22351'],
        strict=True
    )

    @model_validator(mode='before')
    def at_least_one(cls, values):
        if type(json) is not str:
            values=json.loads(values)

        email, account_id=values.get('email'), values.get('account_id')
        if not email and not account_id:
            raise ValueError("Either 'email' or 'account_id' must be provided.")
        return values