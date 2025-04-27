from pydantic import Field
from .base_response import RegisterResponseBase


class Register50X(RegisterResponseBase):
    pass

class Register500(Register50X):
    code: int = Field(
        500, 
        title="Response Status Code", 
        description="Indicates an internal server error."
    )
    message: str = Field(
        "Registration Failed Due to an Internal Error",
        title="Response Message",
        description="Indicates registration failure due to an internal error."
    )