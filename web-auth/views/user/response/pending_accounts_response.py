from .user_base_response import UserBaseResponse
from .pending_accounts_info import PendingAccountsInformation
from pydantic import Field

class PendingAccountsResponse(UserBaseResponse):
    pending_accounts:list[PendingAccountsInformation]=Field(
        default=[],
        title='Pending Accounts'
    )