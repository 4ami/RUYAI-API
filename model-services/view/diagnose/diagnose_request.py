from view import RequestBaseModel
from pydantic import Field
from fastapi import Form

class DiagnoseRequest(RequestBaseModel):
    patient_id:int=Field(
        ...,
        title='Patient ID',
        description='Patient identifier for a specific patient undergoing diagnosis.',
        examples=[1]
    )
    staff_id:int=Field(
        ...,
        title='Medical Staff ID',
        description='Staff ID of the person requesting the diagnosis.'
    )

def fromData(
    patient_id:int=Form(..., title='Patient ID', description='Patient identifier for a specific patient undergoing diagnosis.', example=1),
    staff_id:int=Form(..., title='Medical Staff ID', description='Staff ID of the person requesting the diagnosis.')
)->DiagnoseRequest:
    return DiagnoseRequest(patient_id=patient_id, staff_id=staff_id)