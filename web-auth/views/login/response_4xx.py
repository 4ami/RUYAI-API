from .base_response import LoginResponseBase
from pydantic import Field

class Login4XX(LoginResponseBase):
    pass

class Login404(Login4XX):
    code:int=Field(
        404,
        title='Response Status Code',
        description='Protocol status code associated with response',
    )
    message:str=Field(
        'Email/Password incorrect',
        title='Response Message',
        description='Illustration meesage for the response state.',
    )

class Login403(Login4XX):
    code:int=Field(
        403,
        title='Response Status Code',
        description='Protocol status code associated with response',
    )
    message:str=Field(
        'Forbidden: Account is Locked',
        title='Response Message',
        description='Illustration meesage for the response state.',
    )