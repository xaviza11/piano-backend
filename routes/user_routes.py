from fastapi import APIRouter, Header, HTTPException, Depends
from controllers.user_controller import register_user
from models.user_model import User
from guards.guest_guard import guard_guest_token

router = APIRouter()

@router.post("/register")
def register(user: User, current_guest: dict = Depends(guard_guest_token)):
    return register_user(user)

# Ruta para iniciar sesión y obtener el token
# @router.post("/token")
# def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     return login_user(form_data)

# Ruta para obtener los detalles del usuario autenticado
# @router.get("/users/me")
# def get_user_me(current_user: dict = Depends(get_current_user)):
#     return read_users_me(current_user)
