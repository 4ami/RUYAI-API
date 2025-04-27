from ..base_request import BaseRequest
from pydantic import Field, field_validator

class AddFeedbackRequest(BaseRequest):
    report_id:int=Field(
        ...,
        title='Report Id'
    )
    approval_status:str=Field(
        ...,
        title='Approval Status'
    )
    rate:float=Field(
        ...,
        title='Rating'
    )
    comment:str=Field(
        ...,
        title='Feedback Comment'
    )

    @field_validator('approval_status', mode='before')
    def approval_validation(cls, value:str):
        upper:str = value.upper()
        allowed:list[str] = ['REJECTED', 'APPROVED']
        if not upper in allowed:
            raise ValueError('approval_status must be either \'APPROVED\' or \'REJECTED\'')
        return upper
    
    @field_validator('rate', mode='before')
    def rate_validation(cls, value:float):
        if not (value >= 0 and value <= 10):
            raise ValueError('rate must be in valid range 0-10')
        return value
    
class InternalAddFeedbackRequest(AddFeedbackRequest):
    staff_id:int=Field(
        ...,
        title='Staff Id'
    )