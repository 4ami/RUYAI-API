import os
from enum import Enum
from dotenv import load_dotenv
load_dotenv()

class AVAILABLE_SERVICES(str, Enum):
    __HOST__=os.getenv('HOST')
    AUTH=f'{__HOST__}:3001'
    AI=f'{__HOST__}:3002'
    PATIENT=f'{__HOST__}:3003'