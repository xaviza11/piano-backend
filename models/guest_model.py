from pydantic import BaseModel, EmailStr
from datetime import datetime

class Guest(BaseModel):
    token: str

class GuestInDB(Guest):
    createdAt : datetime = None
    updatedAt : datetime = None
