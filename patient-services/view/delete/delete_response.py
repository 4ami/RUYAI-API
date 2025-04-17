from ..base_response import BaseResponse
from pydantic import Field

class DeleteResponse(BaseResponse):
    message:str=Field(
        ...,
        title='Response Message'
    )