from typing import Dict
from sqlalchemy.orm import Session

from ..repository import user_repo
from ..schemas.oauth_schema import SignUpIn, LoginIn
from ..outil.auth_utils import (
	get_password_hash,
	verify_password,
	create_access_token,
	decode_token,
)

def signup(db: Session, user_in: SignUpIn) -> Dict:
	if user_repo.get_user_by_username(db, user_in.username):
		raise ValueError("Username already registered")
	if user_in.email and user_repo.get_user_by_email(db, user_in.email):
		raise ValueError("Email already registered")
	hashed = get_password_hash(user_in.password)
	user = user_repo.create_user(db, username=user_in.username, email=user_in.email, password_hash=hashed)
	token = create_access_token({"sub": user.user_id})
	return {"access_token": token, "token_type": "bearer", "user_id": user.user_id}


def login(db: Session, payload: LoginIn) -> Dict:
	user = None
	if payload.username:
		user = user_repo.get_user_by_username(db, payload.username)
	elif payload.email:
		user = user_repo.get_user_by_email(db, payload.email)
	else:
		raise ValueError("username or email required")
	if not user or not verify_password(payload.password, user.password_hash):
		raise ValueError("Invalid credentials")
	token = create_access_token({"sub": user.user_id})
	return {"access_token": token, "token_type": "bearer", "user_id": user.user_id}


def authenticate(token: str, db: Session) -> Dict:
	data = decode_token(token)
	if not data or not data.user_id:
		raise ValueError("Invalid token")
	user = user_repo.get_user_by_id(db, data.user_id)
	if not user:
		raise ValueError("User not found")
	new_token = create_access_token({"sub": user.user_id})
	return {"access_token": new_token, "token_type": "bearer", "user_id": user.user_id}