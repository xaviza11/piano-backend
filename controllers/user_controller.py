from fastapi import HTTPException, Depends
from services.user_service import UserService
from fastapi.security import OAuth2PasswordRequestForm
from models.user_model import User

user_service = UserService()

def register_user(user: User):
    try:
        user_service.register(user)
        return {"message": "User registered successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    token = user_service.authenticate_user(form_data.username, form_data.password)
    if not token:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}

def update_user(username, password, user_data):
    try:
        user_service.update_user(username, password, user_data)
        return {"message": "User updated successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
