# routes/song_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime
from database import db 

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
    createdAt: datetime = None
    updatedAt: datetime = None

router = APIRouter()

@router.post("/songs/", response_model=Song)
async def create_song(song: Song):
    current_time = datetime.utcnow()
    song.createdAt = current_time
    song.updatedAt = current_time

    result = db["songs"].insert_one(song.dict())
    if not result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to create song")

    return {**song.dict(), "id": str(result.inserted_id)}

@router.get("/songs/", response_model=List[Song])
async def get_songs():
    songs = db["songs"].find()
    return [Song(**song) for song in songs]

@router.get("/songs/{song_id}", response_model=Song)
async def get_song(song_id: str):
    song = db["songs"].find_one({"_id": song_id})
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return Song(**song)

@router.put("/songs/{song_id}", response_model=Song)
async def update_song(song_id: str, updated_song: Song):
    updated_song.updatedAt = datetime.utcnow()
    result = db["songs"].replace_one({"_id": song_id}, updated_song.dict())
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Song not found")

    return {**updated_song.dict(), "id": song_id}

@router.delete("/songs/{song_id}")
async def delete_song(song_id: str):
    result = db["songs"].delete_one({"_id": song_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Song not found")
    return {"message": "Song deleted successfully"}
