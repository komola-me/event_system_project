from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic.config import ConfigDict

from app.models.models import EventStatus

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
    model_config = ConfigDict(from_attributes=True)


class Participant_Out(BaseModel):
    id: int
    email: str
    model_config = ConfigDict(from_attributes=True)