# TODO
from fastapi import FastAPI

from .core.database import engine, Base
from .routes.game_routes import game_router
from .routes.oauth_routes import oauth_router
from .routes.play_routes import play_router
from .routes.user_routes import user_router


app = FastAPI(title="Project_web3 API")


@app.on_event("startup")
def on_startup():
	Base.metadata.create_all(bind=engine)


app.include_router(game_router)
app.include_router(oauth_router)
app.include_router(play_router)
app.include_router(user_router)

@app.get("/")
@app.get("/health")
@app.get("/healthcheck")
def healthcheck():
	return {"status": "ok"}