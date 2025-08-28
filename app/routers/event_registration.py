from fastapi import APIRouter, HTTPException

from app.schemas.event_registration import EventRegistrationCreate, EventRegistrationRead
from app.dependency import db_dep, current_user_dep
from app.models.models import EventRegistration, Event, User, EventStatus
from app.tasks import send_email

router = APIRouter(prefix="/event_registration", tags=["Event Registration"])

@router.post("/events/{event_id}/register/", status_code=201)
async def register_for_event(event_id: int, db: db_dep, current_user: current_user_dep):
    event = db.query(Event).filter(Event.id == event_id, Event.is_active == True).first()
    if not event or not event.is_active:
        raise HTTPException(status_code=404, detail="Event not found!")

    already_registered = db.query(EventRegistration).filter_by(event_id = event_id, user_id=current_user.id).first()
    if already_registered:
        raise HTTPException(status_code=400, detail="You are already registered for the event.")

    reg_count = db.query(EventRegistration).filter_by(event_id=event_id, status=EventStatus.CONFIRMED).count()
    status = EventStatus.WAITLIST if reg_count >= event.max_participant else EventStatus.CONFIRMED

    reg = EventRegistration(event_id = event_id, user_id=current_user.id, status=status)
    db.add(reg)
    db.commit()

    send_email.delay(
        to_email = current_user.email,
        subject = "Registration for an {event.title} event",
        body = f"""
Hi there!
You have successfully registered for the event:
Title: {event.title}
Date: {event.start_datetime}
Location: {event.location_url}

See you there!

Best regards,
The Event Management System!
        """
    )

    return {"msg": "Registration successful"}


@router.delete("/events/{event_id}/delete_regs/", status_code=204)
async def cancel_registration(event_id: int, db: db_dep, current_user: current_user_dep):
    registry = db.query(EventRegistration).filter_by(event_id=event_id, user_id=current_user.id).first()

    if not registry:
        raise HTTPException(status_code=404, detail="Not Registered.")

    db.delete(registry)
    db.commit()
    return {"msg": "Event registration has been successfully cancelled."}


@router.get("events/{event_id}/participants")
async def list_participants(event_id: int, db: db_dep):
    all_registered_users = db.query(User).join(EventRegistration, EventRegistration.user_id == User.id).filter(EventRegistration.id == event_id).all()

    return all_registered_users