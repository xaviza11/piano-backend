from pydantic import BaseModel, field_validator
from utils.regex import isValidEmail, isValidPassword, isValidUserName

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

    @field_validator('username')
    def validate_username(cls, v):
        if not isValidUserName(v):
            raise ValueError('Username can only contain letters and numbers without symbols')
        return v

    @field_validator('email')
    def validate_email(cls, v):
        if not isValidEmail(v):
            raise ValueError('Invalid email format')
        return v

    @field_validator('password')
    def validate_password(cls, v):
        if not isValidPassword(v):
            raise ValueError('Password must be at least 8 characters long, contain an uppercase letter, and a number')
        return v
