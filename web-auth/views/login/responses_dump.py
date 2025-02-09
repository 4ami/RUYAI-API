from .response_4xx import *
from .response_50x import *

login_dump:dict={
    404:{
        'model':Login404,
        'content':{
            'application/json':{
                'example': Login404().model_dump()
            }
        }
    },
    500:{
        'model':Login500,
        'content':{
            'application/json':{
                'example':Login500().model_dump()
            }
        }
    }
}