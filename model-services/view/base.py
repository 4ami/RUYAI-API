from pydantic import BaseModel, Field

class RequestBaseModel(BaseModel):
    pass

class ResponseBaseModel(BaseModel):
    code:int=Field(
        ...,
        title='Response status code',
        description='Status code associated with response'
    )
    message:str=Field(
        ...,
        title='Response Message',
        description='Message associated with response'
    )