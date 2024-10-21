from fastapi import APIRouter, HTTPException, Header
from controllers.guest_controller import create_guest_token
from controllers.guest_controller import renew_guest_token
# from fastapi.security import OAuth2PasswordRequestForm
# from guards.auth_guard import get_current_user

router = APIRouter()

@router.get("/create")
def create_guest():
    return create_guest_token()

@router.post("/renew")
def renew_token(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1] 
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    return renew_guest_token(token)
