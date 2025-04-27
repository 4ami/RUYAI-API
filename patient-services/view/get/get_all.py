from pydantic import Field
from ..base_response import BaseResponse
from ..patient_information import PatientInformation

class GetAllResponse(BaseResponse):
    patients:list[PatientInformation]=Field(
        ...,
        title='Patients List',
        description='List of all patients registered for a specific hospital'
    )