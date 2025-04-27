from pydantic import BaseModel

class PendingAccountsInformation(BaseModel):
    id:int
    full_name:str
    email:str
    account_status:str
    role:int
    created_at:str