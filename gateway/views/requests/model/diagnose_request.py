from ..base_request import BaseRequest
from pydantic import Field
from fastapi import Form

class DiagnoseRequest(BaseRequest):
    patient_id:int=Field(
        ...,
        title='Patient ID',
        description='Patient identifier for a specific patient undergoing diagnosis.',
        examples=[1]
    )

def fromData(
    patient_id:int=Form(..., title='Patient ID', description='Patient identifier for a specific patient undergoing diagnosis.', example=1),
)->DiagnoseRequest:
    return DiagnoseRequest(patient_id=patient_id)


class InternalDiagnoseRequest(DiagnoseRequest):
    staff_id:int=Field(
        ...,
        title='Medical Staff ID',
        description='Staff ID of the person requesting the diagnosis.'
    )