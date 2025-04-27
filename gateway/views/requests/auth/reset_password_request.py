from pydantic import Field, BaseModel

class ResetPasswordRequest(BaseModel):
    new_password:str=Field(
        ...,
        title='New Password'
    )