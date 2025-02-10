from pydantic import Field
from .base_response import LockBaseResponse

class Lock50X(LockBaseResponse):
    pass

class Lock500(Lock50X):
    code:int=Field(
        500,
        title='Response Status Code',
        description='Protocol status code associated with response',
        strict=True
    )
    message:str=Field(
        'Locking Account Failed Due to an Internal Error',
        title='Response Message',
        description='Illustration meesage for the response state.',
        strict=True
    )