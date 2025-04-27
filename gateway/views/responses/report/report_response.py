from ..base_response import BaseResponse
from ...patient_information import PatientInformation
from typing import Optional
from ..model import ModelFullReport

class ReportResponse(BaseResponse):
    patient_information:Optional[PatientInformation]
    report:Optional[ModelFullReport]
    