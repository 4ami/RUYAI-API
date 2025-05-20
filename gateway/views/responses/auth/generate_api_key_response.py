from ..base_response import BaseResponse
from pydantic import Field
from typing import Optional

class GenerateApiKeyResponse(BaseResponse):
    code:int=Field(
        201,
        title='Response Status Code',
        description='Protocol status code associated with response',
        strict=True
    )
    message:str=Field(
        'API Key Generated',
        title='Response Message',
        description='Illustration meesage for the response state.',
        strict=True
    )
    token:Optional[str]=Field(
        default=None,
        title='Access Token',
        description='User access token keeps user authenticated in short-term period (Session life-time) and used to navigate through the system and make use of its functionality.',
        examples=['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c']
    )