from pydantic import BaseModel

class BaseRequest(BaseModel):
    model_config={"extra":"forbid"}