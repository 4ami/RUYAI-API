from ..base_response import BaseResponse
from pydantic import Field
from typing import Optional

class CreatePatientResponse(BaseResponse):
    message:Optional[str]=Field(
        default=None,
        title='Response Message',
        description='Illustration meesage for the response state.',
        examples=['Success', 'Failed'],
    )
    id:Optional[int]=Field(
        default=None,
        title='Patient ID',
        description='Registered Patient Id'
    )


CREATE_PATIENT_RES:dict={
    500: {
        'model': CreatePatientResponse,
        'content': {
            'application/json': {
                'example':CreatePatientResponse(code=500, message='Failed Due to an Internal Error').model_dump()
            }
        }
    },
    503:{
        'model': CreatePatientResponse,
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
    }
}