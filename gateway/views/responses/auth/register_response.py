from pydantic import Field
from typing import Optional, Any
from ..base_response import BaseResponse

class AuthRegisterResponse(BaseResponse):
    code: Optional[int] = Field(
        default=None,
        title="Response Status Code", 
        description="Protocol status code associated with response"
    )
    message: Optional[str] = Field(
        default=None,
        title="Response Message",
        description="Illustration meesage for the response state."
    )


REGISTER_RESPONSES:dict[str, Any]={
    500: {
        'model': AuthRegisterResponse,
        'content': {
            'application/json': {
                'example':AuthRegisterResponse(code=500, message='Registration Failed Due to an Internal Error').model_dump()
            }
        }
    },
    503:{
        'model': AuthRegisterResponse,
        'content': {
            'application/json': {
                'example':{
                    "detail": {
                        "code": 503,
                        "message": "Auth service is currently unavailable"
                    }
                }
            }
        }
    },
    400:{
        'model':AuthRegisterResponse,
        'content':{
            'application/json':{
                'example':AuthRegisterResponse(code=400, message="Registration Failed Due to Trying to Register an Existing Account.").model_dump()
            }
        }
    }
}