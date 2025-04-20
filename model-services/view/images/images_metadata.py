from pydantic import BaseModel

class ImageMetadata(BaseModel):
    image:str
    ext:str

class ImageInformation(ImageMetadata):
    report_id:int
    path:str