from uvicorn import run
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.routes.api import router as user_router

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="test")
app.include_router(user_router)

if __name__ == '__main__':
    run(app=app)
