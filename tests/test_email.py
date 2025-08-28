import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.tasks import send_email

send_email("admin@gmail.com", "Test", "Hello from Event System!")