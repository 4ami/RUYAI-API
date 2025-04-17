from ..base_response import BaseResponse
from pydantic import Field
from typing import Optional

class CreatePatientResponse(BaseResponse):
    id:Optional[int]=Field(
        default=None,
        title='Patient ID',
        description='Registered Patient Id'
    )