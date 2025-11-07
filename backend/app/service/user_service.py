from typing import Dict
from sqlalchemy.orm import Session

from ..repository import user_repo

def get_user(db: Session, user_id: str) -> Dict:
    # TODO verify permissions based on token_user_id
	user = user_repo.get_user_by_id(db, user_id)
	if not user:
		raise ValueError("User not found")
	return {
		"user_id": user.user_id,
		"username": user.username,
		"email": user.email,
		"is_active": bool(user.is_active),
		"created_at": user.created_at,
	}


def get_user_by_username(db: Session, username: str) -> Dict:
	# TODO verify permissions based on token_user_id
	user = user_repo.get_user_by_username(db, username)
	if not user:
		raise ValueError("User not found")
	return {
		"user_id": user.user_id,
		"username": user.username,
		"email": user.email,
		"is_active": bool(user.is_active),
		"created_at": user.created_at,
	}

