from pydantic import BaseModel

class _ImageMetadata(BaseModel):
    image:str
    ext:str

class _DiagnoseData(BaseModel):
    id:int
    glaucoma_diagnose:str
    glaucoma_confidence:float
    severity:str
    threshold:float=0.5
    image:_ImageMetadata

class ModelFullReport(BaseModel):
    report_id:int
    patient_id:int
    approval_status:str
    created_at:str
    diagnose:list[_DiagnoseData]
