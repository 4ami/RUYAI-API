from ..base_response import BaseResponse
from ...patient_information import PatientInformation
from typing import Optional
from pydantic import Field


class GetAllPatientResponse(BaseResponse):
    message:Optional[str]=Field(
        default=None,
        title='Response Message',
        description='Illustration meesage for the response state.',
        examples=['Success', 'Failed'],
    )
    patients:Optional[list[PatientInformation]]=Field(
        default=None,
        title='All Medical Staff Patients',
        description='List of patients information associated with medical staff',
        examples=[[]]
    )

GET_ALL_PATIENTS_RES:dict={
    500: {
        'model': GetAllPatientResponse,
        'content': {
            'application/json': {
                'example':GetAllPatientResponse(code=500, message='Failed Due to an Internal Error').model_dump()
            }
        }
    },
    503:{
        'model': GetAllPatientResponse,
        'content': {
            'application/json': {
                'example':{
                    "detail": {
                        "code": 503,
                        "message": "Patient service is currently unavailable"
                    }
                }
            }
        }
    },
    400:{
        'model':GetAllPatientResponse,
        'content':{
            'application/json':{
                'example':GetAllPatientResponse(code=400, message="Invalid request").model_dump()
            }
        }
    }
}