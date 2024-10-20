# app.py

from fastapi import FastAPI
from routes.user_routes import router as user_router
from routes.default_page import router as default_router
from routes.guest_routes import router as guest_router
from routes.song_routes import router as song_router
from routes.access_routes import router as access_token_router

app = FastAPI()

app.include_router(user_router, prefix="/user", tags=["auth"])
app.include_router(access_token_router, prefix="/accessToken", tags=["accessToken"])
app.include_router(guest_router, prefix="/guestToken", tags=["guestTokens"])
app.include_router(song_router, prefix="/song", tags=["song"])
app.include_router(default_router, tags=["default"])
