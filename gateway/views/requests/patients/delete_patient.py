from ..base_request import BaseRequest
from pydantic import Field

class DeletePatientRequest(BaseRequest):
    id:int=Field(
        ...,
        title='Patient Id'
    )

class InternalDeletePatientRequest(DeletePatientRequest):
    medical_staff_id:int=Field(
        ...,
        title='Medical Staff Id'
    )