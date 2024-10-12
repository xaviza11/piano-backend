from fastapi import HTTPException
from services.guest_service import GuestService
from models.guest_model import Guest

guest_service = GuestService()

def create_guest(guest: Guest):
    try:
        guest_service.create(guest)
        return {"message": "User registered successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)