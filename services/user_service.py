from database import db
from auth.password_handler import get_password_hash
from models.user_model import UserInDB, User
from fastapi import HTTPException
from datetime import datetime
from auth.jwt_handler import create_access_token
from auth.password_handler import verify_password

class UserService:
    def register(self, user: User):
        if db["users"].find_one({"email": user.email}):
            raise HTTPException(status_code=400, detail="User already exists")

        hashed_password = get_password_hash(user.password)
        
        user_in_db = UserInDB(
            username=user.username,
            email=user.email,
            password=hashed_password, 
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow()
        )
        
        inserted_id = db["users"].insert_one(user_in_db.model_dump()).inserted_id
        
        access_token = create_access_token(data={"sub": str(inserted_id)})
        current_date = datetime.utcnow().isoformat() + "Z"
        
        return {
            "access_token": access_token,
            "date": current_date
        }

    def update_user(self, user_data):
        user = db["users"].find_one({"email": user_data.email})
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not verify_password(user_data.password, user["password"]):
            raise HTTPException(status_code=401, detail="Wrong password")

        updated_data = {
            "username": user_data.new_user_name,
            "email": user_data.new_email,
            "updatedAt": datetime.utcnow()
        }

        if "new_password" in user_data and user_data.new_password:
            updated_data["password"] = get_password_hash(user_data.new_password) 

        db["users"].update_one({"email": user["email"]}, {"$set": updated_data})

        return {"message": "User updated successfully"}

    def authenticate_user(self, email: str, password: str):
        user = db["users"].find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not verify_password(password, user["password"]): 
            raise HTTPException(status_code=401, detail="Wrong password")
        
        access_token = create_access_token(data={"sub": str(user["_id"])})
        current_date = datetime.utcnow().isoformat() + "Z"

        return {
            "access_token": access_token,
            "date": current_date
        }
