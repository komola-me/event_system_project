from fastapi import APIRouter, HTTPException, status, Response
from typing import List

from app.dependency import db_dep, current_user_dep, pagination_dep
from app.models.models import Event
from app.schemas.event import EventCreate, EventListResponse, EventOut

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("/", response_model=List[EventListResponse])
async def list_events(db: db_dep, pagination: pagination_dep):
    events = db.query(Event).filter(Event.is_active == True)
    if not events:
        raise HTTPException(status_code=404, detail="No events found.")

    if pagination["q"]:
        events = events.filter(Event.title.ilike(f"%{pagination['q']}"))

    if pagination["location"]:
        events = events.filter(Event.location_url.ilike(f"%{pagination["location"]}%"))

    if pagination["date_from"]:
        events = events.filter(Event.start_datetime >= pagination["date_from"])

    if pagination["sort_by"] in {"start_datetime", "title"}:
        sort_field = getattr(Event, pagination["sort_by"])
        events = events.order_by(sort_field)

    events = events.offset(pagination["offset"]).limit(pagination["limit"]).all()
    return events


@router.post("/create/", response_model=EventOut)
async def create_event(event: EventCreate, db: db_dep, current_user: current_user_dep):
    new_event = Event(**event.model_dump(), organizer_id=current_user.id)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event


@router.get("/{event_id}/", response_model=EventListResponse)
async def get_event_by_id(db: db_dep, event_id: int):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event or not event.is_active:
        raise HTTPException(status_code=404, detail="Event Not Found")

    return event


@router.put("/update/{event_id}/", response_model=EventOut)
async def update_event(db:db_dep, event_data: EventCreate, current_user: current_user_dep, event_id: int):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the organizer of the event.")

    for key, value in event_data.model_dump().items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)

    return event


@router.delete("/delete/{event_id}/", status_code=204)
async def delete_event(event_id: int, db: db_dep, current_user: current_user_dep):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404, details="Not found")

    if event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this event")

    db.delete(event)
    db.commit()
    return {"message": "Event has been successfully deleted."}