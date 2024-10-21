from fastapi import HTTPException
from services.guest_service import GuestService
from models.guest_model import Guest
from auth.jwt_handler import renew_guest_token

guest_service = GuestService()

def create_guest_token():
    try:
        return guest_service.create()
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
def renew_token(token: str):
    try:
        return renew_guest_token(token)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code,detail=e.detail)