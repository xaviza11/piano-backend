from fastapi import HTTPException, Depends, Header
from auth.jwt_handler import decode_guest_token

def guard_guest_token(authorization: str = Header(...)):

    token = authorization.split(" ")[1] if " " in authorization else None
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    payload = decode_guest_token(token)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid guest token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload
