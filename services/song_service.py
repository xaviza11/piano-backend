from music21 import stream, note, key, scale
import random
from database import db
from fastapi import HTTPException
from bson import ObjectId
from models.song_model import CreateSong
from datetime import datetime
from google.protobuf.json_format import MessageToDict
from utils.retrieve_notes import get_scale

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
            "notes": [note.model_dump() for note in song.notes],  
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
            "createdAt": song["createdAt"],
            "updatedAt": song["updatedAt"]
        }
        
        return {"message": "Song retrieved successfully", "song_data": song_data}

    def retrieve_filtered(self, name: str = None, author: str = None, tone: str = None):
        filter_query = {}

        if not name and not author and not tone:
            raise HTTPException(status_code=400, detail="At least one search parameter is required")
        
        if name:
            filter_query["name"] = {"$regex": name, "$options": "i"}  
        if author:
            filter_query["author"] = {"$regex": author, "$options": "i"}  
        if tone:
            filter_query["tone"] = {"$regex": tone, "$options": "i"} 

        songs = db["songs"].find(filter_query)

        if db["songs"].count_documents(filter_query) == 0:
            raise HTTPException(status_code=404, detail="No songs found")

        songs_data = []
        for song in songs:
            song_data = {
                "id": str(song["_id"]),
                "name": song["name"],
                "tone": song["tone"],
                "author": song["author"],
            }
            songs_data.append(song_data)

        return {"message": "Songs retrieved successfully", "songs": songs_data}

    def generate_melody(self, tone:str):
        melody_stream = stream.Stream()
        notes_data = []
        current_time = 0.0

        selected_scale = get_scale(tone)
        
        for _ in range(8):
            pitch = random.choice([f"{n}{octave}" for n in selected_scale for octave in range(4, 6)])
        
            n = note.Note(pitch)
            n.quarterLength = random.choice([0.25, 0.5, 1.0])
            n.volume.velocityScalar = random.uniform(0.3, 1.0)

            melody_stream.append(n)

            note_data = {
                "note": n.nameWithOctave,
                "time": current_time,
                "velocity": n.volume.velocityScalar,
                "duration": n.quarterLength
            }
            notes_data.append(note_data)
            current_time += n.quarterLength

        return {"message": "Melody generated successfully", "notes": notes_data}
