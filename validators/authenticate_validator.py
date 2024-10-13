from pydantic import BaseModel, validator
from utils.regex import isValidUserName, isValidPassword

class AuthenticateUser(BaseModel):
    username: str
    password: str

    @validator('username')
    def validate_email(cls, v):
        if not isValidUserName(v):
            raise ValueError('Invalid username format')
        return v

    @validator('password')
    def validate_password(cls, v):
        if not isValidPassword(v):
            raise ValueError('Password must be at least 8 characters long, contain an uppercase letter, and a number')
        return v
