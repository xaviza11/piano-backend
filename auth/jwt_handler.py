from datetime import datetime, timedelta
from jose import JWTError, jwt
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
GUEST_SECRET_KEY = os.getenv("GUEST_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
GUEST_TOKEN_EXPIRE_MINUTES = int(os.getenv("GUEST_TOKEN_EXPIRE_MINUTES", 60))
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY").encode()

fernet = Fernet(ENCRYPTION_KEY)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    encrypted_jwt = fernet.encrypt(jwt_token.encode()).decode()
    return encrypted_jwt

def decode_access_token(token: str):
    try:
        decrypted_jwt = fernet.decrypt(token.encode()).decode()
        decoded_data = jwt.decode(decrypted_jwt, SECRET_KEY, algorithms=[ALGORITHM])
        if "exp" in decoded_data:
            decoded_data["exp"] = datetime.fromtimestamp(decoded_data["exp"])
        return decoded_data
    except (JWTError, Exception):
        return None
    
def renew_access_token(token: str):
    decoded_data = decode_access_token(token)
    
    if not decoded_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    expiration_time = decoded_data.get("exp")
    
    if not expiration_time:
        raise HTTPException(status_code=400, detail="Token does not contain expiration time")

    current_time = datetime.utcnow()
    time_left = expiration_time - current_time
    
    if time_left < timedelta(days=1):
        user_data = {key: decoded_data[key] for key in decoded_data if key != "exp"}  
        new_token = create_access_token(user_data)
        current_date = datetime.utcnow().isoformat() + "Z"
        return {
            "message": "Token renewed successfully",
            "token": new_token,
            "date": current_date
        }
    
    current_date = datetime.utcnow().isoformat() + "Z"
    return {
        "message": "Token does not need renewal yet",
        "token": token,
        "date": current_date
    }

def generate_guest_token(guest_id: str):
    expire = datetime.utcnow() + timedelta(minutes=GUEST_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": guest_id, "exp": expire}
    jwt_token = jwt.encode(to_encode, GUEST_SECRET_KEY, algorithm=ALGORITHM)
    encrypted_guest_token = fernet.encrypt(jwt_token.encode()).decode()
    return encrypted_guest_token

def decode_guest_token(token: str):
    try:
        decrypted_jwt = fernet.decrypt(token.encode()).decode()
        decoded_data = jwt.decode(decrypted_jwt, GUEST_SECRET_KEY, algorithms=[ALGORITHM])
        if "exp" in decoded_data:
            decoded_data["exp"] = datetime.fromtimestamp(decoded_data["exp"])
        return decoded_data
    except (JWTError, Exception):
        return None
    
def renew_guest_token(token: str):
    decoded_data = decode_guest_token(token)
    
    if not decoded_data:
        raise HTTPException(status_code=401, detail="Invalid guest token")
    
    expiration_time = decoded_data.get("exp")
    
    if not expiration_time:
        raise HTTPException(status_code=400, detail="Guest token does not contain expiration time")
    
    current_time = datetime.utcnow()
    time_left = expiration_time - current_time

    if time_left < timedelta(days=1):
        guest_id = decoded_data.get("sub")
        new_token = generate_guest_token(guest_id)
        current_date = datetime.utcnow().isoformat() + "Z"
        return {
            "message": "Guest token renewed successfully",
            "token": new_token,
            "date": current_date
        }
    
    current_date = datetime.utcnow().isoformat() + "Z"
    return {
        "message": "Guest token does not need renewal yet",
        "token": token,
        "date": current_date
    }
