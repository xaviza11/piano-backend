from pydantic import BaseModel, FieldValidationInfo, field_validator
from typing import List
from utils.validate_functions import is_valid_tone

class Note(BaseModel):
    note: str
    time: float
    velocity: float
    duration: float

class CreateSong(BaseModel):
    name: str
    tone: str
    author: str
    notes: List[Note]

    @field_validator('tone')
    def validate_tone(cls, v: str) -> str:
        if not is_valid_tone(v):
            raise ValueError('Invalid tone')
        return v
