from pydantic import BaseModel

class DiagnoseMetadata(BaseModel):
    id:int
    glaucoma_diagnose:str
    severity:str