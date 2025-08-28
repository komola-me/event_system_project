import asyncio
import smtplib
from datetime import datetime, timedelta, UTC
from email.mime.text import MIMEText
from celery import Celery
from celery.schedules import crontab

from app.models.models import Event
from app.dependency import db_dep
from app.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND, EMAIL_USERNAME, EMAIL_FROM, EMAIL_PASSWORD, SMTP_PORT, SMTP_SERVER

celery = Celery(
    __name__,
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)


@celery.task
def send_email(to_email: str, subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = to_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send email {to_email}: {e}")


@celery.task
def send_daily_event_reminders():
    db = db_dep
    try:
        now = datetime.now(UTC)
        tommorrow_end = now + timedelta(days=1)

        events = db.query(Event).filter(
            Event.start_datetime.between(now, tommorrow_end)
        ).all()

        for event in events:
            for registration in event.event_registration:
                user = registration.user
                subject = f"Reminder: Upcoming Event - {event.title}"
                body = f"""
Hi, {user.username},
This is a reminder that you have registered for:
Event: {event.title}
Location: {event.location_url}
Date & Time: {event.start_datetime.strftime('%Y-%m-%d %H:%M UTC')}
See you there!
Yours, Event Management Team.
                """
                send_email.delay(to_email=user.email, subject=subject, body=body)

    finally:
        db.close()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=9, minutes=0),
        send_daily_event_reminders.s(),
        name="Send event reminders every morning",
    )


# async def write_notification(email: str, message=""):
#     await asyncio.sleep(3)
#     with open("log.txt", mode="w") as email_file:
#         content = f"notification for {email}: {message}"
#         email_file.write(content)
