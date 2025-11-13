from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

from ..core.database import get_db
from ..schemas.game_schema import GameOut
from ..service import game_service, oauth_service


game_router = APIRouter(prefix="/game", tags=["games"])


@game_router.get("/", response_model=list[GameOut])
def get_games(db: Session = Depends(get_db)):
    try:
        return game_service.get_games(db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@game_router.post("/", response_model=GameOut)
def create_game(title: str, authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid auth scheme")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    try:
        auth_info = oauth_service.authenticate(token, db)
        owner_id = auth_info.get("user_id")
        return game_service.create_game(db, title=title, owner_id=owner_id)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except OperationalError as e:
        raise HTTPException(status_code=503, detail="Database busy, riprova tra pochi istanti.")

@game_router.get("/{game_id}", response_model=GameOut)
def get_game(game_id: str, db: Session = Depends(get_db)):
    try:
        return game_service.get_game(db, game_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@game_router.get("/owner/{owner_id}", response_model=list[GameOut])
def get_games_by_owner(owner_id: str, db: Session = Depends(get_db)):
    try:
        return game_service.get_games_by_owner(db, owner_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@game_router.delete("/{game_id}")
def delete_game(game_id: str, authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid auth scheme")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    try:
        auth_info = oauth_service.authenticate(token, db)
        token_user_id = auth_info.get("user_id")
        return game_service.delete_game(db, game_id, token_user_id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


router = APIRouter()
router.include_router(game_router)