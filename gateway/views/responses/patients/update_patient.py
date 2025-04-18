from ..base_response import BaseResponse
from pydantic import Field
from typing import Optional

class UpdatePtaitenResponse(BaseResponse):
    message:Optional[str]=Field(
        default=None,
        title='Response message',
        description='Message associated with response.'
    )
    first_name:Optional[str]=Field(
        None,
        title='First Name',
        description='Patient First Name'
    )
    middle_name:Optional[str]=Field(
        None,
        title='Middle Name',
        description='Patient Middle Name'
    )
    last_name:Optional[str]=Field(
        None,
        title='Last Name',
        description='Patient Last Name'
    )
    birth_date:Optional[str]=Field(
        None,
        title='Birth Date',
        description='Patient Birth Date'
    )
    gender:Optional[str]=Field(
        None,
        title='Gender',
        description='Patient Gender'
    )
    medical_history:Optional[dict]=Field(
        default=None,
        title='Medical History',
        description='Patient Medical History'
    )

UPDATE_PATIENT_RES:dict={
    404: {
        'model': UpdatePtaitenResponse,
        'content': {
            'application/json': {
                'example':UpdatePtaitenResponse(
                    code=404,
                    message='Patient\'s information failed to updated.',
                ).model_dump()
            }
        }
    },
    500: {
        'model': UpdatePtaitenResponse,
        'content': {
            'application/json': {
                'example':UpdatePtaitenResponse(code=500, message='Failed Due to an Internal Error').model_dump()
            }
        }
    },
    503:{
        'model': UpdatePtaitenResponse,
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