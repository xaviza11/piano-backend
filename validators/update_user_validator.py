from pydantic import BaseModel, field_validator
from typing import Optional
from utils.regex import isValidEmail, isValidPassword, isValidUserName

class UpdateUser(BaseModel):
    new_user_name: Optional[str] = None
    new_email: Optional[str] = None
    new_password: Optional[str] = None
    email: str
    password: str

    @field_validator('email')
    def validate_email(cls, v):
        if v is not None and not isValidEmail(v):
            raise ValueError('Invalid email format')
        return v
    
    @field_validator('new_email')
    def validate_new_email(cls, v):
        if v is not None and not isValidEmail(v):
            raise ValueError('Invalid email format')
        return v

    @field_validator('password')
    def validate_password(cls, v):
        if v is not None and not isValidPassword(v):
            raise ValueError('Password must be at least 8 characters long, contain an uppercase letter, and a number')
        return v

    @field_validator('new_password')
    def validate_new_password(cls, v):
        if v is not None and not isValidPassword(v):
            raise ValueError('Password must be at least 8 characters long, contain an uppercase letter, and a number')
        return v
    
    @field_validator('new_user_name')
    def validate_new_user_name(cls, v):
        if v is not None and not isValidUserName(v):
            raise ValueError('Password must be at least 8 characters long, contain an uppercase letter, and a number')
        return v