from fastapi import APIRouter
diagnosis_router:APIRouter=APIRouter(
    prefix='/diagnose/v1',
    tags=['Diagnosis Model']
)



from fastapi import UploadFile, Depends
from view import fromData, DiagnoseRequest
from utility import PathManager, ModelManager, CNN, ModelType
from middleware import validate_oct_middleware
from view import Diagnosis200, Diagnosis
import numpy as np

@diagnosis_router.post(
    path='/',
    description='Upload OCT and diagnose it system',
    response_model=Diagnosis200
)
def diagnose(
    req:DiagnoseRequest=Depends(fromData),
    oct:list[UploadFile] = Depends(validate_oct_middleware)
):
    #Check staff
    
    #Check patient

    #Store
    imgs=PathManager.store_uploaded(octs=oct)

    #Diagnose
    model:ModelManager = ModelManager(architecture=CNN.FineTuned_EfficientNetB5_Binary)
    classification_model:ModelManager = ModelManager(architecture=CNN.FineTuned_Classification_V2B3)
    THRESHOLD:float=0.50
    diagnosis:list[Diagnosis] = []
    for img in imgs:
        prop= model.classifiy(img=img[0], type_=ModelType.DETECTION)
        grade= classification_model.classifiy(img=img[0], type_=ModelType.CLASSIFICATION)
        grade= np.argmax(grade, axis=1)[0]
        print(grade)
        d = Diagnosis(
            image_sent=img[1], 
            stored_as=img[0], 
            glaucoma= 'Positive' if prop[0][0] >= THRESHOLD else 'Negative',
            glaucoma_propability=prop[0][0],
            threshold_used=THRESHOLD,
            severity=classification_model.map_severity(grade)
        )
        diagnosis.append(d)
    return Diagnosis200(diagnosis=diagnosis)