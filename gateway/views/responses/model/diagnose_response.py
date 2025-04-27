from ..base_response import BaseResponse
from .diagnose_information import DiagnoseInformation
from pydantic import Field
from typing import Optional

class DiagnoseResponse(BaseResponse):
    report_id:int=Field(
        ...,
        title='Report Id',
        description='The stored report that the diagnose belongs to.'
    )
    diagnosis:Optional[list[DiagnoseInformation]]=Field(
        default=None,
        title='List of Diagnosed Images and Thier Results',
        description='Each uploaded OCT and its diagnose in single object.'
    )