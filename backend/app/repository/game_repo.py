from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from ..core.database import Base


class GameModel(Base):
    __tablename__ = "games"
    game_id = Column(String, primary_key=True, index=True)
    owner_id = Column(String, index=True, nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


def create_game(db: Session, owner_id: str, title: str):
    game = GameModel(
        game_id=str(uuid.uuid4()),
        owner_id=owner_id,
        title=title,
    )
    db.add(game)
    db.commit()
    db.refresh(game)
    return game


def get_game_by_id(db: Session, game_id: str):
    return db.query(GameModel).filter(GameModel.game_id == game_id).first()


def get_games(db: Session, limit: int = 100):
    return db.query(GameModel).order_by(GameModel.created_at.desc()).limit(limit).all()


def get_games_by_owner(db: Session, owner_id: str):
    return db.query(GameModel).filter(GameModel.owner_id == owner_id).all()


def delete_game_by_id(db: Session, game_id: str):
    game = db.query(GameModel).filter(GameModel.game_id == game_id).first()
    if not game:
        return None
    db.delete(game)
    db.commit()
    return game
