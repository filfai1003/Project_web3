from typing import Dict, Iterator
from sqlalchemy.orm import Session

from ..repository import game_repo, user_repo
from ..util.ollama_utils import stream_receive_message
import json


SYSTEM_PROMPT = (
    "You are an evocative tabletop RPG narrator. Respond as the narrator, weaving vivid, immersive "
    "scenes that build on the players' previous actions. Keep responses concise (3-5 sentences) "
    "and avoid conclusively ending the story so players can continue."
)


def player_play(db: Session, game_id: str, message: str, token_user_id: str) -> Dict:
    game = game_repo.get_game_by_id(db, game_id)
    if not game:
        raise ValueError("Game not found")
    if game.owner_id != token_user_id:
        raise PermissionError("Not the owner")
    user = user_repo.get_user_by_id(db, token_user_id)
    sender = user.username or "player"
    inter = game_repo.add_interaction(db, game_id=game_id, sender=sender, content=message)
    return {"interaction_id": inter.interaction_id, "sender": inter.sender, "content": inter.content, "created_at": inter.created_at.isoformat()}


def narrator_play(db: Session, game_id: str, token_user_id: str) -> Dict:
    game = game_repo.get_game_by_id(db, game_id)
    if not game:
        raise ValueError("Game not found")
    if game.owner_id != token_user_id:
        raise PermissionError("Not the owner")
    interactions = game_repo.get_interactions_for_game(db, game_id)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for interaction in interactions:
        role = "assistant" if interaction.sender.lower() == "narrator" else "user"
        messages.append({"role": role, "content": interaction.content})

    request_prompt = (
        "Continue the adventure from the narrator's perspective, reacting naturally to the latest player input."
        if interactions
        else "Begin an exciting adventure as the narrator, establishing the setting and inviting the player to act."
    )
    messages.append({"role": "user", "content": request_prompt})

    gen = stream_receive_message(messages)
    try:
        first_chunk = next(gen)
    except StopIteration:
        inter = game_repo.add_interaction(db, game_id=game_id, sender="narrator", content="")
        def empty_iter() -> Iterator[str]:
            if False:
                yield ""
            yield "\n__INTERACTION_JSON__\n" + json.dumps({
                "interaction_id": inter.interaction_id,
                "sender": inter.sender,
                "content": inter.content,
                "created_at": inter.created_at.isoformat(),
            })
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
