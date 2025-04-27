from pydantic import Field, BaseModel
class Diagnosis(BaseModel):
    image_sent:str=Field(
        ...,
        title='Image Sent',
        description='Represent information of image send by client side.',
        examples=['sample.png']
    )
    stored_as:str=Field(
        ...,
        title='Stored As',
        description='Represents the stored image reference information',
        examples=['1474eea8-5f2a-4d4b-9cf1-338ff9a12834.png']
    )
    glaucoma:str=Field(
        ...,
        title='Glaucoma Status',
        description='Tells if the image contains glaucoma signs',
        examples=['Positive', 'Negative']
    )
    glaucoma_propability:float=Field(
        ...,
        title='Glaucoma Propability',
        description='The propability of having glaucoma predicted by the binary model.',
        examples=[0.3512, 0.99123]
    )
    threshold_used:float=Field(
        0.5,
        title='Threshold',
        description='Threshold used to detrmine positive or negative class for the predicted value'
    )
    severity:str=Field(
        ...,
        title='Glaucoma Severity (positive cases)',
        description='Which severity class that the uploaded image fall under.',
        examples=['Mild', 'Moderate', 'Severe', 'NA']
    )