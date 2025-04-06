import os
from enum import Enum
import uuid
from fastapi import UploadFile
import shutil

class Destination(str, Enum):
    ROOT='_data'
    NEW=f'{ROOT}/new/'
    NORMAL=f'{ROOT}/normal/'
    GLAUCOMA_0=f'{ROOT}/mild/'
    GLAUCOMA_1=f'{ROOT}/moderate/'
    GLAUCOMA_2=f'{ROOT}/severe/'


class PathManager:
    @staticmethod
    def store_uploaded(octs:list[UploadFile])->list[tuple[str, str]]:
        if not os.path.exists(Destination.NEW.value):
            os.makedirs(Destination.NEW.value, exist_ok=True)
        
        stored:list[tuple[str,str]]=[]
        
        for oct in octs:
            _id:str=f'{uuid.uuid4()}'
            ext:str = oct.filename.split('.')[-1]
            uploaded:str=f'{_id}.{ext}'
            path=os.path.join(Destination.NEW.value, uploaded)
            with open(path, 'wb') as buf:
                shutil.copyfileobj(oct.file, buf)
            
            stored.append((uploaded, oct.filename))
        
        return stored
