from pydantic import BaseModel, field_validator
from utils.regex import isValidEmail, isValidPassword

class UserPassword(BaseModel):
    password: str

    @field_validator('password')
    def validate_password(cls, v):
        if not isValidPassword(v):
            raise ValueError('Password must be at least 8 characters long, contain an uppercase letter, and a number')
        return v
