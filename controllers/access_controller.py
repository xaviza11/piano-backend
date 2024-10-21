from fastapi import HTTPException
from auth.jwt_handler import renew_access_token

def renew_token(token: str):
    try:
        return renew_access_token(token)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)