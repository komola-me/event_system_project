from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from models.models import EventStatus

class EventRegistrationCreate(BaseModel):
    user_id: int
    event_id: int
    registered_at: datetime
    status: Optional[EventStatus] = EventStatus.WAITLIST


class EventRegistrationRead(BaseModel):
    id: int
    user_id: int
    event_id: int
    registered_at: datetime
    status: EventStatus

    class Config:
        orm_mode = True