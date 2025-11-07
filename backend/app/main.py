# TODO
from fastapi import FastAPI

from .core.database import engine, Base
from .routes.user_routes import router as user_router


app = FastAPI(title="Project_web3 API")


@app.on_event("startup")
def on_startup():
	Base.metadata.create_all(bind=engine)

app.include_router(user_router)
@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}