from pydantic import Field, BaseModel, EmailStr

class ForgetPasswordRequest(BaseModel):
    email:EmailStr=Field(
        ...,
        title='Registered Email'
    )