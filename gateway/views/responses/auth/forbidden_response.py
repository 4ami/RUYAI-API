from ..base_response import BaseResponse
from pydantic import Field

class ForbiddenResponse(BaseResponse):
    code:int=Field(
        403,
        title='Response Status Code',
        description='Protocol status code associated with response',
        strict=True
    )
    message:str=Field(
        'Forbidden - You are not allowed to perform this action',
        title='Response Message',
        description='Illustration meesage for the response state.',
        strict=True
    )