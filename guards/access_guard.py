from fastapi import HTTPException, Depends, Header
from auth.jwt_handler import decode_access_token

def guard_access_token(authorization: str = Header(...)):
    token = authorization.split(" ")[1] if " " in authorization else None
    
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid authorization header", headers={"WWW-Authenticate": "Bearer"},)
    
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return payload
