from pydantic import Field
from .base_response import LockBaseResponse

class Lock20X(LockBaseResponse):
    pass

class Lock200(Lock20X):
    code:int=Field(
        200,
        title='Response Status Code',
        description='Protocol status code associated with response',
        strict=True
    )
    message:str=Field(
        'Account Locked Successfully',
        title='Response Message',
        description='Illustration meesage for the response state.',
        strict=True
    )