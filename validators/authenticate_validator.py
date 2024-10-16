from pydantic import BaseModel, validator
from utils.regex import isValidEmail, isValidPassword

class AuthenticateUser(BaseModel):
    email: str
    password: str

    @validator('email')
    def validate_email(cls, v):
        if not isValidEmail(v):
            raise ValueError('Invalid email format')
        return v

    @validator('password')
    def validate_password(cls, v):
        if not isValidPassword(v):
            raise ValueError('Password must be at least 8 characters long, contain an uppercase letter, and a number')
        return v
