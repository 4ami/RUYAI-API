from pydantic import Field
from .base_response import BaseResponse

class Response500(BaseResponse):
    code:int=Field(
        500,
        title='Response status code',
        description='Http status code describe status of request'
    )
    message:str=Field(
        'Server-Side Error',
        title='Response Message',
        description='Associated Message with response indicating error reason'
    )