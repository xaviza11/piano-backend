# routes/song_routes.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime
from database import db 
from models.song_model import CreateSong
from controllers.song_controller import create_song as create
from controllers.song_controller import retrieve_song as retrieve
from guards.access_guard import guard_access_token
from guards.guest_guard import guard_guest_token

router = APIRouter()

@router.post("/create")
async def create_song(song: CreateSong, current_guest: dict = Depends(guard_access_token)):
    user_id = current_guest.get("sub") 
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    return create(song, user_id)

@router.get("/retrieve/{song_id}")
async def retrieve_song(song_id: str, current_guest: dict = Depends(guard_guest_token)):
    return retrieve(song_id)
