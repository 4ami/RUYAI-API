from pydantic import BaseModel, Field

class IsAdminResponse(BaseModel):
    code:int=Field(
        ...,
        title='Response Status Code'
    )
    message:str=Field(
        ...,
        title='Response message'
    )