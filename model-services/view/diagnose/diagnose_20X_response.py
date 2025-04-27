from view.base import ResponseBaseModel
from .diagnosis import Diagnosis
from pydantic import Field

class Diagnosis20X(ResponseBaseModel):
    pass

class Diagnosis200(Diagnosis20X):
    code:int=Field(
        200,
        title='Response status code',
        description='Status code associated with response'
    )
    message:str=Field(
        'Diagnosis Request Has Been Processed Successfully',
        title='Response Message',
        description='Message associated with response'
    )
    report_id:int=Field(
        ...,
        title='Report Id',
        description='The stored report that the diagnose belongs to.'
    )
    diagnosis:list[Diagnosis]=Field(
        ...,
        title='List of Diagnosed Images and Thier Results',
        description='Each uploaded OCT and its diagnose in single object.'
    )