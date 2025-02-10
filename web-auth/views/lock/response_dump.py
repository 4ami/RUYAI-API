from .response_40x import Lock400, Lock404, Lock409
from .response_50x import Lock500
lock_dump:dict={
    400: {
        'model': Lock400,
        'content': {
            'application/json': {
                'example': Lock400().model_dump()
            }
        }
    },
    404: {
        'model': Lock404,
        'content': {
            'application/json': {
                'example': Lock404().model_dump()
            }
        }
    },
    409: {
        'model': Lock409,
        'content': {
            'application/json': {
                'example': Lock409().model_dump()
            }
        }
    },
    500: {
        'model': Lock500,
        'content': {
            'application/json': {
                'example': Lock500().model_dump()
            }
        }
    },
}