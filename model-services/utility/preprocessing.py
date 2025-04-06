import tensorflow as tf

class Preprocessing:
    def __init__(self):
        self.MEAN = tf.constant([0.485, 0.456, 0.406], dtype=tf.float32)
        self.STD = tf.constant([0.485, 0.456, 0.406], dtype=tf.float32)
        self.SHAPE:tuple[int, int, int]=(456,456,3)

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
        

    @staticmethod
    def prepare(img_ref:str):
        preprocessing:Preprocessing=Preprocessing()
        type_:str = img_ref.split('.')[-1]
        image=preprocessing._load_(ref=f'_data/new/{img_ref}', img_type=type_)
        image=image/255.0
        image=(image-preprocessing.MEAN)/preprocessing.STD
        image=tf.expand_dims(image, axis=0)
        return image