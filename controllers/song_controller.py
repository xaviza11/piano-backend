from fastapi import HTTPException
from services.song_service import SongService
from models.song_model import Song

song_service = SongService()

def create_song(song: Song, user_id: str):
    try:
        song_service.create(song, user_id)
        return {"message": "Song created successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)