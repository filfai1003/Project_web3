from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..core.config import settings
from ..repository import user_repo
from ..schemas.user_schema import UserCreate, TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


def get_password_hash(password: str) -> str:
	return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
	return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.utcnow() + expires_delta
	else:
		expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
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


def signup(db: Session, user_in: UserCreate) -> dict:
	existing = user_repo.get_user_by_username(db, user_in.username)
	if existing:
		raise ValueError("Username already registered")
	hashed = get_password_hash(user_in.password)
	user = user_repo.create_user(db, username=user_in.username, email=user_in.email, password_hash=hashed)
	token = create_access_token({"sub": user.user_id})
	return {"access_token": token, "token_type": "bearer", "user_id": user.user_id}


def login(db: Session, username: str, password: str) -> dict:
	user = user_repo.get_user_by_username(db, username)
	if not user:
		raise ValueError("Invalid credentials")
	if not verify_password(password, user.password_hash):
		raise ValueError("Invalid credentials")
	token = create_access_token({"sub": user.user_id})
	return {"access_token": token, "token_type": "bearer", "user_id": user.user_id}


def authenticate(token: str, db: Session) -> dict:
	data = decode_token(token)
	if not data or not data.user_id:
		raise ValueError("Invalid token")
	user = user_repo.get_user_by_id(db, data.user_id)
	if not user:
		raise ValueError("User not found")
	new_token = create_access_token({"sub": user.user_id})
	return {"access_token": new_token, "token_type": "bearer", "user_id": user.user_id}

