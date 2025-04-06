from fastapi import UploadFile, File
from fastapi.exceptions import HTTPException

def validate_oct_middleware(
    octs:list[UploadFile]=File(
        ...,
        title='OCT Images',
        description='OCT images that required to be diagnosed'
    )
) -> list[UploadFile]:
    allowed:list[str]=['png', 'jpg', 'jpeg']
    allowed_size:int=500*1000
    for file in octs:
        if file.filename.split('.')[-1] not in allowed:
            raise HTTPException(
                status_code=400,
                detail={
                    'message': f'{file.filename} is not allowed!',
                    'allowed_files': allowed
                }
            )
        if file.size > allowed_size:
            raise HTTPException(
                status_code=400,
                detail={
                    'message': f'{file.filename} is not allowed!',
                    'allowed_size': f'{allowed_size} bytes / {allowed_size/1000} KB'
                }
            )
    
    return octs