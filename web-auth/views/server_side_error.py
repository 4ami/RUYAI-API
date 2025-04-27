from pydantic import Field, BaseModel


class ServerSideErrorResponse(BaseModel):
    code:int=Field(
        500,
        title='Response Status Code',
        description='Protocol status code associated with response',
        strict=True
    )
    message:str=Field(
        'Server-side error!',
        title='Response Message',
        description='Illustration meesage for the response state.',
        strict=True
    )