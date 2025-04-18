from pydantic import Field, BaseModel

class VerifyTokenRequest(BaseModel):
    token:str= Field(
        ...,
        title='Access Token',
        description='Generated access token by the system'
    )