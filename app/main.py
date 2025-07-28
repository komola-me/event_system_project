from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.event import router as event_router

app = FastAPI(debug=True)

@app.get('/')
async def root():
    return {"message": "Hello World!"}


app.include_router(auth_router)
app.include_router(event_router)