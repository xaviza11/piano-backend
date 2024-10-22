from pydantic import BaseModel, field_validator
from utils.regex import isValidEmail, isValidPassword, isValidUserName

class UserName(BaseModel):
    username: str

    @field_validator('username')
    def validate_username(cls, v):
        if not isValidUserName(v):
            raise ValueError('Username can only contain letters and numbers without symbols')
        return v
