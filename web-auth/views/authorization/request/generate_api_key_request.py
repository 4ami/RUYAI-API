from pydantic import Field, BaseModel

class GenerateApiKeyRequest(BaseModel):
    id:int=Field(
        ...,
        title='It Staff ID'
    )