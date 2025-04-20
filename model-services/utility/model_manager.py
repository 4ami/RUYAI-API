from enum import Enum
import keras
from .preprocessing import Preprocessing, ModelType
from model import SevirityDiagnose

class CNN(str, Enum):
    __ROOT__='_algorithims'
    FineTuned_EfficientNetB5_Binary=f'{__ROOT__}/airogs_efficientnet_b5_fine-tuned.h5'
    FineTuned_EfficientNetV2B3_Binary=f'{__ROOT__}/airogs_efficientnet_v2b3_fine-tuned.h5'
    Severity_Classification=f'{__ROOT__}/Severity Classification.keras'
    FineTuned_Classification_V2B3=f'{__ROOT__}/best_model_finetuned.keras'

class ModelManager:
    def __init__(self, architecture:CNN)->None:
        self.model= keras.models.load_model(architecture.value)
        self.severity:dict[int,SevirityDiagnose]={
            0:SevirityDiagnose.S0,
            1:SevirityDiagnose.S1,
            2:SevirityDiagnose.S2,
            3:SevirityDiagnose.S3
        }

        if self.model is None: raise Exception('Failed to load model')

    def classifiy(self, img:str, type_:ModelType)->int | float:
        image=Preprocessing.prepare(img_ref=img, model_type=type_)

        if image is None: raise Exception('Image not fount / Invalid Image')

        return self.model.predict(image)
    
    def map_severity(self, predection:int)->str:
        return self.severity[predection].value