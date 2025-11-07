from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from ..core.database import Base


class UserModel(Base):
	__tablename__ = "users"
	user_id = Column(String, primary_key=True, index=True)
	username = Column(String, unique=True, index=True, nullable=False)
	email = Column(String, unique=True, index=True, nullable=True)
	password_hash = Column(String, nullable=False)
	is_active = Column(Boolean, default=True)
	created_at = Column(DateTime, default=datetime.utcnow)


def create_user(db: Session, username: str, email: str, password_hash: str) -> UserModel:
	user = UserModel(
		user_id=str(uuid.uuid4()),
		username=username,
		email=email,
		password_hash=password_hash,
	)
	db.add(user)
	db.commit()
	db.refresh(user)
	return user


def get_user_by_username(db: Session, username: str):
	return db.query(UserModel).filter(UserModel.username == username).first()


def get_user_by_id(db: Session, user_id: str):
	return db.query(UserModel).filter(UserModel.user_id == user_id).first()


def get_user_by_email(db: Session, email: str):
	return db.query(UserModel).filter(UserModel.email == email).first()

