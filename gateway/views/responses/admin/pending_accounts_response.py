from pydantic import BaseModel
from ..base_response import BaseResponse
from pydantic import Field

class PendingAccountsInformation(BaseModel):
    id:int
    full_name:str
    email:str
    account_status:str
    role:int
    created_at:str

class PendingAccountsResponse(BaseResponse):
    pending_accounts:list[PendingAccountsInformation]=Field(
        default=[],
        title='Pending Accounts'
    )