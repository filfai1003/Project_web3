from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas.user_schema import UserOut
from ..service import oauth_service, user_service


user_router = APIRouter(prefix="/user", tags=["users"])


@user_router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: str, db: Session = Depends(get_db)):
    try:
        return user_service.get_user(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@user_router.get("/username/{username}", response_model=UserOut)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    try:
        return user_service.get_user_by_username(db, username)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

router = APIRouter()
router.include_router(user_router)
