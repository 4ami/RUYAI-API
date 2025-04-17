from ..base_response import BaseResponse
from ..response_50x import Response500
from pydantic import Field
from typing import Any,Optional

class UpdatedPatientInfoResponse(BaseResponse):
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

UPDATE_PATIENT_INFO_RESPONSES:dict[int, Any]={
     200: {
        'model': UpdatedPatientInfoResponse,
        'content': {
            'application/json': {
                'example':UpdatedPatientInfoResponse(
                    code=200,
                    first_name='John',
                    middle_name='Nommensen',
                    last_name='Doe',
                    birth_date="YYYY/MM/DD",
                    gender='MALE/FEMALE',
                    medical_history={}
                ).model_dump()
            }
        }
    },
     404: {
        'model': UpdatedPatientInfoResponse,
        'content': {
            'application/json': {
                'example':UpdatedPatientInfoResponse(
                    code=404,
                    message='Patient\'s information failed to updated.',
                ).model_dump()
            }
        }
    },
     500: {
        'model': Response500,
        'content': {
            'application/json': {
                'example':Response500(code=500, message='Failed Due to an Internal Error').model_dump()
            }
        }
    }
}