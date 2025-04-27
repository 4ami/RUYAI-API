from pydantic import Field, BaseModel, field_validator, EmailStr
import re
class LoginRequest(BaseModel):
    email:EmailStr=Field(
        ...,
        title='User email',
        description='Registered user email',
        examples=['email@example.com'],
        strict=True
    )
    password:str=Field(
        ...,
        title='User Account Password',
        description='Password of user account made during registeration.',
        examples=['Secr3t_Pa$sw0rD'],
        strict=True
    )
    @field_validator('password', mode='before')
    def password_validator(cls, value:str)->str:
        # validate password strength
        if len(value) < 8:
            raise ValueError('entered password violates length policy.')
        # validate contains alphabet
        alpha_pattern:str=r'[a-zA-Z]'
        if not re.search(alpha_pattern, value):
            raise ValueError('entered password violates alphabet policy')
        # validate at least contains one Capital letter
        capital_pattern:str=r'[A-Z]'
        if not re.search(capital_pattern, value):
            raise ValueError('entered password violates \'Upper Case Letter\' policy')
        # validate contains numbers
        num_pattern:str=r'[0-9]'
        if not re.search(num_pattern, value):
            raise ValueError('entered password violates numbers policy')
        # validate contains at least 2 digits
        dig_pattern:str=r'(?:.*\d.*\d)'
        if not re.search(dig_pattern, value):
            raise ValueError('entered password violates numbers lower limit of digits policy')
        # validate contains special
        special_pattern:str=r'[!@#$%^&*()_+\-=\[\]{};\'":\\|,.<>\/?`~]'
        if not re.search(special_pattern, value):
            raise ValueError('entered password violates special characters usage policy')
        return value