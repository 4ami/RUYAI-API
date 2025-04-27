from .base_response import LoginResponseBase
from pydantic import Field

class Login50x(LoginResponseBase):
    pass

class Login500(Login50x):
    code: int = Field(
        500, 
        title="Response Status Code", 
        description="Indicates an internal server error."
    )
    message: str = Field(
        "Login Failed Due to an Internal Error",
        title="Response Message",
        description="Indicates login failure due to an internal error."
    )