from typing import Dict
from sqlalchemy.orm import Session

from ..repository import game_repo, user_repo
from ..util.ollama_utils import stream_receive_message
from itertools import chain
import json


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
        role = "narrator" if i.sender == "narrator" else "user"
        messages.append({"role": role, "content": f"{i.content}"})
    gen = stream_receive_message(messages)
    try:
        first_chunk = next(gen)
    except StopIteration:
        inter = game_repo.add_interaction(db, game_id=game_id, sender="narrator", content="")
        def empty_iter():
            if False:
                yield ""
        return empty_iter()
    except RuntimeError:
        raise
    except Exception as e:
        raise RuntimeError(str(e))
    
    def stream_and_persist():
        collected = [first_chunk]
        yield first_chunk
        try:
            for chunk in gen:
                collected.append(chunk)
                yield chunk
        finally:
            try:
                final_text = "".join(collected)
                inter = game_repo.add_interaction(db, game_id=game_id, sender="narrator", content=final_text)
                interaction_obj = {
                    "interaction_id": inter.interaction_id,
                    "sender": inter.sender,
                    "content": inter.content,
                    "created_at": inter.created_at.isoformat(),
                }
                yield "\n__INTERACTION_JSON__\n" + json.dumps(interaction_obj)
            except Exception:
                pass

    return stream_and_persist()
