import tensorflow as tf
from enum import Enum
import cv2
import keras

class ModelType(tuple[int,int,int], Enum):
    DETECTION=(300,300,3)
    CLASSIFICATION=(380,380,3)

class Preprocessing:
    def __init__(self, type_:ModelType):
        self.MEAN = tf.constant([0.485, 0.456, 0.406], dtype=tf.float32)
        self.STD = tf.constant([0.485, 0.456, 0.406], dtype=tf.float32)
        self.SHAPE:tuple[int, int, int]=type_.value

    def _load_(self, ref:str, img_type:str):
        img=tf.io.read_file(ref)
        if img_type == 'png':
            img=tf.image.decode_png(img, channels=3)
        elif img_type in ['jpg', 'jpeg']:
            img=tf.image.decode_jpeg(img, channels=3)
        else:
            img=tf.image.decode_image(img, channels=3)
        img=tf.image.resize(img, size=[self.SHAPE[0],self.SHAPE[1]])
        img=tf.image.convert_image_dtype(image=img, dtype=tf.float32)
        return img
    
    def _severity_preprocessing_(self, ref:str):
        image = cv2.imread(ref)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (self.SHAPE[0], self.SHAPE[1]))
        image = image.astype('float32')
        image = keras.applications.efficientnet_v2.preprocess_input(image)
        image = tf.expand_dims(image, axis=0)
        return image

    @staticmethod
    def prepare(img_ref:str, model_type:ModelType, test:bool = False):
        preprocessing:Preprocessing=Preprocessing(type_=model_type)
        type_:str = img_ref.split('.')[-1]
        if model_type == ModelType.DETECTION:
            if test:
                image=preprocessing._load_(ref=f'{img_ref}', img_type=type_)
            else:
                image=preprocessing._load_(ref=f'_data/{img_ref}', img_type=type_)
            image=image/255.0
            image=(image-preprocessing.MEAN)/preprocessing.STD
            image=tf.expand_dims(image, axis=0)
            return image
        else:
            return preprocessing._severity_preprocessing_(ref=f'_data/{img_ref}')
