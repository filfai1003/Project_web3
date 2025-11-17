from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..core.database import get_db
from backend.app.schemas.play_schema import messageIn, messageOut
from ..service import play_service, oauth_service


play_router = APIRouter(prefix="/play", tags=["play"])


@play_router.post("/player", response_model=messageOut)
def player_play(message: messageIn, request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get('access_token')
    if not token:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Missing auth cookie")
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

@play_router.get("/narrator/{game_id}")
def narrator_play(game_id: str, request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get('access_token')
    if not token:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Missing auth cookie")
    try:
        auth_info = oauth_service.authenticate(token, db)
        user_id = auth_info.get("user_id")
        stream_iter = play_service.narrator_play(db, game_id=game_id, token_user_id=user_id)
        return StreamingResponse(stream_iter, media_type="text/plain; charset=utf-8")
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail=str(e))
    except RuntimeError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail=str(e))


router = APIRouter()
router.include_router(play_router)