from .base_response import RegisterResponseBase
from pydantic import Field
class Register40X(RegisterResponseBase):
    pass

class Register400(Register40X):
    code: int = Field(
        400, 
        title="Response Status Code", 
        description="Indicates client attempt to register using an existing email."
    )
    message: str = Field(
        "Registration Failed Due to Trying to Register an Existing Account.",
        title="Response Message",
        description="Indicates registration failure due to trying to register an existing account."
    )