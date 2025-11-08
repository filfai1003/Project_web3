from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import Session, relationship
from datetime import datetime
import uuid

from ..core.database import Base


class GameModel(Base):
    __tablename__ = "games"
    game_id = Column(String, primary_key=True, index=True)
    owner_id = Column(String, index=True, nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    interactions = relationship("InteractionModel", back_populates="game", cascade="all, delete-orphan")


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


class InteractionModel(Base):
    __tablename__ = "interactions"
    interaction_id = Column(String, primary_key=True, index=True)
    game_id = Column(String, ForeignKey("games.game_id"), nullable=False, index=True)
    sender = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    game = relationship("GameModel", back_populates="interactions")


def add_interaction(db: Session, game_id: str, sender: str, content: str):
    inter = InteractionModel(
        interaction_id=str(uuid.uuid4()),
        game_id=game_id,
        sender=sender,
        content=content,
    )
    db.add(inter)
    db.commit()
    db.refresh(inter)
    return inter


def get_interactions_for_game(db: Session, game_id: str):
    return db.query(InteractionModel).filter(InteractionModel.game_id == game_id).order_by(InteractionModel.created_at.asc()).all()
