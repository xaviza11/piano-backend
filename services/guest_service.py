from auth.jwt_handler import generate_guest_token, decode_guest_token
from datetime import datetime
from models.guest_model import GuestInDB
from database import db  
from bson.objectid import ObjectId

class GuestService:
    def create(self):
        
        guest_data = GuestInDB(
            token="",  
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow()
        )
        
        inserted_guest = db["guests"].insert_one(guest_data.model_dump())
        guest_id = str(inserted_guest.inserted_id) 

        guest_token = generate_guest_token(guest_id)

        db["guests"].update_one(
            {"_id": ObjectId(guest_id)},
            {"$set": {"token": guest_token, "updatedAt": datetime.utcnow()}}
        )

        return {"guest_token": guest_token}
