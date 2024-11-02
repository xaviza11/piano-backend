from fastapi import HTTPException
from services.song_service import SongService
from models.song_model import Song

song_service = SongService()

def create_song(song: Song, user_id: str):
    try:
        response = song_service.create(song, user_id)
        return response  
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
def retrieve_song(song_id: str):
    try:
        song_data = song_service.retrieve(song_id)
        return song_data
    except HTTPException as e:
                raise HTTPException(status_code=e.status_code, detail=e.detail)

def retrieve_songs(name: str = None, author: str = None, tone: str = None):
    try:
        data = song_service.retrieve_filtered(name, author, tone)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
def generate_song(tone: str):
     try:
        data = song_service.generate_melody(tone)
        return data
     except HTTPException as e:
          raise HTTPException(status_code=e.status_code, detail=e.detail)