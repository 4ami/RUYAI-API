from pydantic import BaseModel

class RecentPatientDiagnose(BaseModel):
    patient_id:int
    report_id:int
    glaucoma:str="N/A"
    severity:str="N/A"