from ..base_request import BaseRequest
from pydantic import Field
from .user_information_admin_use import UserInformationForAdmin

class UpdateUserByAdminRequest(BaseRequest):
    user_id:int=Field(
        ...,
        title='User Id'
    )
    user_information:UserInformationForAdmin=Field(
        ...,
        title='User Modified Information'
    )