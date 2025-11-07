from typing import Dict
from sqlalchemy.orm import Session

from ..repository import game_repo, user_repo
from ..util.ollama_utils import receive_message


def player_play(db: Session, game_id: str, message: str, token_user_id: str) -> Dict:
    game = game_repo.get_game_by_id(db, game_id)
    if not game:
        raise ValueError("Game not found")
    if game.owner_id != token_user_id:
        raise PermissionError("Not the owner")
    user = user_repo.get_user_by_id(db, token_user_id)
    sender = user.username
    inter = game_repo.add_interaction(db, game_id=game_id, sender=sender, content=message)
    return {"interaction_id": inter.interaction_id, "sender": inter.sender, "content": inter.content, "created_at": inter.created_at.isoformat()}


def narrator_play(db: Session, game_id: str, token_user_id: str) -> Dict:
    game = game_repo.get_game_by_id(db, game_id)
    if not game:
        raise ValueError("Game not found")
    if game.owner_id != token_user_id:
        raise PermissionError("Not the owner")
    interactions = game_repo.get_interactions_for_game(db, game_id)
    messages = []
    for i in interactions:
        role = "assistant" if i.sender == "assistant" else "user"
        messages.append({"role": role, "content": f"{i.sender}: {i.content}"})
    ai_text = receive_message(messages)
    inter = game_repo.add_interaction(db, game_id=game_id, sender="assistant", content=ai_text)
    return {"interaction_id": inter.interaction_id, "sender": inter.sender, "content": inter.content, "created_at": inter.created_at.isoformat()}
