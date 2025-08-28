from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.middlewares import LoggingMiddleware

from app.routers.auth import router as auth_router
from app.routers.event import router as event_router
from app.routers.user import router as user_router
from app.routers.event_registration import router as event_registration_router

from app.admin.settings import admin

logging.basicConfig(level=logging.INFO)

app = FastAPI(debug=True)

app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get('/')
async def root():
    return {"message": "Hello World!"}


app.include_router(auth_router)
app.include_router(event_router)
app.include_router(user_router)
app.include_router(event_registration_router)

admin.mount_to(app=app)