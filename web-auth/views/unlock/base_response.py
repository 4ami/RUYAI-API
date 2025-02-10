from pydantic import Field, BaseModel

class UnLockBaseResponse(BaseModel):
    code:int=Field(
        ...,
        title='Response Status Code',
        description='Protocol status code associated with response',
        strict=True
    )
    message:str=Field(
        ...,
        title='Response Message',
        description='Illustration meesage for the response state.',
        strict=True
    )