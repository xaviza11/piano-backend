from fastapi import HTTPException
from services.user_service import UserService
from models.user_model import User

user_service = UserService()

def register_user(user: User):
    try:
        user_service.register(user)
        return {"message": "User registered successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

def login_user(form_data):
    token_data = user_service.authenticate_user(form_data.email, form_data.password)
    
    if not token_data:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    return {
        "access_token": token_data["access_token"],
        "username": token_data["username"],
        "message": token_data["message"],
        "date": token_data["date"]
    }


def update_user(user_data):
    try:
        user_service.update_user(user_data)
        return {"message": "User updated successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
