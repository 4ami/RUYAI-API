from ..base_request import BaseRequest
from pydantic import Field

class GenerateApiKeyRequest(BaseRequest):
    id:int=Field(
        ...,
        title='It Staff ID'
    )