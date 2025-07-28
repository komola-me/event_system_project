from fastapi import APIRouter, HTTPException, status

from app.dependency import db_dep
from app.models.models import Event
from app.schemas.event import EventCreate, EventListResponse

router = APIRouter(
    prefix="/event",
    tags=["event"],
)

@router.get("/", response_model=list[EventListResponse])
async def list_events(db: db_dep):
    events = db.query(Event).filter(Event.is_active == True).all()
    if not events:
        raise HTTPException(status_code=404, detail="No events found in db.")
    return events


@router.post("/create/", response_model=EventListResponse, status_code=status.HTTP_201_CREATED)
async def create_event(event_data: EventCreate, db: db_dep):
    new_event = Event(**event_data.dict())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event
