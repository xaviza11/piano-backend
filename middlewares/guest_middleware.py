from fastapi import Depends, HTTPException
from auth.jwt_handler import decode_guest_token

def validate_guest_token(guest_token: str):
    if not decode_guest_token(guest_token):
        raise HTTPException(status_code=401, detail="Invalid guest token")