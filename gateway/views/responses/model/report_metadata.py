from pydantic import BaseModel
from .diagnose_metadata import DiagnoseMetadata

class ReportMetadata(BaseModel):
    report_id:int
    patient_id:int
    approval_status:str
    created_at:str
    diagnosis:list[DiagnoseMetadata]