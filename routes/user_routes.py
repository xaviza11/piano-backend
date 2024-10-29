from fastapi import APIRouter, Header, HTTPException, Depends
from controllers.user_controller import register_user
from controllers.user_controller import login_user
from controllers.user_controller import update_user
from models.user_model import User
from guards.guest_guard import guard_guest_token
from guards.access_guard import guard_access_token
from validators.register_validator import UserRegister
from validators.authenticate_validator import AuthenticateUser
from validators.update_user_validator import UpdateUser

router = APIRouter()

@router.post("/register")
def register(user: UserRegister, current_guest: dict = Depends(guard_guest_token)):
    return register_user(user)

@router.post("/login")
def login(user: AuthenticateUser, current_guest: dict = Depends(guard_guest_token)):
     return login_user(user)

@router.put("/update")
def update(user_data: UpdateUser, current_guest: dict = Depends(guard_access_token)):
     return update_user(user_data)

# Ruta para obtener los detalles del usuario autenticado
# @router.get("/users/me")
# def get_user_me(current_user: dict = Depends(get_current_user)):
#     return read_users_me(current_user)
