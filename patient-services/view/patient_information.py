from pydantic import BaseModel

class PatientInformation(BaseModel):
    _id:str
    first_name:str
    middle_name:str
    last_name:str
    birth_date:str
    gender:str
    medical_history:dict