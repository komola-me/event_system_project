import asyncio
import smtplib
from email.mime.text import MIMEText
from celery import Celery

from app.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND, EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_PORT, SMTP_SERVER

celery = Celery(
    __name__,
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

async def write_notification(email: str, message=""):
    await asyncio.sleep(3)
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@celery.task
def send_email(to_email: str, subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["Body"] = body
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send email {to_email}: {e}")
