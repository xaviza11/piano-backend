from pydantic import BaseModel, EmailStr
from typing import List  

class Note(BaseModel):
    note: str
    time: float
    velocity: float
    duration: float

class Song(BaseModel):
    name: str
    tone: str
    author: str
    notes: List[Note]  
