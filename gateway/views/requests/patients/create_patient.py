from ..base_request import BaseRequest
from pydantic import Field
from typing import Optional

class CreatePatientRequest(BaseRequest):
    first_name:str=Field(
        ...,
        title='First Name',
        description='Patient First Name'
    )
    middle_name:str=Field(
        ...,
        title='Middle Name',
        description='Patient Middle Name'
    )
    last_name:str=Field(
        ...,
        title='Last Name',
        description='Patient Last Name'
    )
    birth_date:str=Field(
        ...,
        title='Birth Date',
        description='Patient Birth Date'
    )
    gender:str=Field(
        ...,
        title='Gender',
        description='Patient Gender'
    )
    medical_history:Optional[dict]=Field(
        default=None,
        title='Medical History',
        description='Patient Medical History'
    )

class InternalCreatePatientRequest(CreatePatientRequest):
    medical_staff_id:int=Field(
        ...,
        title='Medical Staff ID',
        description='Identifier use to relate patient with staff'
    )