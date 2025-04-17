from pydantic import Field
from ..base_response import BaseResponse
from ..patient_information import PatientInformation
from typing import Optional

class GetOneResponse(BaseResponse):
    message:Optional[str]=Field(
        default=None,
        title='Response Message',
        description='Message describe status of response'
    )
    patient:Optional[PatientInformation]=Field(
        default=None,
        title='Patient Information',
        description='Registered patient information'
    )

