from ..base_response import BaseResponse
from pydantic import Field
from .pending_accounts_response import PendingAccountsInformation

class UserAccountsResponse(BaseResponse):
    pages:int = Field(
        default= 0,
        title= "total pages"
    )
    accounts:list[PendingAccountsInformation]=Field(
        default=[],
        title='Pending Accounts'
    )