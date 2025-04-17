from pydantic import BaseModel, Field
from typing import Optional


class UpdatePatientInfoRequest(BaseModel):
    id:int=Field(
        ...,
        title='Patient Id',
        description='Identifier of a specific patient'
    )
    first_name:Optional[str]=Field(
        default=None,
        title='First Name',
        description='Patient First Name'
    )
    middle_name:Optional[str]=Field(
        default=None,
        title='Middle Name',
        description='Patient Middle Name'
    )
    last_name:Optional[str]=Field(
        default=None,
        title='Last Name',
        description='Patient Last Name'
    )
    birth_date:Optional[str]=Field(
        default=None,
        title='Birth Date',
        description='Patient Birth Date'
    )
    gender:Optional[str]=Field(
        default=None,
        title='Gender',
        description='Patient Gender'
    )
    medical_history:Optional[dict]=Field(
        default=None,
        title='Medical History',
        description='Patient Medical History'
    )
    medical_staff_id:int=Field(
        ...,
        title='Medical Staff Id',
        description='Medical Staff Id Responsible of Registering Patient'
    )