from pydantic import BaseModel, EmailStr
from datetime import datetime

class User(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserInDB(User):
    password: str
    createdAt : datetime = None
    updatedAt : datetime = None
