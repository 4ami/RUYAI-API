from pydantic import BaseModel, Field

class DeletePatientRequest(BaseModel):
    id:int=Field(
        ...,
        title='Patient Id'
    )
    medical_staff_id:int=Field(
        ...,
        title='Medical Staff Id'
    )