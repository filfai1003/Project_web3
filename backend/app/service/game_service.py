from typing import List, Dict
from sqlalchemy.orm import Session

from ..repository import game_repo, user_repo


def create_game(db: Session, title: str, owner_id: str) -> Dict:
    game = game_repo.create_game(db, owner_id=owner_id, title=title)
    return {
        "game_id": game.game_id,
        "owner_id": game.owner_id,
        "title": game.title,
        "created_at": game.created_at,
        "interactions": [],
    }


def get_game(db: Session, game_id: str) -> Dict:
    game = game_repo.get_game_by_id(db, game_id)
    if not game:
        raise ValueError("Game not found")
    interactions = game_repo.get_interactions_for_game(db, game_id)
    return {
        "game_id": game.game_id,
        "owner_id": game.owner_id,
        "title": game.title,
        "created_at": game.created_at,
        "interactions": [
            {"sender": i.sender, "content": i.content, "created_at": i.created_at} for i in interactions
        ],
    }


def get_games(db: Session, limit: int = 100) -> List[Dict]:
    games = game_repo.get_games(db, limit=limit)
    return [
        {
            "game_id": g.game_id,
            "owner_id": g.owner_id,
            "title": g.title,
            "created_at": g.created_at,
            "interactions": [
                {"sender": i.sender, "content": i.content, "created_at": i.created_at}
                for i in game_repo.get_interactions_for_game(db, g.game_id)
            ],
        }
        for g in games
    ]


def get_games_by_owner(db: Session, owner_id: str) -> List[Dict]:
    games = game_repo.get_games_by_owner(db, owner_id)
    return [
        {
            "game_id": g.game_id,
            "owner_id": g.owner_id,
            "title": g.title,
            "created_at": g.created_at,
            "interactions": [
                {"sender": i.sender, "content": i.content, "created_at": i.created_at}
                for i in game_repo.get_interactions_for_game(db, g.game_id)
            ],
        }
        for g in games
    ]


def delete_game(db: Session, game_id: str, token_user_id: str) -> Dict:
    game = game_repo.get_game_by_id(db, game_id)
    if not game:
        raise ValueError("Game not found")
    if game.owner_id != token_user_id:
        raise PermissionError("Not the owner")
    deleted = game_repo.delete_game_by_id(db, game_id)
    if not deleted:
        raise ValueError("Game not found")
    return {"game_id": game_id, "deleted": True}
