from database import db
from auth.password_handler import get_password_hash
from models.user_model import UserInDB, User
from fastapi import HTTPException
from datetime import datetime
from auth.jwt_handler import create_access_token
from auth.password_handler import verify_password

class UserService:
    def register(self, user: User):
        if db["users"].find_one({"username": user.username}):
            raise HTTPException(status_code=400, detail="User already exists")

        hashed_password = get_password_hash(user.password)
        
        user_in_db = UserInDB(
            username=user.username,
            email=user.email,
            password=hashed_password, 
            createdAt=datetime.utcnow(),  
            updatedAt=datetime.utcnow()  
        )
        
        db["users"].insert_one(user_in_db.dict())

def update_user(self, username: str, password: str, user_data: User):
        user = db["users"].find_one({"username": username})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not verify_password(password, user["password"]):
            raise HTTPException(status_code=403, detail="Invalid password")

        updated_data = {
            "username": user_data.username,
            "email": user_data.email,
            "updatedAt": datetime.utcnow()  
        }

        if user_data.password:
            updated_data["password"] = get_password_hash(user_data.password)

        db["users"].update_one({"username": username}, {"$set": updated_data})

def authenticate_user(self, username: str, password: str):
        user = db["users"].find_one({"username": username})
        if not user or not verify_password(password, user["password"]): 
            return None
        return create_access_token(data={"sub": user["username"]})
