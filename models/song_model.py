from pydantic import BaseModel, Field, validator
from bson import ObjectId
from typing import List, Optional
from datetime import datetime

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
    user: str

class CreateSong(BaseModel):
    name: str
    tone: str
    author: str
    notes: List[Note]
    user: Optional[str] = Field(None)