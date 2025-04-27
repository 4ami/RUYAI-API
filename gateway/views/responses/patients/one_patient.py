from ..base_response import BaseResponse
from ...patient_information import PatientInformation
from pydantic import Field
from typing import Optional

class GetOnePatientResponse(BaseResponse):
    message:Optional[str]=Field(
        default=None,
        title='Response Message',
        description='Illustration meesage for the response state.',
        examples=['Success', 'Failed'],
    )
    patient:Optional[PatientInformation]=Field(
        default=None,
        title='Patient Information',
        description='Registered patient information'
    )

GET_PATIENT_INFO_RES:dict={
    500: {
        'model': GetOnePatientResponse,
        'content': {
            'application/json': {
                'example':GetOnePatientResponse(code=500, message='Failed Due to an Internal Error').model_dump()
            }
        }
    },
    503:{
        'model': GetOnePatientResponse,
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
        'model':GetOnePatientResponse,
        'content':{
            'application/json':{
                'example':GetOnePatientResponse(code=400, message="Invalid request").model_dump()
            }
        }
    },
    404:{
        'model':GetOnePatientResponse,
        'content':{
            'application/json':{
                'example':GetOnePatientResponse(code=404, message="Patient Not Found / Missing Patient id").model_dump()
            }
        }
    }
}