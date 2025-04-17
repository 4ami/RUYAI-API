from typing import Any
from ..response_50x import Response500
from .get_one import GetOneResponse

GET_ALL_RESPONSES:dict[int, Any]={
    500: {
        'model': Response500,
        'content': {
            'application/json': {
                'example':Response500(code=500, message='Failed Due to an Internal Error').model_dump()
            }
        }
    }
}

GET_ONE_RESPONSES:dict[int, Any]={
    500: {
        'model': Response500,
        'content': {
            'application/json': {
                'example':Response500(code=500, message='Failed Due to an Internal Error').model_dump()
            }
        }
    },
    404:{
        'model':GetOneResponse,
        'content':{
            'application/json':{
                'example':GetOneResponse(code=404, message="Patient is not found").model_dump()
            }
        }
    }
}