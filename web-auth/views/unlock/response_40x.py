from pydantic import Field
from .base_response import UnLockBaseResponse

class UnLock40X(UnLockBaseResponse):
    pass

class UnLock400(UnLock40X):
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

class UnLock404(UnLock40X):
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

class UnLock409(UnLock40X):
    code:int=Field(
        409,
        title='Response Status Code',
        description='Protocol status code associated with response',
    )
    message:str=Field(
        'Conflict: User Account is Already Unlocked',
        title='Response Message',
        description='Illustration meesage for the response state.',
    )