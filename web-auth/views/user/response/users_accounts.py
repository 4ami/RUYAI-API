from .user_base_response import UserBaseResponse
from .pending_accounts_info import PendingAccountsInformation
from pydantic import Field

class UserAccountsResponse(UserBaseResponse):
    pages:int = Field(
        default= 0,
        title= "total pages"
    )
    accounts:list[PendingAccountsInformation]=Field(
        default=[],
        title='Pending Accounts'
    )