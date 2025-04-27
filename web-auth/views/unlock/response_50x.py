from pydantic import Field
from .base_response import UnLockBaseResponse

class UnLock50X(UnLockBaseResponse):
    pass

class UnLock500(UnLock50X):
    code:int=Field(
        500,
        title='Response Status Code',
        description='Protocol status code associated with response',
        strict=True
    )
    message:str=Field(
        'Unlocking Account Failed Due to an Internal Error',
        title='Response Message',
        description='Illustration meesage for the response state.',
        strict=True
    )