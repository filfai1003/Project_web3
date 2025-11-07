from datetime import datetime, timedelta
from typing import Optional
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash
from jose import jwt, JWTError
from pydantic import BaseModel

from ..core.config import settings

ph = PasswordHasher()
ALGORITHM = "HS256"


class TokenData(BaseModel):
    user_id: Optional[str] = None

def get_password_hash(password: str) -> str:
    return ph.hash(password)

def verify_password(plain_password: str, stored_hash: str) -> bool:
    try:
        return ph.verify(stored_hash, plain_password)
    except (VerifyMismatchError, VerificationError, InvalidHash):
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return TokenData(user_id=user_id)
    except JWTError:
        return None
