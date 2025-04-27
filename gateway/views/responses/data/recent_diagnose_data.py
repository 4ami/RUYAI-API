from pydantic import BaseModel
from ...patient_information import PatientInformation
class RecentPatientDiagnose(BaseModel):
    patient_id:int
    report_id:int
    glaucoma:str="N/A"
    severity:str="N/A"

class RecentPatientDiagnoseFull(BaseModel):
    report_id:int
    patient_info:PatientInformation
    glaucoma:str="N/A"
    severity:str="N/A"