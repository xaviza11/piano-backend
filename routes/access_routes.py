from fastapi import APIRouter
from controllers.access_controller import renew_access_token
from models.user_model import User
# from fastapi.security import OAuth2PasswordRequestForm
# from guards.auth_guard import get_current_user

router = APIRouter()

@router.post("/renew")
def renew_token(token: str):
    return renew_access_token(token)
