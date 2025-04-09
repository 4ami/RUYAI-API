from .base_response import LoginResponseBase
from pydantic import Field

class Login20X(LoginResponseBase):
    pass

class Login200(Login20X):
    code:int=Field(
        200,
        title='Response Status Code',
        description='Protocol status code associated with response',
        strict=True
    )
    message:str=Field(
        'Login Success. {Authenticated}',
        title='Response Message',
        description='Illustration meesage for the response state.',
        strict=True
    )
    token:str=Field(
        ...,
        title='Access Token',
        description='User access token keeps user authenticated in short-term period (Session life-time) and used to navigate through the system and make use of its functionality.',
        examples=['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c']
    )
    ref_token:str=Field(
        ...,
        title='Referesh Token',
        description='Referesh token act like access token except it mainly used to revoke access token when expired. Referesh token typically long-term period.',
        examples=['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c']
    )
    type:str=Field(
        'Bearer',
        title='Access Token Type',
        description='A type of access token that grants access to a protected resource.',
        examples=['Bearer', 'Cookie', 'Query'],
        strict=True
    )
    loc:str=Field(
        'Authorization',
        title='Location of Token',
        description='This tells where you should use token when communicate with us.',
        examples=['Authorization', 'X-API-Key']
    )