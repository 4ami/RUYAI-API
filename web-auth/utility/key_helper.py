
import subprocess
import dotenv
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


dotenv.load_dotenv()

class KeyHelper:

    def __init__(self):
        self._private:str=None
        self._public:str=None
        self.__generate__()

    def __generate__(self)->None:
        # SECRET Not generated yet
        if not os.getenv('SECRET'):
            self.__secret_gen__()
        
        # SECRET generated, but not read yet
        if not hasattr(self, '__secret__'):
            self.__secret__=os.getenv('SECRET')   
        
        #Keys are not generated yet
        if (
            not os.path.exists('public.pem')
            and
            not os.path.exists('private.pem')
        ):
            (self.__private_gen__(), self.__public_gen__())
        


    def __secret_gen__(self)->None:
        self.__secret__=os.urandom(64).hex()
        dotenv.set_key('.env', 'SECRET', self.__secret__)

    def __public_gen__(self):
        subprocess.run([
            'openssl',
            'rsa',
            '-pubout',
            '-in',
            'private.pem',
            '-out',
            'public.pem',
            '-passin',
            'pass:{secret}'.format(secret=self.__secret__)
        ])

    def __private_gen__(self):
        subprocess.run([
            'openssl',
            'genpkey',
            '-algorithm',
            'RSA',
            '-out',
            'private.pem',
            '-aes256',
            '-pass',
            'pass:{secret}'.format(secret=self.__secret__)
        ])

    def __public_read__(self):
        with open('public.pem', 'r') as public:
            self.__public__=public.read()
        self._public=self.__public__
    
    def __private_read__(self):
        with open('private.pem', 'rb') as private:
            encrypted_private=private.read()
            try:
                self.__private__=serialization.load_pem_private_key(
                    data=encrypted_private,
                    password=self.__secret__.encode(),
                    backend=default_backend()
                ).private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ).decode()
                self._private=self.__private__
            except Exception as e:
                print(e)

    @staticmethod
    def get_public()->str:
        _kh_:KeyHelper=KeyHelper()
        if not _kh_._public:
            _kh_.__public_read__()
        return _kh_._public

    @staticmethod
    def get_private()->str:
        _kh_:KeyHelper=KeyHelper()
        if not _kh_._private:
            _kh_.__private_read__()
        return _kh_._private
