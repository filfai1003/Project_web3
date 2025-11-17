from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas.oauth_schema import SignUpIn, LoginIn, Token
from ..service import oauth_service
from ..core.config import settings


oauth_router = APIRouter(prefix="/auth", tags=["auth"])


@oauth_router.post("/signup", response_model=Token)
def signup(user_in: SignUpIn, response: Response, db: Session = Depends(get_db)):
    try:
        res = oauth_service.signup(db, user_in)
        token = res.get("access_token")
        if token:
            response.set_cookie(
                key=settings.COOKIE_NAME if hasattr(settings, 'COOKIE_NAME') else 'access_token',
                value=token,
                httponly=True,
                secure=getattr(settings, 'COOKIE_SECURE', False),
                samesite=getattr(settings, 'COOKIE_SAMESITE', 'lax'),
                path=getattr(settings, 'COOKIE_PATH', '/'),
                max_age=getattr(settings, 'COOKIE_MAX_AGE_SECONDS', None),
            )
        return {"user_id": res.get("user_id"), "username": res.get("username"), "email": res.get("email")}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@oauth_router.post("/login", response_model=Token)
def login(payload: LoginIn, response: Response, db: Session = Depends(get_db)):
    try:
        res = oauth_service.login(db, payload)
        token = res.get("access_token")
        if token:
            response.set_cookie(
                key=settings.COOKIE_NAME if hasattr(settings, 'COOKIE_NAME') else 'access_token',
                value=token,
                httponly=True,
                secure=getattr(settings, 'COOKIE_SECURE', False),
                samesite=getattr(settings, 'COOKIE_SAMESITE', 'lax'),
                path=getattr(settings, 'COOKIE_PATH', '/'),
                max_age=getattr(settings, 'COOKIE_MAX_AGE_SECONDS', None),
            )
        return {"user_id": res.get("user_id"), "username": res.get("username"), "email": res.get("email")}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@oauth_router.get("/authenticate", response_model=Token)
def authenticate(request: Request, response: Response, db: Session = Depends(get_db)):
    token = request.cookies.get(getattr(settings, 'COOKIE_NAME', 'access_token'))
    if not token:
        raise HTTPException(status_code=401, detail="Missing auth cookie")
    try:
        res = oauth_service.authenticate(token, db)
        # refresh cookie with new token if provided
        new_token = res.get("access_token")
        if new_token:
            response.set_cookie(
                key=getattr(settings, 'COOKIE_NAME', 'access_token'),
                value=new_token,
                httponly=True,
                secure=getattr(settings, 'COOKIE_SECURE', False),
                samesite=getattr(settings, 'COOKIE_SAMESITE', 'lax'),
                path=getattr(settings, 'COOKIE_PATH', '/'),
                max_age=getattr(settings, 'COOKIE_MAX_AGE_SECONDS', None),
            )
        return {"user_id": res.get("user_id"), "username": res.get("username"), "email": res.get("email")}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@oauth_router.post('/logout')
def logout(response: Response):
    # clear the auth cookie
    response.delete_cookie(getattr(settings, 'COOKIE_NAME', 'access_token'), path=getattr(settings, 'COOKIE_PATH', '/'))
    return {"ok": True}


router = APIRouter()
router.include_router(oauth_router)