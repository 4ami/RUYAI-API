from ..base_response import BaseResponse
from pydantic import Field

class UnauthorizedResponse(BaseResponse):
    code:int=Field(
        401,
        title='Response Status Code',
        description='Protocol status code associated with response',
        strict=True
    )
    message:str=Field(
        'Unauthorized',
        title='Response Message',
        description='Illustration meesage for the response state.',
        strict=True
    )