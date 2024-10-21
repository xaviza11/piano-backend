from fastapi import APIRouter, Header, HTTPException
from controllers.access_controller import renew_token as renew_token_controller
from models.user_model import User
# from fastapi.security import OAuth2PasswordRequestForm
# from guards.auth_guard import get_current_user

router = APIRouter()

@router.post("/renew")
def renew_token(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]  
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    return renew_token_controller(token)
