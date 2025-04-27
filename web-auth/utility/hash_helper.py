import os
import hashlib
class HashHelper:
    @staticmethod
    def hash(password:str)->tuple[str,str]:
        salt:bytes=os.urandom(64)
        hashed:str= hashlib.sha256((salt+password.encode())).hexdigest()
        return (hashed, salt.hex())
    
    @staticmethod
    def compare(hashed:str, salt:str, password:str)->bool:
        salt_bytes:bytes=bytes.fromhex(salt)
        password=hashlib.sha256((salt_bytes+password.encode())).hexdigest()
        return hashed==password
    
    @staticmethod
    def hash_with_salt(password:str, salt:str)->str:
        salt_bytes:bytes = bytes.fromhex(salt)
        hashed:str= hashlib.sha256((salt_bytes+password.encode())).hexdigest()
        return hashed