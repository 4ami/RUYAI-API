from pydantic import BaseModel
from ..images import ImageMetadata

class DiagnoseMetadata(BaseModel):
    id:int
    glaucoma_diagnose:str
    severity:str

class CompleteDiagnose(DiagnoseMetadata):
    glaucoma_confidence:float
    threshold:float=0.5
    image:ImageMetadata