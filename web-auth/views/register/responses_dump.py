from .response_50x import *
from .response_40x import *
register_dump:dict={
    500: {
        'model': Register500,
        'content': {
            'application/json': {
                'example':Register500().model_dump()
            }
        }
    },
    400:{
        'model':Register400,
        'content':{
            'application/json':{
                'example':Register400().model_dump()
            }
        }
    }
}