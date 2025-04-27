from pydantic import Field, BaseModel

class RegisterResponseBase(BaseModel):
    code:int=Field(
        201,
        title='Response Status Code',
        description='Protocol status code associated with response',
        examples=[201, 500],
        strict=True
    )
    message:str=Field(
        'Registeration Success',
        title='Response Message',
        description='Illustration meesage for the response state.',
        examples=['Registeration Success', 'Registeration Failed'],
        strict=True
    )