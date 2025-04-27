from ..base_response import BaseResponse

class DeletePatientResponse(BaseResponse):
    pass

DELETE_PATIENT_RES:dict={
    500: {
        'model': DeletePatientResponse,
        'content': {
            'application/json': {
                'example':DeletePatientResponse(code=500, message='Failed Due to an Internal Error').model_dump()
            }
        }
    },
    503:{
        'model': DeletePatientResponse,
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
        'model':DeletePatientResponse,
        'content':{
            'application/json':{
                'example':DeletePatientResponse(code=400, message="Invalid request").model_dump()
            }
        }
    },
    404:{
        'model':DeletePatientResponse,
        'content':{
            'application/json':{
                'example':DeletePatientResponse(code=404, message="Patient is not exist").model_dump()
            }
        }
    }
}