from ..base_response import BaseResponse
from pydantic import Field
from typing import Optional

class AuthLoginResponse(BaseResponse):
    token:Optional[str]=Field(
        default=None,
        title='Access Token',
        description='User access token keeps user authenticated in short-term period (Session life-time) and used to navigate through the system and make use of its functionality.',
        examples=['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c']
    )
    ref_token:Optional[str]=Field(
        default=None,
        title='Referesh Token',
        description='Referesh token act like access token except it mainly used to revoke access token when expired. Referesh token typically long-term period.',
        examples=['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c']
    )
    type:Optional[str]=Field(
        default=None,
        title='Access Token Type',
        description='A type of access token that grants access to a protected resource.',
        examples=['Bearer', 'Cookie', 'Query'],
        strict=True
    )
    loc:Optional[str]=Field(
        default=None,
        title='Location of Token',
        description='This tells where you should use token when communicate with us.',
        examples=['Authorization', 'X-API-Key']
    )

LOGIN_RESPONSES={
    404:{
        'model':AuthLoginResponse,
        'content':{
            'application/json':{
                'example': AuthLoginResponse(
                    code=404,
                    message='Email/Password incorrect'
                ).model_dump()
            }
        }
    },
    403:{
        'model':AuthLoginResponse,
        'content':{
            'application/json':{
                'example': AuthLoginResponse(
                    code=403,
                    message='Forbidden: Account is Locked'
                ).model_dump()
            }
        }
    },
    429:{
        'model':AuthLoginResponse,
        'content':{
            'application/json':{
                'example': AuthLoginResponse(
                    code=429,
                    message='Account is locked. We send you an email to re-activate your account.'
                ).model_dump()
            }
        }
    },
    500:{
        'model':AuthLoginResponse,
        'content':{
            'application/json':{
                'example':AuthLoginResponse(
                    code=500,
                    message="Login Failed Due to an Internal Error"
                ).model_dump()
            }
        }
    },
    503:{
        'model':AuthLoginResponse,
        'content':{
            'application/json':{
                'example':AuthLoginResponse(
                    code=503,
                    message="Auth service is currently unavailable"
                ).model_dump()
            }
        }
    }
}