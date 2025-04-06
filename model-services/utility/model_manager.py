from enum import Enum
import keras
from .preprocessing import Preprocessing

class CNN(str, Enum):
    __ROOT__='_algorithims'
    FineTuned_EfficientNetB5_Binary=f'{__ROOT__}/airogs_efficientnet_b5_fine-tuned.h5'

class ModelManager:
    def __init__(self, architecture:CNN)->None:
        self.model= keras.models.load_model(architecture.value)

        if self.model is None: raise Exception('Failed to load model')

    def classifiy(self, img:str)->int | float:
        image=Preprocessing.prepare(img_ref=img)

        if image is None: raise Exception('Image not fount / Invalid Image')

        return self.model.predict(image)