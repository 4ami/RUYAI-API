from ..base_response import BaseResponse
from pydantic import Field
from typing import Optional

class VerifyTokenResponse(BaseResponse):
    valid:bool=Field(
        ...,
        title='Token Validity'
    )
    id:Optional[int]=Field(
        default=None,
        title='User ID'
    )
    full_name:Optional[str]=Field(
        default=None,
        title='User Full Name'
    )
    role:Optional[int]=Field(
        default=None,
        title='User Role'
    )