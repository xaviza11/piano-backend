from datetime import datetime, timedelta
from jose import JWTError, jwt
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

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
