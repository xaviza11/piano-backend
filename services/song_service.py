from database import db
from fastapi import HTTPException
from bson import ObjectId
from models.song_model import CreateSong
from datetime import datetime

class SongService:
    def create(self, song: CreateSong, user_id):
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid user ObjectId")
        
        user = db["users"].find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        song_in_db = {
            "name": song.name,
            "tone": song.tone,
            "author": song.author,
            "notes": [note.dict() for note in song.notes],  
            "user": ObjectId(user_id),  
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
        }
        
        result = db["songs"].insert_one(song_in_db)
        
        if result.inserted_id:
            return {
                "message": "Song created successfully",
                "id": str(result.inserted_id)
            }
        else:
            raise HTTPException(status_code=500, detail="Song creation failed")
        
    def retrieve(self, song_id):
        if not ObjectId.is_valid(song_id):
            raise HTTPException(status_code=400, detail="Invalid song ObjectId")
        
        song = db["songs"].find_one({"_id": ObjectId(song_id)})
        if not song:
            raise HTTPException(status_code=404, detail="Song not found")
        
        song_data = {
            "id": str(song["_id"]),
            "name": song["name"],
            "tone": song["tone"],
            "author": song["author"],
            "notes": song["notes"],
            "user": str(song["user"]),
            "createdAt": song["createdAt"],
            "updatedAt": song["updatedAt"]
        }
        
        return {"message": "song retrieved successfully", "song_data": song_data}
