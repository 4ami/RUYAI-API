from pydantic import Field
from .base_response import LockBaseResponse

class Lock40X(LockBaseResponse):
    pass

class Lock400(Lock40X):
    code:int=Field(
        400,
        title='Response Status Code',
        description='Protocol status code associated with response',
        strict=True
    )
    message:str=Field(
        'Bad Request: Provided information are invalid',
        title='Response Message',
        description='Illustration meesage for the response state.',
        strict=True
    )

class Lock404(Lock40X):
    code:int=Field(
        404,
        title='Response Status Code',
        description='Protocol status code associated with response',
    )
    message:str=Field(
        'User Account is Not Registered',
        title='Response Message',
        description='Illustration meesage for the response state.',
    )

class Lock409(Lock40X):
    code:int=Field(
        409,
        title='Response Status Code',
        description='Protocol status code associated with response',
    )
    message:str=Field(
        'Conflict: User Account is Already Locked',
        title='Response Message',
        description='Illustration meesage for the response state.',
    )