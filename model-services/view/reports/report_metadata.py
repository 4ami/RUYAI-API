from pydantic import BaseModel
from datetime import date
from ..diagnose import DiagnoseMetadata, CompleteDiagnose

class ReportMetadata(BaseModel):
    report_id:int
    patient_id:int
    approval_status:str
    created_at:date


class ReportDiagnosisMetadata(ReportMetadata):
    diagnosis:list[DiagnoseMetadata]

class FullReportData(ReportMetadata):
    diagnose:list[CompleteDiagnose]