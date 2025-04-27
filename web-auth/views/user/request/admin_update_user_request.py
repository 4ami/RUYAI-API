from pydantic import BaseModel, Field
from .user_information import AdminUseOfUserInformation


class AdminUpdateUserRequest(BaseModel):
    user_id:int=Field(
        ...,
        title='User Id'
    )
    user_information:AdminUseOfUserInformation=Field(
        ...,
        title='User Modified Information'
    )