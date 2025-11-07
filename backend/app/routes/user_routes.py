from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas.user_schema import UserOut
from ..service import user_service


user_router = APIRouter(prefix="/user", tags=["users"])


@user_router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: str, authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid auth scheme")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    try:
        auth_info = user_service.authenticate(token, db)
        token_user_id = auth_info.get("user_id")
        return user_service.get_user(db, user_id, token_user_id)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


router = APIRouter()
router.include_router(user_router)
