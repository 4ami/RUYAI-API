from pydantic import Field
from .base_response import UnLockBaseResponse

class UnLock20X(UnLockBaseResponse):
    pass

class UnLock200(UnLock20X):
    code:int=Field(
        200,
        title='Response Status Code',
        description='Protocol status code associated with response',
        strict=True
    )
    message:str=Field(
        'Account Unlocked Successfully',
        title='Response Message',
        description='Illustration meesage for the response state.',
        strict=True
    )