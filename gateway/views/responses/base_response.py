from pydantic import BaseModel, Field

class BaseResponse(BaseModel):
    code:int=Field(
        ...,
        title='Response Status Code',
        description='Protocol status code associated with response',
        examples=[200, 404, 500],
        strict=True
    )
    message:str=Field(
        ...,
        title='Response Message',
        description='Illustration meesage for the response state.',
        examples=['Success', 'Failed'],
        strict=True
    )