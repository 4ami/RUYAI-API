from ..base_response import BaseResponse
from pydantic import Field
from typing import Optional

class UpdatedUserInformationByAdmin(BaseResponse):
    full_name:Optional[str]=Field(
        default=None,
        title='User Full Name'
    )
    role:Optional[int]=Field(
        default=None,
        title='User Role Id'
    )
    account_status:Optional[str]=Field(
        default=None,
        title='User Account Status'
    )