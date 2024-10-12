from fastapi import APIRouter
from controllers.guest_controller import create_guest
from models.user_model import User
from services.guest_service import GuestService
# from fastapi.security import OAuth2PasswordRequestForm
# from guards.auth_guard import get_current_user

router = APIRouter()
guest_service = GuestService()

@router.get("/create")
def create_guest():
    return guest_service.create()
