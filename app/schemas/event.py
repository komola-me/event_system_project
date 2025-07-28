from pydantic import BaseModel
from datetime import datetime


class EventCreate(BaseModel):
    title: str
    description: str
    start_datetime: datetime
    end_datetime: datetime
    location_url: str | None = None
    max_participant: int
    organizer_id: int
    is_active: bool
    created_at: datetime


class EventListResponse(BaseModel):
    id: int
    title: str
    description: str
    max_participant: int
    start_datetime: datetime
    end_datetime: datetime
    location_url: str | None = None
    is_active: bool
    created_at: datetime
