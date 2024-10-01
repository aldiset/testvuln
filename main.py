from fastapi import FastAPI
from app.routes.api import router as user_router

app = FastAPI()

# Include user-related routes
app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "Hello, Everyone!"}
