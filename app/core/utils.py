from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext

from ..config import security_settings

_password_context = CryptContext(schemes=["argon2", "bcrypt"])


def hash_password(password: str) -> str:
    return _password_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return _password_context.verify(plain, hashed)


def generate_access_token(data:dict, expiry: timedelta = timedelta(days=1)) -> str:
    token = jwt.encode(
        payload={
            **data, 
            "exp": datetime.now(timezone.utc) + expiry,
            "jti": str(uuid4())        
            },
        key=security_settings.JWT_SECRET_KEY,
        algorithm=security_settings.JWT_ALGORITHM
    )
    return token

def decode_access_token(token:str)-> dict:
    try:
        return jwt.decode(token, key=security_settings.JWT_SECRET_KEY, algorithms=[security_settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")


def verify_access_token(token:str)->dict:
    t = token.split(",")
    print(t)
    data = decode_access_token(token=t[0])
    if data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return data