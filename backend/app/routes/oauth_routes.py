
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas.oauth_schema import SignUpIn, LoginIn, Token
from ..service import user_service


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/signup", response_model=Token)
def signup(user_in: SignUpIn, db: Session = Depends(get_db)):
    try:
        return user_service.signup(db, user_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@auth_router.post("/login", response_model=Token)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    try:
        return user_service.login(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@auth_router.get("/authenticate", response_model=Token)
def authenticate(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    # Expect "Bearer <token>"
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid auth scheme")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    try:
        return user_service.authenticate(token, db)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


router = APIRouter()
router.include_router(auth_router)