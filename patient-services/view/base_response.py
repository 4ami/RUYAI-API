from pydantic import BaseModel, Field

class BaseResponse(BaseModel):
    code:int=Field(
        ...,
        title='Response status code',
        description='Http status code describe status of request'
    )