from .response_40x import UnLock400, UnLock404, UnLock409
from .response_50x import UnLock500
unlock_dump:dict={
    400: {
        'model': UnLock400,
        'content': {
            'application/json': {
                'example': UnLock400().model_dump()
            }
        }
    },
    404: {
        'model': UnLock404,
        'content': {
            'application/json': {
                'example': UnLock404().model_dump()
            }
        }
    },
    409: {
        'model': UnLock409,
        'content': {
            'application/json': {
                'example': UnLock409().model_dump()
            }
        }
    },
    500: {
        'model': UnLock500,
        'content': {
            'application/json': {
                'example': UnLock500().model_dump()
            }
        }
    },
}