from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from ..core.database import get_db
from backend.app.schemas.play_schema import messageIn, messageOut
from ..service import play_service, oauth_service


play_router = APIRouter(prefix="/play", tags=["play"])


@play_router.post("/player", response_model=messageOut)
def player_play(message: messageIn, authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid auth scheme")
    except Exception:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    try:
        auth_info = oauth_service.authenticate(token, db)
        user_id = auth_info.get("user_id")
        return play_service.player_play(db, game_id=message.game_id, message=message.message, token_user_id=user_id)
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail=str(e))
    except RuntimeError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail=str(e))

@play_router.get("/narrator/{game_id}", response_model=messageOut)
def narrator_play(game_id: str, authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid auth scheme")
    except Exception:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    try:
        auth_info = oauth_service.authenticate(token, db)
        user_id = auth_info.get("user_id")
        return play_service.narrator_play(db, game_id=game_id, token_user_id=user_id)
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail=str(e))
    except RuntimeError as e:
        from fastapi import HTTPException
        # Downstream Ollama connection issues -> service unavailable
        raise HTTPException(status_code=503, detail=str(e))


router = APIRouter()
router.include_router(play_router)