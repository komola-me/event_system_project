from datetime import UTC, datetime
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from sqlalchemy import Enum as SQLAlchemyEnum

from app.database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(128), unique=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))

    events: Mapped[list["Event"]] = relationship(back_populates="organizer")
    event_registrations: Mapped[list["EventRegistration"]] = relationship(back_populates="user")


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250))
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    start_datetime: Mapped[datetime] = mapped_column(default=None, nullable=True)
    end_datetime: Mapped[datetime] = mapped_column(default=None, nullable=True)
    location_url: Mapped[str | None] = mapped_column(String(100), nullable=True)
    max_participant: Mapped[int] = mapped_column(default=0)
    organizer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    is_active: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))

    organizer: Mapped["User"] = relationship(back_populates="events")
    event_registrations: Mapped[list["EventRegistration"]] = relationship(back_populates="event")


class EventStatus(str, enum.Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    WAITLIST = "waitlist"

class EventRegistration(Base):
    __tablename__ = "event_registrations"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("events.id"))
    registered_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    status: Mapped[EventStatus] = mapped_column(SQLAlchemyEnum(EventStatus), default=EventStatus.WAITLIST)

    user: Mapped["User"] = relationship(back_populates="event_registrations")
    event: Mapped["Event"] = relationship(back_populates="event_registrations")
